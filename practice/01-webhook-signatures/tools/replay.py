#!/usr/bin/env python3
"""Replay exported events through the sender and the customer's receiver, locally.

    python3 tools/replay.py [--event evt_0012] [--secret whsec_…] [--skew SECONDS]

Prints one line per delivery in the receiver's log format. Read-only: nothing is
sent anywhere and no files are written.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.webhooks import build_delivery  # noqa: E402
from customer.receiver import verify  # noqa: E402

DEFAULT_SECRET = "whsec_test_northwind_9f3c"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--event", action="append", help="event id to replay (repeatable)")
    parser.add_argument("--secret", default=DEFAULT_SECRET, help="secret used by BOTH sides")
    parser.add_argument("--skew", type=int, default=0, help="receiver clock offset in seconds")
    parser.add_argument("--events-file", default=str(ROOT / "data" / "events.jsonl"))
    args = parser.parse_args()

    failed = total = 0
    with open(args.events_file, encoding="utf-8") as fh:
        for line in fh:
            event = json.loads(line)
            if args.event and event["id"] not in args.event:
                continue
            delivery = build_delivery(event, args.secret)
            ok, reason = verify(
                args.secret,
                delivery.headers["Hookline-Signature"],
                delivery.body,
                now=delivery.timestamp + args.skew,
            )
            total += 1
            failed += not ok
            when = datetime.fromtimestamp(delivery.timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            print(
                f"{when} delivery={delivery.id} event={event['id']} type={event['type']} "
                f"status={200 if ok else 401} reason={reason} bytes={len(delivery.body)}"
            )

    print(f"# {total} replayed, {failed} failed", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
