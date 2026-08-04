# Runbook — Issue VGE-2026-SUB-01 Rev3 for Signature

**Proposal ref:** `VGE-2026-SUB-01`  ·  **Revision:** `Rev3`  ·  **Date prepared:** 2026-08-04
**Pipeline status:** all 41 v2 gates recorded pass; `validate.py` exit 0; manifest `gates_passed: true`.
**Frozen artefact:** `02-clients/VGE-vongeyern-realestate/04-draft/VGE-2026-SUB-01_Rev3_Proposal.pdf` (≈466 KB, 10 pp).
**This runbook is a human procedure.** The engine does not sign, send, or post on its own. Do not skip steps.

---

## 0. Pre-flight (read all of this before doing anything)

| # | Check | Pass criterion |
|---|---|---|
| 0.1 | `python 05-ops/validate.py 02-clients/VGE-vongeyern-realestate/` | exit 0, `RESULT: clean` |
| 0.2 | `02-clients/VGE-vongeyern-realestate/manifest.yaml` ⇒ `gates_passed` | `true` |
| 0.3 | `manifest.yaml` ⇒ `current_revision` | `VGE-2026-SUB-01_Rev3` |
| 0.4 | `manifest.yaml` ⇒ `walkaway_card_produced` | `true` |
| 0.5 | `02-clients/VGE-vongeyern-realestate/02-calc/gate-report.md` line 76 | **signed** by reviewer (date filled) |
| 0.6 | `02-clients/VGE-vongeyern-realestate/04-draft/VGE-2026-SUB-01_Rev3_Proposal.pdf` exists and is the latest | file present, modified today |
| 0.7 | `00-knowledge/PRECEDENCE.md` confirms the client is REAL (not a draft/exercise) — see clause-library ¶ G14 | confirmed in writing |
| 0.8 | Client registered address — informal line known (`Waterfront Living — 5 min to the Dubai Islands beach`) | Default = Option 2 from §2: Ms. Nadja types the registered address on her signing page before signing. Do not delay issuance. |

If **any** check fails → stop. Do not send. Re-run the pipeline before issuing.

---

## 1. Sign the gate report (G29 evidence completeness)

Open `02-clients/VGE-vongeyern-realestate/02-calc/gate-report.md`, line 76:

```
Reviewer: _______________  Date: _______________
```

Write the **Commercial Desk reviewer's** full name and the date. This is the only piece of evidence that converts the gate report from "mechanism passes" to "SGC attests". Commit the change.

---

## 2. Confirm the authorised signer chain (G6 — only registered signatory may countersign for SGC)

Read `06-brand/entity/legal-identity.yaml`. As of 2026-08-04 the only registered SGC authorised signatory is:

| Role | Name | Email | Phone |
|---|---|---|---|
| Company Manager, authorised signatory | Ali Asgher Teli Muhammad Iqbal Teli | `hello@sgctech.ai` | `+971 52 198 5231` |

`john@sgctech.ai` and `bran@sgctech.ai` are **not** on this registry as of 2026-08-04 and **cannot countersign for SGC**.

Decide (in writing, on this runbook or in `04-review/reviewer-notes.md`):

| Decision | Default value |
|---|---|
| SGC countersigner (action_id `sgc_sign`) | `hello@sgctech.ai` — `Ali Asgher Teli Muhammad Iqbal Teli` |
| Client recipient (action_id `client_sign`) | **Ms. Nadja** · Owner / Manager · `info@vongeyern.de` · `+971585518040` (phone required for OTP per `send-protocol.md`) |
| CC on envelope | **omit** (no internal CC) — Path C1, direct to client |

> **⚠️ Registered address — known risk (decision 2026-08-04).** The client-supplied location is `Waterfront Living — 5 min to the Dubai Islands beach`. This reads as a marketing description, not a registered address on the Dubai trade licence. The Order Form will carry the literal string the client provided. Two acceptable resolutions:
>
> 1. **Before issue** — Commercial Desk obtains the trade-licence registered address from Ms. Nadja, regenerates the Order Form, re-hashes, and re-issues as `Rev4`.
> 2. **At signing** — Ms. Nadja is asked to type the registered address into the Order Form's address field on her signing page before she signs. The frozen PDF goes out with `Waterfront Living — 5 min to the Dubai Islands beach`; her signed copy carries the real registered address. The hash chain still holds (signed PDF ≠ frozen, but envelope completion triggers Zoho Sign's own audit cert + a fresh `x_signed_pdf_hash`).
>
> Default for this issue: **option 2**. Do not delay issuance over an address line that can be corrected at signing time.

