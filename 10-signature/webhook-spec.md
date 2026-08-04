# Webhook Specification

Inbound endpoint receiving provider callbacks (Zoho Sign events). This document specifies the security model, event handling, idempotency, error handling, and the post-processing Odoo write-back.

---

## Endpoint

```
POST /webhooks/signature/{provider}/
```

The webhook handler is a separate service (not part of this repository) that:
1. Receives inbound callbacks from Zoho Sign
2. Verifies, validates, and logs every event
3. Performs Odoo write-back
4. Sends notification emails

The repository contains only this specification. The handler is deployed separately.

---

## Security

### HMAC verification (non-negotiable)

**Every** inbound callback must be verified before the body is parsed. Unverified payloads are rejected with HTTP 401 and logged to the audit log with the raw payload hash, source IP, and timestamp.

**Zoho Sign — verified headers:**

| Header | Value |
|---|---|
| `X-ZS-WEBHOOK-TIMESTAMP` | Unix timestamp of when Zoho Sign sent the callback |
| `X-ZS-WEBHOOK-SIGNATURE` | HMAC-SHA256 of the raw request body, base64-encoded, using the Zoho Sign webhook secret (`whsec_...`) |

**Zoho Sign HMAC verification (Node.js):**

```javascript
const crypto = require('crypto');

const payload   = request.rawBody;          // raw buffer, not parsed JSON
const timestamp = request.headers['x-zs-webhook-timestamp'];
const signature = request.headers['x-zs-webhook-signature'];

const expectedSig = crypto
  .createHmac('sha256', process.env.ZOHO_SIGN_WEBHOOK_SECRET)
  .update(payload)
  .digest('base64');

if (signature !== expectedSig) {
  // Reject — HMAC mismatch
}
```

**Verification steps (in order):**
1. Read `X-ZS-WEBHOOK-TIMESTAMP` as Unix integer.
2. Reject if `|current_server_time − timestamp| > 300 seconds` (5 minutes). Log: `Timestamp skew rejected: zs_timestamp={ts}, server_time={now}, diff={diff}s`.
3. Compute HMAC-SHA256 of the raw body using `ZOHO_SIGN_WEBHOOK_SECRET`. Compare to `X-ZS-WEBHOOK-SIGNATURE` using constant-time comparison (`crypto.timingSafeEqual`).
4. On mismatch: reject with 401. Log: `HMAC mismatch — potential spoofing from {ip_address}`.

**Note**: `X-ZS-WEBHOOK-TIMESTAMP` is the authoritative timestamp source, not the `event_time` field inside the JSON payload. Use the header for replay protection.

### Credential storage — Zoho Sign OAuth 2.0

Zoho Sign uses OAuth 2.0 with refresh tokens. The access token is short-lived; the refresh token is persistent and used to obtain a new access token automatically.

**Required environment variables:**

| Variable | Description |
|---|---|
| `ZOHO_SIGN_CLIENT_ID` | From Zoho Sign API console → Connected Apps |
| `ZOHO_SIGN_CLIENT_SECRET` | From Zoho Sign API console → Connected Apps |
| `ZOHO_SIGN_REFRESH_TOKEN` | Persistent token obtained from the OAuth authorization code exchange |
| `ZOHO_SIGN_ACCESS_TOKEN` | Short-lived access token; refreshed automatically by the SDK or token manager |
| `ZOHO_SIGN_WEBHOOK_SECRET` | The `whsec_...` value from the Zoho Sign webhook config UI (used for HMAC verification) |
| `ZOHO_SIGN_ACCOUNT_ID` | Zoho Sign account ID (visible in Zoho Sign settings) |
| `ZOHO_SIGN_BASE_URL` | Zoho Sign API base URL (e.g. `https://sign.zoho.com`) |

**Credential security:**
- `ZOHO_SIGN_CLIENT_ID`, `ZOHO_SIGN_CLIENT_SECRET`, and `ZOHO_SIGN_REFRESH_TOKEN` are stored in **environment variables** or a secret manager (AWS Secrets Manager, HashiCorp Vault).
- `ZOHO_SIGN_WEBHOOK_SECRET` is the HMAC signing secret — same storage class.
- **Never** in this repository, never in `odoo-mapping.yaml`, never in a committed `.env` file.
- The webhook handler reads secrets from environment variables at startup.
- Access tokens are stored in memory or a short-lived token cache only — never written to disk or logged.

---

## Idempotency

### Idempotency key

**Every event is idempotent by `envelope_id + event_id`.** Providers retry callbacks. A duplicate "signed" event must not create a second Odoo record or send a second notification email.

Implementation:
1. On receiving an event, extract `envelope_id` and the provider's event ID (e.g., Zoho Sign's `event_id` or `event_uuid`).
2. Check the audit log (append-only) for an entry with the same `envelope_id + event_id`.
3. If found: return HTTP 200 immediately, log: `Duplicate event ignored: {envelope_id}/{event_id}`.
4. If not found: process the event, then write the `envelope_id + event_id` pair to the audit log before returning.

### Idempotency table schema (audit log)

```
signature_events:
  - id: SERIAL PRIMARY KEY
  - envelope_id: TEXT NOT NULL
  - event_id: TEXT NOT NULL          -- provider's event ID
  - event_type: TEXT NOT NULL        -- sent | viewed | signed | completed | declined | expired | voided
  - processed_at: TIMESTAMPTZ NOT NULL
  - odoo_write_performed: BOOLEAN
  - notification_sent: BOOLEAN
  - UNIQUE(envelope_id, event_id)
```

