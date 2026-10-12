"""Northwind's webhook verification (shared by the customer; based on Hookline's sample)."""
import hashlib
import hmac

TOLERANCE_SECONDS = 300


def verify(secret: str, signature_header: str, body: bytes, now: int):
    """Return (ok, reason). Verifies the HMAC over the raw request body."""
    try:
        parts = dict(item.split("=", 1) for item in signature_header.split(","))
        timestamp = int(parts["t"])
        received = parts["v1"]
    except (KeyError, ValueError):
        return False, "malformed_header"

    if abs(now - timestamp) > TOLERANCE_SECONDS:
        return False, "timestamp_out_of_tolerance"

    signed = str(timestamp).encode("ascii") + b"." + body
    expected = hmac.new(secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received):
        return False, "signature_mismatch"
    return True, "ok"