If you intend to register `john@sgctech.ai` or `bran@sgctech.ai` as an additional signatory first, do that update to `06-brand/entity/legal-identity.yaml` through the **Commercial Desk** channel — agents do not edit `06-brand/`.

---

## 3. Render the frozen PDF with the issue footer

The PDF in `04-draft/` is the **draft**. The frozen PDF carries an issue footer and is the artefact of record.

Run, in PowerShell, from `C:\sgc_proposal_engine`:

```powershell
cd "C:\sgc_proposal_engine\02-clients\VGE-vongeyern-realestate\04-draft"
python render_pdf.py `
  --in  VGE-2026-SUB-01_Rev3_Proposal.html `
  --out VGE-2026-SUB-01_Rev3_Sent.pdf `
  --issue-date (Get-Date -Format "yyyy-MM-dd") `
  --mark "ISSUED FOR SIGNATURE"
```

The rendered `VGE-2026-SUB-01_Rev3_Sent.pdf` lives in the same folder for now; you will copy it into `05-issued/VGE-2026-SUB-01_Rev3/` immediately after `validate.py` accepts it (do **not** edit `05-issued/` after that copy — see §7).

Compute the SHA-256:

```powershell
Get-FileHash .\VGE-2026-SUB-01_Rev3_Sent.pdf -Algorithm SHA256
```

Copy the resulting hex digest. It must match the value you write into `manifest.yaml.issued_artifacts[0].frozen_sha256`. A mismatch in any later hash check will abort the Odoo write-back (CRITICAL alert, no Odoo row, no emails).

---

## 4. Compose the envelope

Three documents go into the envelope, in this order:

| # | Document | Source |
|---|---|---|
| 1 | Rev3 Proposal (frozen) | the `_Sent.pdf` you just rendered in §3 |
| 2 | Order Form | rendered from `02-calc/pricing-worksheet.yaml` — a **draft** companion script lives in `04-draft/`; confirm pricing figures match §3 of the proposal before sending |
| 3 | MSA & SLA v2026.08 | template at `08-contracts/` (Commercial Desk controlled); copy into `02-clients/VGE-vongeyern-realestate/05-issued/VGE-2026-SUB-01_Rev3/` for the issue and brand-style before upload |

Signers, in order (sequential is required so the SGC countersignature honours G49):

| Order | Role | Email | Name | Auth |
|---|---|---|---|---|
| 0 | Client (signatory) | from §2 | from §2 | OTP by phone |
| 1 | SGC countersignatory | `hello@sgctech.ai` | `Ali Asgher Teli Muhammad Iqbal Teli` | email OTP |

Envelope settings:

| Setting | Value |
|---|---|
| `expiration_days` | 30 |
| `is_sequential` | `true` |
| Reminders | day 3, day 7, day 14 |
| Signer authentication | email OTP |
| Language | English |
| Completion criterion | both parties signed |

---

## 5. Send via the verified 2-step Zoho Sign API

> **G52 — Never commit credentials.** All values below are read from the environment or your local `zoho_test_branding.py`. Do not paste real Client ID / Client Secret / Refresh Token into this runbook, into chat, or into any file in the repo.

### 5.1 — Acquire an access token

```powershell
$ZOHO_BASE   = "https://accounts.zoho.com"
$TOKEN_URL   = "$ZOHO_BASE/oauth/v2/token"
$tokens = Invoke-RestMethod -Method POST -Uri $TOKEN_URL `
  -Body @{
    grant_type    = "refresh_token"
    client_id     = $env:ZOHO_SIGN_CLIENT_ID
    client_secret = $env:ZOHO_SIGN_CLIENT_SECRET
    refresh_token = $env:ZOHO_SIGN_REFRESH_TOKEN
  }
$access_token = $tokens.access_token        # never logged
```

If `$tokens.access_token` is empty, stop — refresh failed, do not retry without investigating.

### 5.2 — Step A: create the request (multipart/form-data)

`requests` is an **OBJECT inside a JSON string in the `data` field**, not an array, not a JSON body.

```powershell
$API = "https://sign.zoho.com/api/v1"

