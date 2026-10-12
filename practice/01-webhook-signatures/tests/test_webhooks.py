import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.webhooks import build_delivery
from customer.receiver import verify

SECRET = "whsec_test_unit"


class WebhookSignatureTest(unittest.TestCase):
    def test_delivery_verifies_with_reference_receiver(self):
        event = {
            "id": "evt_0001",
            "type": "customer.updated",
            "created": 1758000000,
            "data": {"customer": {"id": "cus_100", "name": "Acme Freight", "city": "Leeds"}},
        }
        delivery = build_delivery(event, SECRET)
        ok, reason = verify(SECRET, delivery.headers["Hookline-Signature"], delivery.body, now=event["created"])
        self.assertTrue(ok, reason)

    def test_wrong_secret_is_rejected(self):
        event = {"id": "evt_0002", "type": "invoice.paid", "created": 1758000000, "data": {"amount": 1200}}
        delivery = build_delivery(event, SECRET)
        ok, reason = verify("whsec_other", delivery.headers["Hookline-Signature"], delivery.body, now=event["created"])
        self.assertFalse(ok)
        self.assertEqual(reason, "signature_mismatch")

    def test_stale_timestamp_is_rejected(self):
        event = {"id": "evt_0003", "type": "invoice.paid", "created": 1758000000, "data": {"amount": 1200}}
        delivery = build_delivery(event, SECRET)
        ok, reason = verify(SECRET, delivery.headers["Hookline-Signature"], delivery.body, now=event["created"] + 900)
        self.assertFalse(ok)
        self.assertEqual(reason, "timestamp_out_of_tolerance")


if __name__ == "__main__":
    unittest.main()
