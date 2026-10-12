"""Wire encoding for outbound webhook requests."""
import json


def encode_body(event: dict) -> bytes:
    # 2.4.1: send readable UTF-8 rather than \uXXXX escapes.
    return json.dumps(event, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def headers(signature: str, delivery_id: str) -> dict:
    return {
        "Content-Type": "application/json; charset=utf-8",
        "Hookline-Delivery": delivery_id,
        "Hookline-Signature": signature,
        "User-Agent": "Hookline-Webhooks/2.4",
    }
