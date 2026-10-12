# Ticket #48213 — Webhook signature verification failing intermittently

**From:** Priya Raman, Platform Engineering, Northwind Logistics
**Received:** 2026-10-06 09:14 UTC
**Plan:** Business
**Priority (customer-set):** High

Hi,

Since roughly the end of September a chunk of your webhooks are failing
signature verification on our side and we're dropping them. It's not all of
them, most go through fine, which is what makes this so annoying. We haven't
changed our receiver code in months (attached, it's basically your sample).

Things I can think of:

- We rotated our webhook signing secret on Sept 25 as part of a routine
  rotation. Could some of your senders still be using the old secret?
- Our receiver runs in two regions. Maybe clock drift on one of them is
  tripping the timestamp tolerance?

We're missing customer updates in our CRM sync because of this and it's
getting noticed. I've attached our receiver log for the last two weeks. The
current secret is the one ending `…9f3c` in your dashboard.

Can you tell us what's going on?

Priya

---

*Internal note (support tooling):* test-mode signing secret for this account is
`whsec_test_northwind_9f3c`. Previous secret (revoked 2026-09-25 08:00 UTC):
`whsec_test_northwind_a71e`.
