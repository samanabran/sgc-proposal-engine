# Send Protocol

## Overview

The send protocol governs how a frozen, issue-ready proposal revision is transmitted to the client for electronic signature. It covers preconditions, artifact preparation, envelope composition, expiry, reminders, and the Odoo opportunity record update.

This protocol applies only to **subscription (SUB)** model proposals. PRJ and RET models follow a separate signature process documented in their respective deal folders.

---

## Preconditions — issue-ready gate

An envelope may **only** be created when every condition below is true. Sending from a draft or from a record with open RESOLVE fields is a G46 violation and is blocked.

1. `gates_passed: true` in `manifest.yaml`
2. `validate.py` exits 0 (only check-14 entity-resolution blocker permitted)
3. QA checklist complete (`04-review/qa-checklist.md`)
4. Brand QA complete (`04-review/brand-qa-checklist.md`)
5. Zero open RESOLVE fields in the draft (confirmed by human reviewer sign-off)
6. Human review stage passed — human signed off on the draft

The webhook handler independently verifies these conditions before acting on any callback. An envelope reaching `completed` status against a non-issue-ready record is a failure-mode event (see `failure-modes.md`).

---

## Artifact preparation — freeze and hash

### Step 1 — Freeze

The artifact sent for signature is the **frozen PDF snapshot** of the issued revision, rendered from the approved draft at `03-draft/{PROPOSAL-REF}_RevN/` (or the equivalent `04-draft/` path in older revisions). The live HTML draft is never sent.

Freezing means:

- The HTML draft is rendered to PDF using the brand styles (`06-brand/styles/proposal.pdf.css` or `proposal-landscape.css` per `registry.yaml`)
- The frozen PDF receives a visual "ISSUE DATE: YYYY-MM-DD / ISSUED FOR SIGNATURE" footer on the cover page and on page 1, added at render time — not retroactively
- The frozen PDF is stored at `05-issued/{PROPOSAL-REF}_RevN/{PROPOSAL-REF}_RevN_Sent.pdf`

### Step 2 — SHA-256 hash

```bash
sha256sum 05-issued/{PROPOSAL-REF}_RevN/{PROPOSAL-REF}_RevN_Sent.pdf
```

The hash is recorded in `manifest.yaml`:

```yaml
issued_artifacts:
  - ref: "{PROPOSAL-REF}_RevN"
    sent_date: "YYYY-MM-DD"
    frozen_pdf_path: "05-issued/{PROPOSAL-REF}_RevN/{PROPOSAL-REF}_RevN_Sent.pdf"
    frozen_sha256: "abcd1234..."
```

The hash is what proves the signed copy and the issued copy are the same document. If the hash of the downloaded signed PDF does not reconcile to the stored hash, the webhook handler logs a critical error and alerts a human. The Odoo write-back does not proceed.

### Step 3 — Record in manifest

Update `manifest.yaml`:

```yaml
stage: sent
current_revision: "{PROPOSAL-REF}_RevN"
sent_date: "YYYY-MM-DD"
envelope_id: null       # filled by webhook handler on creation response
frozen_sha256: "..."
```

---

## Envelope composition

The envelope contains three documents, in this order:

1. **Proposal Rev N** — the frozen PDF (`{PROPOSAL-REF}_RevN_Sent.pdf`)
2. **Order Form** — the completed order form PDF (generated from `02-calc/pricing-worksheet.yaml` figures, brand-styled)
3. **MSA & SLA v2026.08** — the standard SGC TECH AI MSA and SLA document (brand-styled, dated v2026.08 per naming convention)

### Signature blocks

Each document contains two signature blocks:

**Client signatory block**
- Field: `signer_client_name` — full legal name of the person signing
- Field: `signer_client_title` — role/title
- Field: `signer_client_date` — auto-filled by provider on signature

**SGC authorised signatory block**
- Name: `Ali Asghar Teli Muhammad Iqbal Teli` (Company Manager, per trade license — `06-brand/entity/legal-identity.yaml`)
- Title: `Company Manager`
- Organisation: `Scholarix Global Consultants FZCO` / `SGC TECH AI`
- Date: auto-filled by provider

### Signer order

1. Client signatory signs first
2. SGC authorised signatory countersigns second

Both signatures are required before the envelope reaches `completed` status. Client signature alone is not sufficient to move the Odoo record to Won (G49).

