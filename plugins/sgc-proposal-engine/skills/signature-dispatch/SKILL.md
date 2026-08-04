---
name: signature-dispatch
description: Step 13 of the SDR pipeline. Calls Zoho Sign to send the envelope. Refuses to send without a valid approval record (G53). Degrades gracefully if the Odoo sgc_crm_fields module is not deployed.
version: 1.0.0
owner: signature-handler (this skill orchestrates; the handler lives in the desk SRE repo and is NOT bundled)
position: 13
---

# signature-dispatch

The signature-dispatch stage. The handler is not in the plugin — only
the orchestrating skill is. The handler lives in the SRE repo and is
called over a Den-managed MCP connection.

## When to use

- Trigger phrases: "send for signature", "create the envelope", "dispatch to Zoho Sign", "send the proposal", "request signatures".

If the approval record is missing or stale, refuse. This is the
single most-enforced refusal in the pipeline (G53).

## Position in step gate

Step 13. The fixed sequence:

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

This skill **refuses to run** unless `05-approval/approval-record.yaml` exists with `decision: approved` and a valid `approved_artifact_sha256` matching the on-disk PDF.

## Bundled knowledge files to read, in order

1. `knowledge/guardrails-g42-g53.yaml` (mirror) — G53 in particular
2. `knowledge/send-protocol.md` — the two-step Zoho API flow
3. `knowledge/odoo-mapping.yaml` — the Odoo write-back contract
4. `knowledge/commercial-rules/protection-guardrails.md` — G46–G52 cross-references

The `handler/` directory under the original `10-signature/` is **not
bundled**. It is the runtime SRE artifact, lives in a separate
credentials-bounded repo, and is invoked over MCP. No credential in
this plugin.

## What it writes, where

- Updates `manifest.yaml: stage` to `sent`; records `envelope_id`, `sent_date`, `frozen_sha256` (the binding hash)
- Appends an entry to `05-approval/pending-odoo-writes.yaml` if the Odoo sgc_crm_fields module is not deployed (graceful degradation; see below)
- No client-facing files. The handler writes `04-issued/<PROPOSAL-REF>_RevN/<PROPOSAL-REF>_RevN_Signed.pdf` and `_AuditCertificate.pdf` to Odoo `ir.attachment` on `completed`.

## Preflight — refuses to proceed if any of:

- No valid `approval-record.yaml` for this artifact (G53)
- `approved_artifact_sha256` ≠ SHA-256 of PDF on disk (G53)
- Artifact not in `04-issued/` (G53)
- `expires_at` is in the past (G53)
- `decision: rejected` (G53)
- `decision: conditional` with `conditions: [...]` that are unmet (G53)
- `approver.name` is not exactly `Ali Asghar Teli Muhammad Iqbal Teli` (G53)
- Any Tier 1 client `RESOLVE:` is still open (G52 + `sufficiency-rules.yaml: tier_1`)

Each preflight check is reported individually with its pass/fail status.

## Envelope composition

The envelope contains three documents, in this order:

1. **Proposal Rev N** — the frozen PDF (`<PROPOSAL-REF>_RevN_Sent.pdf`)
2. **Order Form** — the completed order form PDF, brand-styled
3. **MSA & SLA v2026.08** — the standard SGC TECH AI MSA and SLA document, brand-styled

Both signatures are required (G49). The client signs first, SGC
countersigns second.

### Envelope settings

| Parameter | Value |
|---|---|
| Expiry | 30 days from send date |
| Reminder — first | Day 3 after send, if not viewed |
| Reminder — second | Day 7, if not signed |
| Reminder — third | Day 14, if not signed |
| Signer authentication | OTP (one-time password) sent to signer's email |
| Signing order | Client first, then SGC |
| Language | English |
| Completion event | Fired only when both parties have signed |

## Two-step Zoho API flow

Follow `knowledge/send-protocol.md` exactly. The handler is the writer;
this skill orchestrates the call. The contract is the verified
working pattern reproduced from the Zoho Sign Node.js SDK request flow;
deviating from it produces errors `9015`, `9008`, `9106`, `9083`,
`9039`, `9043`.

Authentication: every call carries `Authorization: Zoho-oauthtoken <access_token>`. The access token is short-lived; the handler obtains it from the refresh token, never stores long-term. Credentials live in the handler's secret manager, never in the plugin, never in `manifest.yaml`, never logged.

Step A: `POST {ZOHO_SIGN_BASE_URL}/api/v1/requests` with `Content-Type: multipart/form-data`. The `data` part is a **JSON string** (not a body, not an array) with the `requests` object (note: object, not array), `actions` array, `is_sequential: true`, `expiration_days: 30`, `verify_recipient: true`, `signing_order: 0` and `1`.

