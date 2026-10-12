# Practice 01 — "Some of our webhooks fail signature verification"

You are a support engineer at **Hookline**, which sends signed webhooks to
customers. A customer has opened [ticket.md](ticket.md).

## What you have

| Path | What it is |
|---|---|
| `ticket.md` | The customer's message |
| `logs/receiver.log` | The customer's receiver log for the period (they attached it) |
| `data/events.jsonl` | The events Hookline sent them, exported from the admin tool |
| `CHANGELOG.md` | Hookline release notes |
| `app/` | Hookline's webhook sender (your product's code) |
| `customer/receiver.py` | The customer's verification code (they shared it) |
| `tools/replay.py` | Re-sends events from `data/` through sender → receiver locally |
| `tests/` | Hookline's existing tests (`python3 -m unittest discover -s tests`) |

Everything is local and stdlib-only Python. Nothing here touches a network.

## Your job

1. Scaffold a case: `bin/new-case webhook-signatures` (from the workbench root).
2. Work it per [WALKTHROUGH.md](WALKTHROUGH.md). Treat `app/` as production code: read it,
   replay against it, but don't edit it until you have a reproduction.
3. Finish with a filled-in `case.md`, `customer-reply.md` and `escalation.md`.

Useful starting points (run from this directory):

```sh
python3 tools/replay.py                  # replay every event with current code
python3 tools/replay.py --event evt_0012 # replay one
```

## Self-check

When you're done, compare against `.solution/ANSWER.md`. Don't open it first.