$requests_obj = @{
  request_name    = "VGE-2026-SUB-01 Rev3"
  is_sequential   = $true
  expiration_days = 30
  self_sign       = $false
  actions = @(
    @{
      action_id           = "client_sign"
      recipient_email     = "info@vongeyern.de"              # Ms. Nadja · Owner / Manager
      recipient_name      = "Ms. Nadja"                      # title held at signing per §2
      recipient_phonenumber = "+971585518040"                # E.164, required for OTP
      verify_recipient    = $true
      signing_order       = 0
    },
    @{
      action_id           = "sgc_sign"
      recipient_email     = "hello@sgctech.ai"
      recipient_name      = "Ali Asgher Teli Muhammad Iqbal Teli"
      signing_order       = 1
    }
  )
} | ConvertTo-Json -Depth 8 -Compress

$create = Invoke-RestMethod -Method POST -Uri "$API/requests" `
  -Headers @{ Authorization = "Zoho-oauthtoken $access_token" } `
  -Form @{
    file = Get-Item '.\VGE-2026-SUB-01_Rev3_Sent.pdf'              # × 3, one per document
    file = Get-Item '.\VGE-2026-SUB-01_Rev3_OrderForm.pdf'         # render first if not present
    file = Get-Item '.\VGE-2026-SUB-01_Rev3_MSA_SLA_v2026.08.pdf'  # render first if not present
    data = $requests_obj
  }

$request_id  = $create.requests.request_id
$document_id = $create.requests.document_ids[0].document_id
$action_ids  = $create.requests.actions | ForEach-Object action_id
```

Common error codes from Zoho Sign and what they actually mean (verified pattern):

| Code | Real cause | Fix |
|---|---|---|
| 9015 | `requests` sent as JSON array, not object | ensure `data` is a JSON string whose top-level is an **object** with one `requests` member |
| 9008 | `data` field sent as JSON body instead of multipart part | must be multipart/form-data; `data` is a form part with a JSON string value |
| 9106 | `file` filename missing/duplicate | use distinct filenames per part |
| 9083 / 9039 | expired/invalid token | re-run §5.1 |
| 9043 | missing `recipient_phonenumber` for OTP | add it |

### 5.3 — Step B: submit with placement fields

Field type IDs are **fixed in Zoho Sign's data dictionary** — never invent:

| Field | `field_type_id` | `field_type_name` |
|---|---|---|
| Signature | `604823000000000141` | `Signature` |
| Date | `604823000000000151` | `Date` |

```powershell
$fields = @{
  requests = @{
    actions = @(
      @{
        action_id = $action_ids[0]   # client_sign
        action_type = "SIGN"
        fields = @{
          image_fields = @(
            @{
              field_type_name = "Signature"
              field_type_id   = "604823000000000141"
              page_no   = 12                        # or wherever the signature block sits
              x_coord   = <px from left>
              y_value   = <px from top>
              width     = 180
              height    = 48
            }
          )
          date_fields = @(
            @{
              field_type_name = "Date"
              field_type_id   = "604823000000000151"
              page_no   = 12
              x_coord   = <px>
              y_value   = <px>
              width     = 120
              height    = 28
              date_format = "dd MMM yyyy"
            }
          )
        }
      },
      @{
        action_id = $action_ids[1]   # sgc_sign — same shape, yours to position
        # identical signature/date image_fields + date_fields
      }
    )
  }
} | ConvertTo-Json -Depth 12 -Compress

Invoke-RestMethod -Method POST `
  -Uri "$API/requests/$request_id/submit" `
  -Headers @{ Authorization = "Zoho-oauthtoken $access_token" } `
  -Form @{
    action_id   = $action_ids[0]
    document_id = $document_id
    data        = $fields
  }
```

If Step B returns errors → the envelope **was created but never sent** (`request_id` will still be visible in Zoho Sign as an unsent draft). Fix fields and re-submit. The Zoho Sign REST semantics require both steps.

### 5.4 — Record the envelope on the manifest

Open `02-clients/VGE-vongeyern-realestate/manifest.yaml`. Find `current_revision: VGE-2026-SUB-01_Rev3`. Set:

