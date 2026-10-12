"""Build outbound webhook deliveries."""
import json
from dataclasses import dataclass
from typing import Optional

from . import signing, transport


@dataclass
class Delivery:
    id: str
    timestamp: int
    headers: dict
    body: bytes


def build_delivery(event: dict, secret: str, now: Optional[int] = None) -> Delivery:
    timestamp = now if now is not None else event["created"]
    delivery_id = "dlv_" + event["id"].split("_", 1)[1]
    payload = json.dumps(event, separators=(",", ":"))
    signature = signing.sign(secret, timestamp, payload)
    return Delivery(
        id=delivery_id,
        timestamp=timestamp,
        headers=transport.headers(signature, delivery_id),
        body=transport.encode_body(event),
    )
