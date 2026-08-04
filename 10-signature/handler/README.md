# Signature Webhook Handler — Reference Implementation

Pure-stdlib Python 3 reference implementation of the separate webhook handler
service specified in `10-signature/webhook-spec.md`. This is a **reference**:
it is runnable offline against the fixture pack in
`10-signature/webhook-fixtures/` so the pipeline contract can be exercised
before the production service is deployed. The production deployment is a
separate service (per `webhook-spec.md`); this package is the executable
specification.

## Layout

```
handler/
├── README.md          this file
├── handler.py         entry point: HTTP server + offline self-test CLI
├── config.py          environment-variable loading (no secrets in code)
├── hmac_verify.py     X-ZS-WEBHOOK-TIMESTAMP + X-ZS-WEBHOOK-SIGNATURE verification
├── store.py           SQLite idempotency + audit + dead-letter (mirrors webhook-db-schema.sql)
├── zoho_client.py     Zoho Sign API client (OAuth refresh, document download)
├── odoo_client.py     Odoo External API JSON-RPC 2.0 client (stub mode when offline)
├── notifications.py   SMTP notification dispatcher (templates in notification-templates/)
└── events.py          per-event handlers (sent/completed/declined/expired/...)
```

## Dependencies

Python 3.9+ standard library **only**. No pip installs. (PostgreSQL in
production per `webhook-db-schema.sql`; this reference uses SQLite with the
identical UNIQUE(envelope_id, event_id) constraint so it runs anywhere.)

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ZOHO_SIGN_WEBHOOK_SECRET` | yes* | `whsec_...` HMAC key (*required unless `--insecure-no-hmac` for offline dev) |
| `ZOHO_SIGN_CLIENT_ID` | no | OAuth client id (used only for document download on `completed`) |
| `ZOHO_SIGN_CLIENT_SECRET` | no | OAuth client secret |
| `ZOHO_SIGN_REFRESH_TOKEN` | no | OAuth refresh token |
| `ZOHO_SIGN_ACCOUNT_ID` | no | Zoho Sign account id |
| `ZOHO_SIGN_BASE_URL` | no | default `https://sign.zoho.com` |
| `ODOO_URL` | no | Odoo External API URL — **unset = stub mode** (no real writes) |
| `ODOO_DATABASE` | no | Odoo database name |
| `ODOO_API_KEY` | no | Odoo External API key |
| `ALERT_EMAIL` | no | dead-letter / critical alert recipient, default `sgc-admin@sgctech.ai` |

Secrets come from the environment or a secret manager only. **Never commit
them** (G52).

## Run offline (self-test against fixtures)

```powershell
$env:ZOHO_SIGN_WEBHOOK_SECRET = "whsec_test_0000"
python handler.py selftest ..\webhook-fixtures
```

`selftest` replays every fixture through the full pipeline (HMAC verify →
idempotency → dispatch) with the Odoo client in stub mode and prints a
PASS/FAIL table. Exit code 0 = all pass.

## Run as HTTP server

```powershell
python handler.py serve --host 127.0.0.1 --port 8443
```

Endpoint: `POST /webhooks/signature/zoho_sign/`

Behaviour contract (from `webhook-spec.md`):
- 400 — body is not valid JSON
- 401 — HMAC mismatch or stale timestamp
- 200 — event accepted; duplicate events return 200 "Duplicate event ignored"
- 500 — unexpected error (provider retries)
- Response is returned **before** async processing (never block > 500 ms)

## HMAC verification

Headers verified on every request (see `hmac_verify.py` and
`webhook-spec.md` §Security):

| Header | Meaning |
|---|---|
| `X-ZS-WEBHOOK-TIMESTAMP` | Unix seconds; rejected if `|now - ts| > 300` |
| `X-ZS-WEBHOOK-SIGNATURE` | `base64(HMAC-SHA256(raw_body, ZOHO_SIGN_WEBHOOK_SECRET))` |

Comparison is constant-time (`hmac.compare_digest`). Failed verification is
logged with the source IP and rejected with 401.

## Event dispatch

| Event | Odoo action (see `odoo-mapping.yaml`) |
|---|---|
| `sent` | stage → Proposal Sent; attach frozen PDF; day-3 follow-up activity |
| `viewed` | audit log only |
| `signed_by_a_recipient` | audit log only |
| `completed_by_all` | hash-verify signed PDF vs frozen; stage → Won; attach signed PDF + audit cert; draft mobilisation invoice (G51, never auto-posted); notify SDR + signatory + client |
| `declined` | stage → Lost; record reason; SDR follow-up |
| `expires` | stage → Stalled; SDR follow-up |
| `recalled` | stage → Stalled; SDR follow-up |
| `hard_bounced` | log + alert; **no** Won |
| `reassigned` | audit log + signer details |

On `completed`: the downloaded signed PDF SHA-256 must match the stored
frozen hash. Mismatch → CRITICAL, human alerted, **no Odoo write**,
return 200.

## Failure handling

- Async work (Odoo writes, emails) is queued after the 200 response.
- Retries: exponential backoff, max 3 attempts.
- After 3 failures → dead-letter queue + alert `ALERT_EMAIL`.
- Envelopes are never auto-reprocessed; a human reviews and re-triggers.