The audit log is append-only. No UPDATE or DELETE operations.

---

## HTTP response

- Return **HTTP 200** immediately after the idempotency check passes and before any async processing.
- If the body cannot be parsed (invalid JSON): return HTTP 400, log the raw body.
- If HMAC verification fails: return HTTP 401, log the attempt.
- Any other error: return HTTP 500 — provider will retry.

**Never block the provider's callback thread** for more than 500ms. All Odoo writes, email sends, and async processing happen after the 200 response is returned.

---

## Event handling

### Events to handle (all required)

Zoho Sign event names as configured in the Zoho Sign webhook UI:

| Zoho Sign event | Description | Odoo action |
|---|---|---|
| `sent` | Envelope sent to all signers | Update stage, attach PDF, create day-3 activity |
| `viewed` | At least one signer viewed the envelope | Log to audit trail; no Odoo write |
| `signed_by_a_recipient` | Any signer completed their signature | Log to audit trail; no Odoo write yet |
| `completed_by_all` | All parties signed (both client and SGC) | Full write-back: Won stage, attach signed PDF + audit cert, create invoice draft, notify SDR |
| `declined` | Client or SGC declined | Move to lost/stalled, reason recorded, notify SDR |
| `expires` | 30-day expiry reached without completion | Move to stalled, notify SDR |
| `recalled` | SDR voided before completion | Move to stalled, notify SDR |
| `hard_bounced` | Signer email bounced | Log + alert SDR; do not write to Won |
| `reassigned` | Signer reassigned | Log to audit trail; update signer details |

### Handling: `completed`

Both parties must have signed. A client signature alone does **not** constitute completion (G49).

1. Verify hash of downloaded signed PDF against stored `frozen_sha256`. If mismatch → alert human immediately, do not write to Odoo.
2. Download signed PDF and audit certificate from Zoho Sign API.
3. Verify downloaded file hashes against what Zoho Sign reports in the callback metadata.
4. Write to Odoo (see `odoo-mapping.yaml`).
5. Send notifications (see `notification-templates/`).
6. Write audit log entry with all fields.
7. Return 200.

### Handling: `declined`, `expired`, `voided`

These events must move the CRM record **backward**, not leave it stale.

1. Extract decline reason if supplied (Zoho Sign `reason` field).
2. Write to Odoo: move to appropriate stage (`lost` or `stalled`), record reason in `description` or custom field.
3. Create follow-up activity for SDR.
4. Send SDR notification.
5. Write audit log entry.
6. Return 200.

---

## Async processing and failure handling

### Queue and retry

- Odoo writes and email sends are queued asynchronously after the 200 response.
- On queue entry failure: retry with exponential backoff, maximum 3 retries.
- After 3 retries: move to dead-letter queue, alert a named SGC admin by email/SMS.

### Dead-letter path

- Dead-letter queue entries include: full event payload, number of retries, error message, timestamp.
- Alert sent to: a human-configured alert email address (e.g., `sgc-admin@sgctech.ai`).
- The envelope is **not** automatically re-processed. A human reviews and manually triggers reprocessing if appropriate.

---

## Hash verification before Odoo write-back

Never trust document content from the callback payload itself. On `completed`:

1. Use the `envelope_id` from the callback to call Zoho Sign's API:
   ```
   GET /api/v1/envelope/{envelope_id}/documents
   GET /api/v1/envelope/{envelope_id}/audit_trail
   GET /api/v1/envelope/{envelope_id}/download?file_id=<document_id>
   ```
2. Verify the SHA-256 hash of the downloaded signed PDF against the stored `frozen_sha256`.
3. If the hash matches: proceed with Odoo write-back and notifications.
4. If the hash does **not** match:
   - Log a CRITICAL error: `Hash mismatch on {envelope_id}. Signed PDF does not match frozen original. Odoo write-back ABORTED.`
   - Alert human immediately.
   - Do NOT write to Odoo, do NOT send notification emails.
   - Return 200 (provider does not need to retry; the event was processed).

---

## Audit log entry schema

Every event logged:

```
signature_audit_log:
  - id: SERIAL PRIMARY KEY
  - logged_at: TIMESTAMPTZ NOT NULL DEFAULT NOW()
  - envelope_id: TEXT NOT NULL
  - event_type: TEXT NOT NULL
  - event_id: TEXT NOT NULL           -- provider's event UUID
  - event_timestamp: TIMESTAMPTZ        -- from provider payload
  - actor: TEXT                         -- e.g., "client" | "sgc" | "system"
  - actor_email: TEXT
  - actor_ip: TEXT                     -- from provider payload
  - provider: TEXT                     -- "zoho_sign"
  - raw_payload_hash: TEXT              -- SHA256 of raw JSON payload (for forensics)
  - odoo_opportunity_id: INTEGER
  - odoo_write_performed: BOOLEAN
  - odoo_write_details: TEXT           -- JSON summary of fields written
  - notification_sent: BOOLEAN
  - error_message: TEXT
  - UNIQUE(envelope_id, event_id)
```

The log is append-only. No UPDATE or DELETE. Records are retained per `audit-retention.md`.
