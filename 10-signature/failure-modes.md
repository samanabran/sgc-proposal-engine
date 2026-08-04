# Failure Modes

Each failure mode describes: the trigger, the detection mechanism, the immediate response, and the resolution path.

---

## FM-01: HMAC verification fails on inbound callback

**Trigger**: `X-ZS-WEBHOOK-SIGNATURE` HMAC does not match the computed HMAC of the raw payload.

**Detection**: Webhook handler — HMAC check before body parsing.

**Immediate response**:
- Return HTTP 401.
- Log: raw payload hash, source IP, timestamp, `event_type` if parseable, `envelope_id` if parseable.
- Do not process the event.

**Resolution**: Investigate whether the payload is:
1. A legitimate retry from Zoho Sign (re-sent with the same payload — HMAC will still fail, but the payload is valid). Zoho Sign's retry mechanism re-sends the same payload with the same HMAC; if Zoho Sign's HMAC is computed at send time, retries may carry a stale signature. Confirm with Zoho Sign's technical support.
2. A spoofing attempt — if confirmed, escalate to security team and review webhook endpoint exposure.
3. A clock skew between handler and Zoho Sign — check handler server time.

---

## FM-02: Hash mismatch on completed event

**Trigger**: SHA-256 of the downloaded signed PDF does not equal the stored `frozen_sha256`.

**Detection**: Webhook handler — hash verification step before Odoo write-back on `completed`.

**Immediate response**:
- Return HTTP 200 (event received; do not retry).
- Log CRITICAL error: `Hash mismatch on {envelope_id}. Odoo write-back ABORTED. frozen={frozen_sha256}, received={computed_hash}`.
- Do NOT write to Odoo.
- Do NOT send notifications.
- Alert human immediately (email + in-app).

**Resolution**:
1. Human downloads the signed PDF from Zoho Sign directly and manually verifies the hash.
2. If the hash genuinely differs: the document rendered or transmitted by Zoho Sign is not the document that was sent. Report to Zoho Sign. The legal status of the document is uncertain — escalate to Commercial Desk and legal counsel.
3. If the hash matches (handler bug): fix the handler, reprocess the event using the stored idempotency key (event_id + envelope_id) to avoid duplicate writes.

---

## FM-03: Envelope completed but record was not issue-ready

**Trigger**: `completed` event received, but the manifest shows `gates_passed != true` or `validate.py` would not exit 0, or there are open RESOLVE fields.

**Detection**: Webhook handler checks issue-ready conditions at `completed` event processing time.

**Immediate response**:
- Return HTTP 200.
- Log CRITICAL: `Completed event on non-issue-ready record: {envelope_id}`.
- Alert human.
- Do NOT write to Odoo Won stage.

**Resolution**: This is a G46 violation. The deal was sent for signature without passing the gate. Options:
1. If the commercial terms in the signed PDF are correct and the deal is commercially clean: human review, then manual Odoo write-back to Won with full documentation of the gate violation.
2. If the signed PDF contains wrong commercial terms: the amendment/void process applies. The signed contract is still binding — a correction envelope must be issued.

---

## FM-04: Duplicate completed event (idempotency failure)

**Trigger**: Second `completed` event for the same envelope_id arrives.

**Detection**: Audit log lookup — `envelope_id + event_id` pair already exists.

**Immediate response**:
- Return HTTP 200.
- Log: `Duplicate completed event ignored: {envelope_id}/{event_id}`.
- No Odoo write-back, no notifications.

**Resolution**: No action needed. If the first event's Odoo write-back failed (e.g., Odoo was down), reprocess the original event by manually inserting the event_id into the dead-letter queue with a "reprocess" flag.

---

## FM-05: Client signature alone moved to Won (G49 violation)

**Trigger**: A `signed` event (not `completed`) where the handler erroneously writes the Odoo record to Won on client signature alone.

**Detection**: Manual code review or audit log cross-check. This should be structurally impossible if the event handler only processes `completed` for Won. This is a code-level safeguard, not a runtime detection.

**Immediate response**: N/A (this is prevented in code).

**Prevention**: The `completed` event handler checks that both parties' signatures are present before writing Won. `signed_by_client` and `signed_by_sgc` are logged but do not trigger stage changes.

