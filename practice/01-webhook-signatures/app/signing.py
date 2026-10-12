"""Hookline webhook signatures.

Header format:  Hookline-Signature: t=<unix seconds>,v1=<hex hmac-sha256>
Signed string:  "<t>.<payload>"
"""
import hashlib
import hmac


def sign(secret: str, timestamp: int, payload: str) -> str:
    signed = f"{timestamp}.{payload}".encode("utf-8")
    mac = hmac.new(secret.encode("utf-8"), signed, hashlib.sha256)
    return f"t={timestamp},v1={mac.hexdigest()}"
