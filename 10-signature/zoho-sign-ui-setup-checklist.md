# Zoho Sign UI Setup Checklist — Manual Configuration

Applies to: the SGC TECH AI Zoho Sign account (admin: `hello@scholarixglobal.com`).

This checklist is for **manual configuration in the Zoho Sign web UI** — the agent has
no Zoho Sign UI credentials, so an SGC human performs these steps. Everything here is
the *configuration* side of the contract specified in `webhook-spec.md`,
`send-protocol.md`, and `odoo-mapping.yaml`.

> **Status legend**: ☐ = not done · ✅ = done · ⚠ = needs verification

---

## 1. Webhook delivery (REQUIRED before go-live)

The webhook handler is a **separate deployed service** (see `webhook-spec.md`). Zoho Sign
must be configured to deliver callbacks to it.

| # | Step | Where in Zoho Sign UI | Status |
|---|---|---|---|
| 1.1 | Deploy the webhook handler service and note its public HTTPS URL | (external — the service repo) | ☐ |
| 1.2 | Create a webhook pointing at `POST https://<handler-host>/webhooks/signature/zoho_sign/` | **Settings → Webhooks → Add Webhook** (or Admin → Webhooks) | ☐ |
| 1.3 | Copy the webhook secret (`whsec_...`) shown once at creation into the handler's `ZOHO_SIGN_WEBHOOK_SECRET` env var | Webhook creation dialog → copy secret | ☐ |
| 1.4 | Subscribe to **all** of these events (handler treats each as required): `sent`, `viewed`, `signed_by_a_recipient`, `completed_by_all`, `declined`, `expires`, `recalled`, `hard_bounced`, `reassigned` | Webhook event checklist | ☐ |
| 1.5 | Confirm the webhook is **active/enabled** after creation | Webhooks list | ☐ |
| 1.6 | Send a test envelope, verify the handler returns HTTP 200 and logs the event | (integration test) | ☐ |

Notes:
- The handler **must** be reachable at a public HTTPS endpoint (no self-signed certs).
- Zoho Sign retries on non-2xx; the handler returns 200 immediately after the
  idempotency check and processes asynchronously (never block > 500 ms — `webhook-spec.md`).
- If the webhook UI lists event names differently (e.g. `signed`, `expired`, `voided`),
  map them to the handler's set via the handler config; log the difference in the
  handler's integration notes.

---

## 2. Email template From address (branded sender)

Goal: signing emails arrive **FROM `hello@scholarixglobal.com`**, not
`notifications@zohosign.com`.

**Current status (2026-08-04): NOT working — FROM still `notifications@zohosign.com`.**
Domain `scholarixglobal.com` is verified in Zoho Sign (DKIM `42287223._domainkey`
+ SPF `v=spf1 include:zcsender.net ~all` in Cloudflare), which is **necessary but not
sufficient**.

**Go-live decision 2026-08-04: NOT a gate.** Envelopes sent from
`notifications@zohosign.com` are equally enforceable (Zoho's audit certificate carries
the evidential weight; the frozen→signed SHA-256 hash chain is the integrity proof).
Branded FROM is a deliverability/trust improvement, fixed **in parallel** with the Odoo
integration. Honest risks if left default: a broker's spam filter may quarantine the
signing email; the client may not recognise the sender.

| # | Step | Where in Zoho Sign UI | Status |
|---|---|---|---|
| 2.1 | Open email template settings; set the **From address** to `hello@scholarixglobal.com` | **Settings → Email Templates** (edit the template used for signature requests) | ☐ |
| 2.2 | Complete individual address verification: Zoho sends a confirmation link to `hello@scholarixglobal.com` — click it in the inbox | Inbox of `hello@scholarixglobal.com` | ☐ |
| 2.3 | Ensure the branded template is the account **default** (API-created envelopes use the default template) | Email Templates → set default | ☐ |
| 2.4 | (Reliable delivery) Configure **Custom SMTP routing** so all Zoho Sign email goes through SGC's own mail server | **Settings → Email → Custom SMTP** (native release feature; needs SGC SMTP server + credentials) | ☐ |
| 2.5 | (Alternative, paid) Custom domain / white-label add-on if full brand control is required | Zoho Sign admin → request access (may incur licensing cost) | ☐ |
| 2.6 | Send a real test envelope to an external inbox and confirm the FROM line | (integration test) | ☐ |

When 2.6 is confirmed, flip the status in `send-protocol.md` → **Branded sender** section
to *verified* and record the template configuration used.

---

## 3. Pre-live provider checks (lawyer items — from `provider-evaluation.md`)

| # | Item | Status |
|---|---|---|
| 3.1 | Confirm Zoho Sign's TDRA licensing position under Federal Decree-Law 46/2021 for UAE e-signatures | ☐ |
| 3.2 | Confirm the audit certificate + signed PDF retention meets UAE commercial/VAT record rules (see `audit-retention.md`) | ☐ |
| 3.3 | Confirm OTP verification satisfies the client's authentication expectations | ☐ |
| 3.4 | Confirm the 5-envelope free tier capacity vs expected monthly volume (paid plan if needed) | ☐ |

---

## 4. Handover note

Record completion of every item here in the client's `manifest.yaml` under
`escalations` or a `signature_integration` note (whichever the runbook uses), so the
integration state is visible to the next SDR/engine run.
