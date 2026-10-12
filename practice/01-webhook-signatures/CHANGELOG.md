# Hookline changelog

## 2.4.2 — 2026-10-01

- Dashboard: delivery list now paginates at 100 rows.
- Retry backoff capped at 6 hours (was 24).

## 2.4.1 — 2026-09-24 (deployed 14:00 UTC)

- Webhook bodies are now sent as readable UTF-8 instead of `\uXXXX` escapes.
  Several customers reported garbled names in tools that display the raw body.
- Fixed a typo in the `invoice.finalized` event description.

## 2.4.0 — 2026-09-15

- New event type: `customer.merged`.
- Signing secrets can be rotated from the dashboard; the previous secret stays
  valid for 0 hours after rotation (immediate cut-over).

## 2.3.9 — 2026-09-02

- Timestamp tolerance guidance in docs changed from 10 minutes to 5 minutes.
