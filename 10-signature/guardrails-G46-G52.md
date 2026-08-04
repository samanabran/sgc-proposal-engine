# Guardrails G46–G52 — Signature Pipeline

These guardrails are specific to the signature and CRM pipeline (G46–G52).
They supplement the 41 commercial guardrails in `00-knowledge/commercial-rules/`.

---

## G46 — Frozen and hashed artifact only

**Rule**: Only a frozen, hashed, issue-ready artifact may be sent for signature.

An envelope may only be created when all of the following are true:
- `gates_passed: true` in `manifest.yaml`
- `validate.py` exits 0 (check-14 entity-resolution blocker permitted)
- QA checklist complete
- Brand QA complete
- Zero open RESOLVE fields in the draft
- Human review signed off

**Violation**: Sending from a draft or from a non-issue-ready record corrupts the pipeline and may bind SGC to a document that has not passed the gate check. If this occurs, the signed document is still legally binding — but the commercial terms in it must be verified against the gate-passing worksheet before the Odoo Won write-back proceeds.

**Enforcement**: The webhook handler verifies issue-ready conditions at `completed` event processing time. If the record was not issue-ready, the handler alerts a human and does not write Won.

---

## G47 — HMAC verification on every callback

**Rule**: Every inbound callback is HMAC-verified before parsing. Unverified payloads are dropped.

- Compute HMAC-SHA256 of the raw request body using `ZOHO_SIGN_WEBHOOK_SECRET`.
- Compare against `X-ZS-WEBHOOK-SIGNATURE` header (constant-time comparison), with the Unix timestamp from `X-ZS-WEBHOOK-TIMESTAMP` as the authoritative clock.
- Mismatch → return HTTP 401, log the attempt, do not parse or process.
- Timestamp skew > 5 minutes → return HTTP 401, log.

**Enforcement**: The webhook handler performs HMAC verification as the first operation before any body parsing or logging.

---

## G48 — Idempotent webhook handling

**Rule**: All webhook handling is idempotent by `envelope_id + event_id`.

A duplicate `signed` or `completed` event must not create a second Odoo record, send a second notification email, or create a duplicate invoice.

**Enforcement**:
1. Every event is checked against the append-only `signature_events` audit table before processing.
2. If `envelope_id + event_id` already exists: return HTTP 200 immediately, log duplicate, skip processing.
3. The `signature_events` table is append-only (no UPDATE, no DELETE).

---

## G49 — Won requires both parties

**Rule**: Won requires full execution by both parties — not client signature alone.

A client signature with no countersignature is not a contract SGC can rely on. Moving to Won on client signature alone will corrupt pipeline reporting and cash forecasting.

**Enforcement**:
- The Odoo Won write-back is triggered only by the `completed` event (both parties signed).
- `signed_by_client` and `signed_by_sgc` events are logged but do not change the Odoo stage.
- The Zoho Sign envelope is configured so that `completed` fires only when both parties have signed.

---

## G50 — Signed artifacts are immutable

**Rule**: Signed artifacts are immutable. Changes are amendments only. No overwrite, no re-render, no regeneration.

**Enforcement**:
- No code path in the webhook handler deletes or overwrites a stored signed PDF.
- Delete rights are restricted to a named SGC admin with Commercial Desk sign-off.
- Any change to a signed contract requires a new amendment envelope, not an edit to the stored artifact.
- A `deletion_log` table records every deletion with user, date, reason, and approving authority.

---

## G51 — Mobilisation invoice as draft

**Rule**: The mobilisation invoice is created as draft and posted by a human. No auto-post.

**Enforcement**:
- The webhook handler creates `account.move` with `state: "draft"`.
- No code path sets `state: "posted"` on the mobilisation invoice.
- The notification to the SGC signatory explicitly warns: "Mobilisation invoice drafted as DRAFT. DO NOT POST until payment is confirmed."
- The notification to the SDR reinforces: "(drafted — do not post yet)" next to the mobilisation amount.

---

## G52 — No secrets committed

**Rule**: No credential, key, or secret is ever committed to the repository.

**Enforcement**:
- Credentials are stored in environment variables or a secret manager (AWS Secrets Manager, HashiCorp Vault, or equivalent).
- `odoo-mapping.yaml` contains field mappings and API endpoint URLs only — no secrets.
- The webhook handler reads secrets from environment variables at startup.
- No `.env` file is committed or exists in the repository.
- The repository contains no Zoho Sign API keys, Odoo API keys, or bearer tokens.
- `validate.py` check #17 (evidence checklist) and check #18 (forbidden phrases) do not cover secrets — the enforcement is a development practice, not a code check.

---

## Relationship to commercial gates

G46–G52 are pipeline integrity guardrails, not commercial guardrails. They do not replace the 41 commercial gates in `00-knowledge/commercial-rules/`. A deal that passes all 41 commercial gates and all 7 signature guardrails is ready to issue and execute.

---

## Acceptance criteria summary

| Guardrail | Acceptance criterion |
|---|---|
| G46 | Webhook handler rejects `completed` event on a record where manifest shows `gates_passed != true` |
| G47 | A crafted payload without a valid HMAC returns HTTP 401 and logs the attempt |
| G48 | Duplicate `completed` event with the same `envelope_id + event_id` produces exactly one Odoo write and one notification email |
| G49 | `signed_by_client` event does not move Odoo stage to Won; only `completed` does |
| G50 | No code path exists that overwrites or deletes a stored signed PDF |
| G51 | Mobilisation `account.move` is created with `state: "draft"`, never `posted` |
| G52 | No secret, API key, or credential appears in any tracked file in the repository (verified by pre-commit hook or CI check) |