Step B: `POST {ZOHO_SIGN_BASE_URL}/api/v1/requests/{request_id}/submit` with the per-action field placement. Field-type IDs: **Signature `604823000000000141`**, **Date `604823000000000151`**. Coordinates per proposal layout, per `send-protocol.md:217-241`.

The response carries `request_id` (used as the `envelope_id`), `request_status`, per-action `action_id`s. Record `envelope_id` in `manifest.yaml`.

## Unbranded-FROM warning (not a block)

Read `send-protocol.md:248-254` "Branded sender" section. If the status is `NOT working`, log the warning on every send:

> Sent from default sender `notifications@zohosign.com` — branded FROM unverified. Deliverability/recognition risk, not a validity risk.

This is a deliverability warning, not a G53 block. The envelope is sent; the warning is in `manifest.yaml: sent_brand_status: not_working`. The handler logs the warning to the SDR's session.

## Signatory — named approver vs actual signer

Per `06-brand/entity/legal-identity.yaml: contact`:

- **Named approver** (per the trade licence, Dubai Integrated Economic Zones Authority, IFZA, Licence No. 45160): `Ali Asghar Teli Muhammad Iqbal Teli`, Company Manager. This is the legal signatory whose authority binds the entity.
- **Actual signer** (acting on behalf of the named approver): `Renbran Anthony Madelo`, Founder & CEO. Renbran Madelo signs in behalf of the named Company Manager per documented authority.

The envelope's `recipient_name` for the SGC action is **`Renbran Anthony Madelo`** (the actual signer who countersigns). The Zoho Sign audit certificate records `Renbran Anthony Madelo, signing in behalf of Ali Asghar Teli Muhammad Iqbal Teli, Company Manager`. The Odoo `crm.lead.x_signing_actor_sgc` field records the actual signer (`Renbran Anthony Madelo`); a separate note field records the named approver.

The G53 preflight's `approver.name` check matches the **actual signer** in the Zoho Sign payload, not the named approver. G53 enforces that the actual signer is uniquely identified and that their authority is documented. It does not enforce that the actual signer is the named approver — that relationship is documented separately in the MSA and the Order Form.

## Odoo write-back with graceful degradation

The handler calls Odoo on `sent` and `completed` per
`knowledge/odoo-mapping.yaml`. The `sgc_crm_fields` module provides
the 17 custom fields on `crm.lead` listed below. The module is a
reference skeleton at `10-signature/sgc-crm-fields/`; install it
per the steps in `PUBLISHING.md` §"sgc_crm_fields install".

### Fields (17 + 1 relation)

```
x_envelope_id            Char       Zoho Sign envelope ID
x_signed_pdf_hash        Char       SHA-256 of signed PDF
x_frozen_pdf_hash        Char       SHA-256 of frozen sent PDF
x_sent_date              Datetime   Envelope sent at
x_completed_date         Datetime   Fully executed at
x_signing_actor_client   Char       Client signatory
x_signing_actor_sgc      Char       SGC signatory
x_decline_reason         Text       Decline reason
x_contract_term_months   Integer    Initial term
x_subscription_fee       Float      Monthly total (AED)
x_platform_fee           Float      Platform portion (AED)
x_recovery_fee           Float      Recovery portion (AED)
x_mobilisation_amount    Float      One-off mobilisation (AED)
x_cadence                Selection  quarterly_in_advance | monthly_in_advance | annual_in_advance
x_edition                Selection  community | enterprise
x_upgrade_policy         Text       Upgrade policy text
x_kickoff_date           Date       Target kickoff
x_invoice_id             Many2one   Draft mobilisation invoice (G51)
```

### Runtime detection (concrete call)

The skill performs an `ir.model.fields` lookup via the Odoo External
API. The literal call:

```http
POST https://<odoo>/json/2/call_kw
Headers: Authorization: Bearer <api_key>
Body: {
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute_kw",
    "args": [
      "<odoo_database>",
      2,                  # user-id (or use 0 for system)
      "<api_key>",
      "ir.model.fields",
      "search_count",
      [[["name", "=", "x_envelope_id"], ["model", "=", "crm.lead"]]]
    ]
  },
  "id": 1
}
```

Result handling:

- `count > 0`: sgc_crm_fields is deployed. The handler performs the native Odoo write-back per `odoo-mapping.yaml`.
- `count == 0` or error: not deployed. The handler appends to `pending-odoo-writes.yaml` (no failure).

### pending-odoo-writes.yaml schema

When the module is not deployed, the handler appends the intended
writes to `<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/pending-odoo-writes.yaml`:

