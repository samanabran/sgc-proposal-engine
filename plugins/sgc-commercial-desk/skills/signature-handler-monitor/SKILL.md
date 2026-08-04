---
name: signature-handler-monitor
description: Desk-only monitoring skill. Watches the webhook handler's signature pipeline, alerts on G46–G52 anomalies, and reconciles `pending-odoo-writes.yaml` when sgc_crm_fields is finally deployed.
version: 1.0.0
owner: Commercial Desk + IT
position: desk-side; continuous
---

# signature-handler-monitor

The desk's monitoring skill for the signature pipeline. The handler
itself is in the SRE repo (not in the plugin); this skill reads
handler logs and Odoo state, and reconciles when the sgc_crm_fields
module is finally deployed.

## When to use

- Trigger phrases: "monitor the signature pipeline", "check the handler logs", "reconcile pending Odoo writes", "is sgc_crm_fields deployed", "what's the envelope status", "alert on a G46 violation", "G47 HMAC failure log", "G48 idempotency check".

This skill is the desk's view of the signature pipeline. The SDR
plugin never invokes it.

## Bundled knowledge files to read, in order

1. `knowledge/10-signature/send-protocol.md` (full)
2. `knowledge/10-signature/odoo-mapping.yaml` (full)
3. `knowledge/10-signature/guardrails-G46-G52.md` (full)
4. `knowledge/10-signature/failure-modes.md` (full)
5. `knowledge/10-signature/audit-retention.md` (full)
6. `knowledge/10-signature/webhook-spec.md` (full)
7. The handler's logs (read over a Den-managed MCP connection to the handler's logging endpoint)
8. The Odoo External API (for runtime `ir.model.fields.x_envelope_id` lookup)
9. `<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/pending-odoo-writes.yaml` (when sgc_crm_fields is not deployed)

## What it writes, where

- `plugins/sgc-commercial-desk/knowledge/monitoring/signature-pipeline-log.md` — append-only log of every monitoring event
- `<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/pending-odoo-writes.yaml` — re-issued as a normal Odoo write-back when sgc_crm_fields is deployed
- A daily digest to the desk's `04-review/qa-checklist.md` mirror, summarising envelope state across active deals

## What it monitors

- **G46 — frozen-and-hashed artifact only**: any envelope that reaches `completed` against a non-issue-ready record. Alert the approver, do not write Won.
- **G47 — HMAC verification**: any unverified callback. Log the attempt, alert the desk, do not parse the payload.
- **G48 — idempotency**: any duplicate `envelope_id + event_id` for `signed` or `completed`. Verify the audit log, ensure exactly one Odoo write and one notification email.
- **G49 — Won requires both parties**: any `signed_by_client` event that the handler tried to move to Won. Refuse; the handler must not write Won on client signature alone.
- **G50 — signed artifacts are immutable**: any code path that overwrites or deletes a stored signed PDF. Alert the desk; the handler is in violation.
- **G51 — mobilisation invoice as draft**: any `account.move` written with `state: "posted"`. The handler must create drafts only; the approver posts after payment confirmation.
- **G52 — no secrets committed**: any secret, key, or credential in a tracked file. Run `plugins/sgc-proposal-engine/ci/secrets-scan.sh` on every handler commit.

## Runtime detection of sgc_crm_fields

When this skill is asked "is `sgc_crm_fields` deployed?", it performs the runtime lookup:

```
1. POST https://<odoo>/json/2/call_kw with:
   - model: ir.model.fields
   - method: search_count
   - args: [[["name", "=", "x_envelope_id"], ["model", "=", "crm.lead"]]]
2. If count > 0: deployed; the handler can do the Odoo write-back natively.
3. If count == 0: not deployed; the handler appends to pending-odoo-writes.yaml.
```

This is the same lookup the `signature-dispatch` skill does; the desk's
monitoring view is the canonical answer to "is the module deployed
right now?".

## Reconciliation

When `sgc_crm_fields` is deployed, this skill:

1. Iterates `pending-odoo-writes.yaml` across all active client folders.
2. For each entry: replays the Odoo write-back per `odoo-mapping.yaml`.
3. Marks the entry as `reconciled: true` with the timestamp.
4. After successful replay, deletes the entry from `pending-odoo-writes.yaml`.
5. Notifies the SDR of the reconciliation (the original "Day 3 reminder" activity may have already been created manually).

## What it refuses

- **Bypassing HMAC verification** — refuses to read a payload without HMAC verification. Cite G47.
- **Allowing Won on client signature alone** — refuses to write Won on `signed_by_client`. Cite G49.
- **Posting a draft invoice** — refuses to set `account.move.state = "posted"`. The handler creates drafts; the approver posts. Cite G51.
- **Overwriting a signed PDF** — refuses any code path that overwrites a stored signed PDF. Cite G50.
- **Logging a secret** — refuses to log any Zoho/Odoo/webhook secret. Cite G52.

## Escalation path

- **G47 HMAC failure** — alert the desk and the approver immediately. The webhook is potentially compromised; pause all signature pipeline activity until the desk's IT lead investigates.
- **G48 idempotency violation** — alert the desk; investigate the handler's audit log.
- **G49 violation (Won on client signature alone)** — alert the approver; the Odoo stage must be rolled back to `Proposal Sent` until the SGC countersignature arrives.
- **G50 violation (signed PDF overwrite)** — alert the approver and the desk's IT lead; the handler is in violation of the immutability rule.
- **G51 violation (posted invoice)** — alert the approver; the invoice must be reverted to draft.
- **G52 violation (secret in tracked file)** — alert the desk and IT lead immediately; the secret must be rotated.

## What this skill does NOT do

- It does not write to the handler. The handler is in the SRE repo.
- It does not invoke the SDR plugin's `signature-dispatch`. The SDR plugin's skill does that, with the approver's approval record.
- It does not change the canonical Zoho two-step flow. `send-protocol.md` is desk-shipped and verbatim.
- It does not push the SDR plugin. `PUBLISHING.md` describes the push mechanism.

## Acceptance check (self-test)

At any point, this skill must be able to answer YES to each:

1. The handler is running with HMAC verification enabled (G47)?
2. The handler is appending to `signature_events` before processing (G48)?
3. The handler never sets `account.move.state = "posted"` for mobilisation invoices (G51)?
4. The handler reads `ZOHO_SIGN_WEBHOOK_SECRET` from environment, never from disk (G52)?
5. The current `send-protocol.md` status line for branded FROM is read on every send (G-not-a-block, but reported)?
6. `pending-odoo-writes.yaml` across all active deals is current (no entries older than 7 days without reconciliation)?