---

## Envelope settings

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

---

## Send process

1. SDR or agent initiates send via the webhook handler's send endpoint, providing:
   - `proposal_ref` (e.g. `VGE-2026-SUB-01_Rev3`)
   - `client_signatory_name`, `client_signatory_email`, `client_signatory_title`
   - `client_signatory_phone` (required for OTP delivery)
   - `sgc_signatory_email` (`hello@sgctech.ai` — from `legal-identity.yaml`; this is the SGC countersigner's **recipient** email for the signing request)
2. Handler verifies issue-ready conditions from `manifest.yaml`
3. Handler creates the Zoho Sign envelope via API using the verified two-step contract below
4. Handler records the `request_id` (the `envelope_id`) returned by Zoho Sign in `manifest.yaml`
5. Handler calls Odoo External API: update opportunity stage to `Proposal Sent`, attach frozen PDF, set day-3 follow-up activity
6. Handler returns `envelope_id` and send confirmation to SDR

### Verified API contract (two-step send)

The contract below is the **verified working pattern** (reproduced from the Zoho Sign Node.js SDK request flow; confirmed by repeated live sends from the SGC account `hello@scholarixglobal.com`). Deviating from it is the known cause of errors `9015`, `9008`, `9106`, `9083`, `9039`, `9043`.

**Authentication** — every call carries:

```
Authorization: Zoho-oauthtoken <access_token>
```

The access token is short-lived. Obtain it from the refresh token (never store an access token long-term):

```
POST https://accounts.zoho.com/oauth/v2/token
  grant_type=refresh_token
  client_id=<ZOHO_SIGN_CLIENT_ID>
  client_secret=<ZOHO_SIGN_CLIENT_SECRET>
  refresh_token=<ZOHO_SIGN_REFRESH_TOKEN>
→ response["access_token"]  (memory-only; never written to disk or logged)
```

Credentials live in environment variables / a secrets manager only — `ZOHO_SIGN_CLIENT_ID`, `ZOHO_SIGN_CLIENT_SECRET`, `ZOHO_SIGN_REFRESH_TOKEN`, `ZOHO_SIGN_BASE_URL` (G52 — never committed).

**Step A — create request (draft envelope)**

```
POST {ZOHO_SIGN_BASE_URL}/api/v1/requests
Content-Type: multipart/form-data
```

Form parts (this is the critical format):

| Part | Value |
|---|---|
| `file` | Raw PDF bytes (one `file` part per document; frozen proposal PDF, Order Form, MSA & SLA) |
| `data` | **JSON string** — NOT a JSON body, NOT an array — see below |

The `data` part — note `requests` is an **object**, and it sits inside the multipart `data` field as a serialised string:

```json
{
  "requests": {
    "request_name": "{PROPOSAL-REF}_RevN",
    "is_sequential": true,
    "expiration_days": 30,
    "actions": [
      {
        "action_id": "client_sign",
        "recipient_email": "{client_signatory_email}",
        "recipient_name": "{client_signatory_name}",
        "recipient_phonenumber": "{client_signatory_phone}",
        "verify_recipient": true,
        "signing_order": 0
      },
      {
        "action_id": "sgc_sign",
        "recipient_email": "{sgc_signatory_email}",
        "recipient_name": "Ali Asghar Teli Muhammad Iqbal Teli",
        "signing_order": 1
      }
    ],
    "self_sign": false
  }
}
```

(`expiration_days: 30` realises the 30-day envelope expiry setting; `verify_recipient: true` realises OTP signer authentication; `is_sequential: true` + `signing_order` realise "client first, SGC countersigns second".)

**Step B — submit the request with field placement**

```
POST {ZOHO_SIGN_BASE_URL}/api/v1/requests/{request_id}/submit
```

Form fields: `action_id` and `document_id` (both from the Step A response), plus:

| Part | Value |
|---|---|
| `data` | JSON string with the per-action field placement — see below |

```json
{
  "requests": {
    "actions": [
      {
        "action_id": "client_sign",
        "fields": {
          "image_fields": [
            {
              "field_type_name": "Signature",
              "field_type_id": 604823000000000141,
              "page_no": 1,
              "x_coord": 480, "y_value": 700, "width": 120, "height": 60
            }
          ],
          "date_fields": [
            {
              "field_type_name": "Date",
              "field_type_id": 604823000000000151,
              "page_no": 1,
              "x_coord": 480, "y_value": 770, "width": 100, "height": 30
            }
          ]
        }
      },
      {
        "action_id": "sgc_sign",
        "fields": { "image_fields": [ /* Signature block for SGC */ ], "date_fields": [ /* Date */ ] }
      }
    ]
  }
}
```

Field coordinates are per-document `page_no`/`x_coord`/`y_value`/`width`/`height`. The verified field type IDs are: **Signature `604823000000000141`**, **Date `604823000000000151`** (queryable via the Zoho Sign field-types API). Coordinates for each document's two signature blocks are defined per proposal layout and stored with the envelope configuration.

The response carries `request_id` (used as the `envelope_id`), `request_status` (`inprogress` once sent), and per-action `action_id`s. The envelope is sent immediately on submit.

### Branded sender

Signing emails are intended to be sent **from the SGC Zoho Sign account `hello@scholarixglobal.com`**, not from Zoho's default `notifications@zohosign.com`. The sender domain `scholarixglobal.com` is **verified** in Zoho Sign (done: DKIM `42287223._domainkey.scholarixglobal.com` + SPF `v=spf1 include:zcsender.net ~all` in Cloudflare).

**Status 2026-08-04 — NOT yet working**: test signing emails still arrive with FROM `notifications@zohosign.com`. Domain verification alone is insufficient. To send from the branded address the Zoho Sign account must also have the **From address set to `hello@scholarixglobal.com` on the email template** (and the individual address confirmed where Zoho requires it — Zoho sends a confirmation link to `hello@scholarixglobal.com`). API-created envelopes use the account's **default** email template, so the branded template must be the default (or explicitly associated) for API sends to use the custom From. When the user confirms a branded FROM in a real test send, flip this status to verified and record the template configuration used.

**Go-live decision 2026-08-04 — NOT a gate**: branded FROM is a deliverability/trust improvement, not a validity requirement. An envelope sent from `notifications@zohosign.com` is equally enforceable — Zoho's audit certificate + the frozen→signed hash chain carry the evidential weight, not the sender domain. The honest risks are (a) a broker's spam filter eating the signing email and (b) the client not recognising the sender. Mitigation: proceed to go-live with the default sender; fix in **parallel** via Custom SMTP routing in the Zoho Sign admin (routes all Zoho Sign email through SGC's own mail server for branded FROM + deliverability) — or the paid custom-domain/white-label add-on if full sender-domain branding is wanted. Do not delay the Odoo integration for this.

---

## Expiry and voiding

If the envelope expires (30 days with no completion):

- The webhook handler receives an `expired` event
- Odoo opportunity is moved to a `stalled` stage with reason `envelope_expired`
- Activity is created for the SDR with a note that the proposal requires re-send or follow-up
- A new envelope may be created (the proposal validity window resets); the expired envelope is archived, not deleted

If the SDR voids the envelope before completion:

- The webhook handler receives a `voided` event
- Same Odoo handling as `expired` — record moves to `stalled`, SDR notified, activity created

If the client declines:

- The webhook handler receives a `declined` event
- Odoo opportunity moves to `lost` stage with reason from the provider (decline reason if supplied)
- SDR notified, no further action without human decision

---

## Odoo record on send

On `sent` event from provider, the webhook handler performs the following Odoo write-back:

```
Model: crm.lead (opportunity)
Fields updated:
  - x_envelope_id: <envelope_id from Zoho Sign>
  - x_sent_date: <sent timestamp>
  - x_frozen_pdf_hash: <stored frozen_sha256>
  - stage_id: <"Proposal Sent" stage ID>   # pipeline stage, not Won
  - description: append "Sent for signature: <envelope_id>"

Attachment created:
  - name: "{PROPOSAL-REF}_RevN_Sent.pdf"
  - type: binary
  - datas: <frozen PDF base64>
  - res_model: crm.lead
  - res_id: <opportunity ID>

Activity created (mail.activity):
  - activity_type_id: <follow-up type ID>
  - date_deadline: <sent_date + 3 calendar days>
  - user_id: <SDR owner of this opportunity>
  - note: "Day 3 reminder: {PROPOSAL-REF} sent for signature. Check signing status in Zoho Sign."
```

See `odoo-mapping.yaml` for the full Odoo field mapping and authentication setup.
