# Signature Provider Evaluation

## Pre-build resolution

### Odoo edition

SGC runs **Odoo Community** internally. This is established by:

- `00-knowledge/pricing/editions.yaml: default_edition: community`
- AGENTS.md rule G36: "NEVER describe Odoo Community as Enterprise"
- `06-brand/entity/legal-identity.yaml` showing SGC as Scholarix Global Consultants FZCO, a trade-license entity without reference to an Odoo Enterprise subscription

**Consequence**: Odoo Sign (an Enterprise-only app) is unavailable. The pipeline must use an external e-signature provider and write back to Odoo via the Odoo External API (XML-RPC / JSON-RPC).

---

## Provider evaluation

Three providers were evaluated for SGC's profile: ~5 envelopes/month, UAE jurisdiction, webhook-driven automation, Odoo Community write-back.

### Zoho Sign

| Criterion | Assessment |
|---|---|
| UAE legal posture | Meets Federal Decree-Law 46/2021 (AES-level signatures, GlobalSign/Seiko timestamps, OTP auth). Zoho is a global TSP; UAE TDRA licensing status should be confirmed before first live use (see lawyer item below). |
| Audit certificate | Full audit trail + Certificate of Completion per envelope. Tamper-evident sealing via hash. |
| Webhook reliability | HTTPS callback URL required. HMAC signing via `X-ZS-WEBHOOK-SIGNATURE` header (HMAC-SHA256 of raw body, base64) + `X-ZS-WEBHOOK-TIMESTAMP` (authoritative clock, 300s skew window), keyed by the Zoho Sign webhook secret (`whsec_...`). Retry on 2xx-within-30s timeout. |
| HMAC of callbacks | Yes — HMAC-SHA256 of raw body using `ZOHO_SIGN_WEBHOOK_SECRET` (see `webhook-spec.md`). |
| Per-envelope cost at 5/mo | **Free tier** — 5 envelopes/month, no charge. |
| Data residency | Zoho's global infrastructure; UAE data residency not confirmed as a stated option. Confirm with Zoho before use if data-sovereignty is a hard requirement. |
| API completeness | Full REST API: send envelope, get status, download signed PDF, download audit certificate, list envelopes. |

### Dropbox Sign (formerly HelloSign)

| Criterion | Assessment |
|---|---|
| UAE legal posture | Same AES/audit trail level as Zoho. Widely used internationally. |
| Audit certificate | Full audit trail + Certificate of Completion. |
| Webhook reliability | Retries up to 6 times with exponential backoff (5 min → 15 → 45 → 2h15 → 6h45 → 20h15). Requires `200` with body containing `Hello API Event Received`. |
| HMAC of callbacks | Yes — `Content-Sha256` header (HMAC-SHA256 of JSON payload using API key). IP allowlist also available. |
| Per-envelope cost at 5/mo | **API Essentials: $75/month** (50 envelopes included). No free tier for API. $15/month plan starts at 5 envelopes but requires annual commitment. |
| Data residency | Dropbox global infrastructure; EU/US primary. |
| API completeness | Full API: send, status, download signed PDF, audit trail. |

### DocuSign

| Criterion | Assessment |
|---|---|
| UAE legal posture | Recognised globally; AES-level signatures. |
| Audit certificate | Comprehensive audit trail + Certificate of Completion. |
| Webhook reliability | Connect platform with retry and dead-letter queue. Enterprise-grade. |
| HMAC of callbacks | Yes — HMAC-SHA256 with client secret. |
| Per-envelope cost at 5/mo | **Not viable** — minimum API plan is ~$25/month and volume starts at 100 envelopes. |
| Data residency | US primary, with some regional options. |
| API completeness | Full API but designed for high-volume enterprise use. |

---

## Recommendation

**Zoho Sign — free tier**.

At 5 envelopes/month the cost is zero. Zoho Sign provides all the capabilities SGC requires: HMAC-verified webhooks, tamper-evident audit trail, OTP signer authentication, signed PDF download, audit certificate download, and a REST API that covers every operation in this pipeline.

The only material risk is confirming Zoho's TDRA licensing status under UAE Federal Decree-Law 46/2021 before first live use. This is a lawyer item, not a blocker for building the integration.

**Dropbox Sign** is the fallback if Zoho's UAE licensing is not confirmed. Its minimum viable API cost (~$15/month) is acceptable at SGC's volume.

**DocuSign** is excluded — minimum cost and volume assumptions are incompatible with 5 envelopes/month.

---

## Storage of signed PDFs

Signed PDFs and audit certificates are stored in **two places**:

1. **Zoho Sign's cloud** — original hosted copy. Zoho retains indefinitely on its paid plans; the free plan has 5-envelope active limit but Zoho's standard retention policy preserves completed envelopes.
2. **SGC's own storage** — downloaded by the webhook handler on `completed` event and stored to SGC's chosen document store (AWS S3, Google Drive, or equivalent). This is the copy with delete/access-control rights that SGC owns.

SGC's copy is the primary operational document. Zoho's copy is the secondary evidence source.

Delete rights: only a named SGC admin may delete a stored signed contract. The webhook handler never deletes. A deletion is an amendment-triggering event — a new envelope is issued for any contract change, never an overwrite.

---

## Items for a UAE-qualified lawyer to confirm before first live use

1. Is Zoho Sign (or Dropbox Sign) a licensed TSP or QTSP under UAE Federal Decree-Law 46/2021 and Cabinet Resolution 28/2023? If not, what is the evidential weight of their audit certificates in a UAE court?
2. Does a signature created with OTP authentication meet the "associated exclusively with the signatory" requirement under Article 19(1) of the 2021 Law?
3. Is Zoho Sign's GlobalSign/Seiko timestamping service a recognised "Qualified Trust Service" under the TDRA's trusted list?
4. What evidence must SGC present in addition to the audit certificate to establish the contract's enforceability — e.g., the hash chain linking the frozen PDF to the signed PDF?