```yaml
# Append-only log. The desk-side signature-handler-monitor skill
# reconciles when sgc_crm_fields is finally deployed.
- timestamp: 2026-08-04T13:00:00Z
  proposal_ref: "<PROPOSAL-REF>_RevN"
  envelope_id: "<envelope_id>"
  event: sent | completed | declined | expired | voided
  intended_writes:
    - model: crm.lead
      operation: search+write
      search_by: [x_envelope_id, name]
      fields:
        x_envelope_id: "<envelope_id>"
        x_frozen_pdf_hash: "<frozen_sha256>"
        x_sent_date: "<sent_timestamp>"
        x_completed_date: "<completed_timestamp>"
        x_signing_actor_client: "<client_signatory_name>"
        x_signing_actor_sgc: "Ali Asghar Teli Muhammad Iqbal Teli"
        x_decline_reason: "<reason>"
        x_contract_term_months: 24
        x_subscription_fee: 1750.0
        x_platform_fee: 1100.0
        x_recovery_fee: 650.0
        x_mobilisation_amount: 15000.0
        x_cadence: quarterly_in_advance
        x_edition: community
        x_upgrade_policy: "<verbatim from editions.yaml>"
        x_kickoff_date: "2026-09-01"
    - model: ir.attachment
      operation: create
      fields:
        name: "<PROPOSAL-REF>_RevN_Sent.pdf"
        res_model: crm.lead
        res_id: <opportunity_id>
        mimetype: application/pdf
        datas: <base64 of frozen PDF>
    - model: mail.activity
      operation: create
      fields:
        activity_type_id: <Follow-up type ID>
        date_deadline: "<sent_date + 3 calendar days>"
        user_id: <SDR user ID>
        note: "Day 3 reminder: <PROPOSAL-REF> sent for signature."
        res_model: crm.lead
        res_id: <opportunity_id>
  reconciliation:
    status: pending | reconciled
    reconciled_at: null
    reconciled_by: null
    notes: ""
  reason: "sgc_crm_fields not deployed; ir.model.fields.x_envelope_id not found on crm.lead"
  remediation: "Install sgc_crm_fields module. See PUBLISHING.md §'sgc_crm_fields install'."
```

The desk-side `signature-handler-monitor` skill iterates this file
across all active client folders when sgc_crm_fields is deployed,
replays the writes, and marks entries as `reconciled: true`.

- The SDR is notified (the desk-side `signature-handler-monitor` skill alerts the desk).
- The deal is **not blocked** — the Zoho Sign envelope is in flight.

If the Odoo call fails for any other reason (auth, network, etc.),
the handler logs the failure, retries per the Odoo write-back's
exponential-backoff, and appends to `pending-odoo-writes.yaml` on
final failure.

## What it refuses

- **No approval record** — refuses to call the Zoho Sign API. Cite G53.
- **Stale approval** (hash mismatch, expired, rejected, conditional-with-unmet-conditions, wrong approver) — same.
- **Artifact not in `04-issued/`** — same.
- **Three or more documents in the envelope** — refuses; the envelope must contain exactly the three documents above in the stated order.
- **SGC countersign before client sign** — refuses to configure the envelope that way. G49.
- **No OTP on the client signatory** — refuses to disable `verify_recipient: true`. G47 (HMAC), G49 (Won).
- **Mobilsation invoice posted by the handler** — refuses to set `state: "posted"` on the `account.move`. The invoice is created draft per G51.

## Escalation path

- **G53 preflight failure** — `RESOLVE:` and route back to `approval-gate` (or to the approver, depending on the failure).
- **Odoo sgc_crm_fields not deployed** — `pending-odoo-writes.yaml` is appended; the SDR or desk performs manual reconciliation once the module is installed. The deal is not blocked.
- **Branded FROM unverified** — log the warning; do not delay. (See send-protocol.md:254.)
- **Zoho API error 9015/9008/9106/9083/9039/9043** — the call deviated from the verified two-step flow. Stop and re-read `send-protocol.md`. The handler must not improvise the request shape.
- **Webhook handler credentials missing** — refuse to send. The handler's secret manager must be configured before the skill runs. The SDR cannot proceed without the handler.

## What this skill does NOT do

- It does not bundle the handler. `10-signature/handler/*` is in the SRE repo.
- It does not commit any credential. The handler reads from the secret manager at startup; the skill only invokes the handler over MCP.
- It does not move the artifact. `04-issued/` is the source; the handler does not move anything.
- It does not draft a covering email. The covering email is drafted by the SDR after the envelope is sent, using the template in `01-templates/comms/`.

## Acceptance check (self-test)

Before declaring the deal `envelope-sent`, the skill must be able to answer YES to each:

1. Approval record exists and is unexpired, with `decision: approved` and `approver.name == "Ali Asghar Teli Muhammad Iqbal Teli"`?
2. The on-disk PDF SHA-256 equals `approved_artifact_sha256`?
3. The envelope contains exactly three documents in the stated order: Proposal Rev N, Order Form, MSA & SLA v2026.08?
4. The envelope is configured with client-first signing, OTP, 30-day expiry, reminders day 3/7/14?
5. The unbranded-FROM warning was logged if applicable?
6. The Odoo write-back was either performed or appended to `pending-odoo-writes.yaml`?