```yaml
stage: sent
sent_date: "<ISO-8601 UTC of step 5.2 success>"
envelope_id: "<request_id from §5.2>"
issued_artifacts:
  - path: "05-issued/VGE-2026-SUB-01_Rev3/VGE-2026-SUB-01_Rev3_Sent.pdf"
    frozen_sha256: "<hex digest from §3>"
```

Save and commit the manifest.

### 5.5 — Copy the artefact into `05-issued/`

**Before** the client's first view, copy:

```powershell
New-Item -ItemType Directory -Force `
  -Path "..\05-issued\VGE-2026-SUB-01_Rev3"
Copy-Item .\VGE-2026-SUB-01_Rev3_Sent.pdf `
        ..\05-issued\VGE-2026-SUB-01_Rev3\
```

After this copy you **must not edit** anything inside `05-issued/VGE-2026-SUB-01_Rev3/`. If a revision is needed, increment and start over (AGENTS.md absolute rule).

---

## 6. Odoo write-back — what happens automatically vs not

Until the webhook handler is deployed and registered in Zoho Sign, **delivery works but Odoo stays stale**.

| Event | crm.lead effect | Pre-condition |
|---|---|---|
| `sent` | stage → Proposal Sent; attach frozen PDF; day-3 follow-up | handler deployed + webhook registered |
| `signed_by_a_recipient` | audit only | same |
| `completed_by_all` | stage → Won; attach signed PDF + audit cert; draft mobilisation invoice (G51 — human posts); kickoff activity; notify SDR + signatory + client; **hash-verify signed PDF vs frozen first; abort + CRITICAL alert on mismatch** | same |
| `declined` | stage → Lost; record reason; SDR follow-up | same |
| `expires` | stage → Stalled/Proposal Sent; SDR follow-up | same |
| `voided` (recalled) | stage → Stalled/Proposal Sent; SDR follow-up | same |
| `hard_bounced` | log + alert; **no Won** | same |
| `reassigned` | audit only | same |

The Odoo fields the handler expects on `crm.lead` are listed in `10-signature/odoo-mapping.yaml`. The matching Odoo module skeleton lives at `10-signature/sgc-crm-fields/` — to be ported into `odoo19-sgc/addons/` by the Odoo developer before go-live.

Until those two external steps (handler deploy + webhook register) happen, the only signal you get back from Zoho is the email reminders to the SDR. Do **not** treat signed-up Zoho as Won in Odoo manually — wait for the webhook.

---

## 7. Hard guardrails (do not violate)

- **G29** — gate-report reviewer signature is mandatory before the first send.
- **G14** — entity resolution (Odoo client, signer email, SGC signatory) is verified on every send.
- **G35** — SGC is not VAT-registered. Do **not** add a VAT line or quote TRN. The MSA/Order Form carry the truthful disclosure; the proposal prose stays silent unless the client or SDR raises it (your 2026-08-04 decision).
- **G36** — Odoo Community ≠ Enterprise. Never describe Community as Enterprise in body, subject, or signature page.
- **G49** — completion requires **both** signatures; client alone does not constitute completion.
- **G51** — mobilisation invoice created as **draft**; human posts after payment confirmation.
- **G52** — never commit Zoho credentials, Odoo API key, or webhook secret anywhere in the repo.

---

## 8. Quick recap (for the SDR)

1. `validate.py` exit 0 ✓
2. gate-report line 76 signed ✓
3. authorised signer confirmed in writing (in this runbook or `reviewer-notes.md`) ✓
4. freeze the PDF, sha256, copy into `05-issued/VGE-2026-SUB-01_Rev3/` ✓
5. run steps 5.1 → 5.3, record `envelope_id` + `sent_date` + `frozen_sha256` in `manifest.yaml` ✓
6. wait for webhook callbacks; do not write to Odoo manually

If anything in §0 fails, do not start §1.

---

## 9. Restart-from-scratch when needed

If `validate.py` regresses to exit 1, or `manifest.yaml.gates_passed` flips to `false`, or the client retracts/significant new info arrives — the correct path is a new revision (`Rev4`), not an in-place edit.

- Increment `current_revision` to `VGE-2026-SUB-01_Rev4`.
- Re-run the pipeline; new `walkaway_card_produced: true`, new reviewer signature, new frozen PDF.
- Send via a new envelope — never reuse a declined/voided `envelope_id`.