---

## FM-06: Odoo API key is invalid or expired

**Trigger**: Odoo External API returns 401 on any write operation.

**Detection**: Webhook handler — Odoo API response check after every write.

**Immediate response**:
- Odoo write fails; alert human immediately.
- Queue event for retry with exponential backoff (max 3 retries over 5 minutes).
- After 3 retries: dead-letter queue, alert human.

**Resolution**: Rotate the Odoo API key (User → Preferences → API Keys → Revoke old → Create new). Update the webhook handler's `ODOO_API_KEY` environment variable and restart the service.

---

## FM-07: Zoho Sign API is unavailable when downloading signed documents on completed

**Trigger**: Zoho Sign API returns non-2xx on download request, or times out.

**Detection**: Webhook handler — API response check after `completed` event.

**Immediate response**:
- Return HTTP 200 (event received).
- Log CRITICAL: `Failed to download signed PDF from Zoho Sign: {envelope_id}, status={http_status}`.
- Do NOT write Won to Odoo (cannot verify hash without the document).
- Alert human immediately.

**Resolution**:
1. Human downloads manually from Zoho Sign dashboard.
2. Human manually verifies hash and processes the Odoo write-back.
3. After resolution, update webhook handler's retry logic if the failure was transient.

---

## FM-08: Invoice creation fails on completed

**Trigger**: `completed` event processed, Odoo write succeeds, but `account.move` creation fails.

**Detection**: Webhook handler — invoice creation step.

**Immediate response**:
- Return HTTP 200.
- Log ERROR: `Invoice creation failed for {envelope_id}, Odoo opportunity updated but invoice missing`.
- Alert human (billing/finance).
- Opportunity is Won in Odoo but invoice is missing.

**Resolution**:
1. Human creates mobilisation invoice manually in Odoo.
2. Reference the envelope_id in the invoice notes.
3. Flag as draft pending payment confirmation.

---

## FM-09: Notification email fails to send

**Trigger**: SMTP or email API returns error on send.

**Detection**: Webhook handler — email send result check.

**Immediate response**:
- Log WARNING: `Notification send failed: template={template}, recipient={email}, error={error}`.
- Retry up to 3 times with 5-minute backoff.
- After 3 retries: skip, do not block the Odoo write-back.

**Resolution**:
1. Human sends the relevant notification manually.
2. Document in the audit log that the automated notification failed and was manually sent.

---

## FM-10: Envelope expires without a completion event being received

**Trigger**: No `completed` event within 30 days of send; `expired` event arrives from Zoho Sign (or is detected by a scheduled job checking envelope statuses).

**Detection**: Zoho Sign `expired` event, or scheduled job in the webhook handler.

**Immediate response**:
- Odoo opportunity moves to `stalled` stage.
- SDR notified.
- Activity created.

**Resolution**: SDR decides: issue a new envelope (reset validity window) or close the opportunity as lost. No new proposal needs to be drafted if the terms haven't changed — a new envelope can be issued from the same revision if the terms are identical.

---

## FM-11: Odoo opportunity not found for a valid event

**Trigger**: An event arrives with an `envelope_id` that does not match any `x_envelope_id` in Odoo.

**Detection**: Webhook handler — search returns zero results.

**Immediate response**:
- Return HTTP 200.
- Log ERROR: `Opportunity not found for envelope_id={envelope_id}, event_type={event_type}`.
- Alert human.

**Resolution**: Manually look up the opportunity in Odoo by the proposal reference. If the opportunity exists but `x_envelope_id` is not set (was not written on `sent`): this indicates the `sent` event failed to write. Set `x_envelope_id` manually in Odoo and reprocess the event.

---

## FM-12: SMS/OTP delivery failure to client signatory

**Trigger**: Zoho Sign reports OTP delivery failure or the client reports not receiving the signing link.

**Detection**: Zoho Sign dashboard alert or client complaint.

**Immediate response**: N/A — this is handled by Zoho Sign's own retry mechanism.

**Resolution**: SDR resends the envelope from the Zoho Sign dashboard or via the webhook handler's resend endpoint. The expired envelope is voided and a new one is issued. Both are logged in the audit trail.
