# Webhook Test Fixtures (Zoho Sign)

Offline-testable payload fixtures for the signature webhook handler, one file per event
type, plus a helper to sign them with the correct HMAC so tests exercise the real
verification path (`X-ZS-WEBHOOK-SIGNATURE` + `X-ZS-WEBHOOK-TIMESTAMP`, per
`webhook-spec.md`).

## Files

| File | Event | Handler expectation |
|---|---|---|
| `sent.json` | `sent` | Update stage → Proposal Sent, attach frozen PDF, day-3 activity |
| `viewed.json` | `viewed` | Audit log only |
| `signed_by_a_recipient.json` | `signed_by_a_recipient` | Audit log only |
| `completed_by_all.json` | `completed_by_all` | Hash check → Won, signed PDF + audit cert, draft invoice, notify |
| `declined.json` | `declined` | Lost + reason + SDR follow-up |
| `expires.json` | `expires` | Stalled + SDR follow-up |
| `recalled.json` | `recalled` | Stalled + SDR follow-up |
| `hard_bounced.json` | `hard_bounced` | Log + alert SDR; never Won |
| `reassigned.json` | `reassigned` | Audit log + signer details update |
| `sign_fixture.py` | — | Computes `X-ZS-WEBHOOK-TIMESTAMP` + `X-ZS-WEBHOOK-SIGNATURE` for a payload |

## Payload shape

Fixtures use the canonical Zoho Sign webhook callback shape: a top-level `event` object
with `event_id`, `event_type`, `event_time`, `account_id`, `request_id` (the envelope
ID), plus `request_name` and `actions[]`. Handler-relevant fields (envelope id, actor,
reason) are included; the handler maps `request_id` → `envelope_id` via its provider
adapter.

> **Note**: field names are *indicative* of Zoho Sign's documented callback format. When
> the first real callback is received, reconcile the exact field names in the handler's
> provider adapter and update these fixtures to match — do not assume the wire format is
> frozen.

## Usage

```bash
# Sign one fixture and print headers for a test request
python sign_fixture.py completed_by_all.json --secret whsec_test_0000

# Output (JSON):
# {
#   "X-ZS-WEBHOOK-TIMESTAMP": 1722758400,
#   "X-ZS-WEBHOOK-SIGNATURE": "base64...",
#   "body_sha256": "hex..."
# }
```

The handler test suite should:
1. Build a request from the fixture + signed headers → expect HTTP 200 and the
   event-specific Odoo/audit behaviour.
2. Tamper with the body → expect HTTP 401 (HMAC mismatch).
3. Replay the same `envelope_id` + `event_id` → expect HTTP 200 "Duplicate event ignored".
4. Send a stale timestamp (> 300 s skew) → expect HTTP 401 (timestamp skew rejected).

## Test secret

Fixtures are signed with any secret you pass; for deterministic tests use
`whsec_test_0000` and set `ZOHO_SIGN_WEBHOOK_SECRET=whsec_test_0000` in the test env.
Never use a production secret in tests.
