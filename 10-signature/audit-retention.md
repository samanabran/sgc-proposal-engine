# Audit and Document Retention

## Append-only audit log

The signature audit log (`signature_events` table) is **append-only**. No UPDATE or DELETE operations are permitted. This is the legal record of every event that touched a contract and must be tamper-evident.

### Retention periods

| Record type | Retention period | Basis |
|---|---|---|
| Audit log entries (envelope events) | **10 years** from envelope completion date | UAE commercial contract limitation period (10 years for written commercial contracts under UAE Civil Transactions Code) |
| Signed PDF contracts | **10 years** from completion date | Same — commercial contract limitation period |
| Audit certificates (Zoho Sign) | **10 years** from completion date | Stored alongside the signed PDF |
| Odoo opportunity record (Won) | **10 years** after last activity | Commercial records retention |
| Mobilisation invoices | **10 years** from invoice date | UAE VAT/excise tax records retention (10 years under UAE Federal Law No. 7 of 2017 on Tax Procedures) |
| Draft invoices (unpaid, voided) | **3 years** from invoice date | Standard commercial record keeping |
| Decline/expire/void records | **10 years** from event date | Full audit trail preservation regardless of outcome |

### Deletion

**Signed contracts and audit certificates are immutable.** No overwrite, no regeneration, no re-rendering.

A signed contract may only be **superseded** by a formal amendment envelope, not by editing the stored artifact.

Delete rights:

| Document type | Who may delete | Required approval |
|---|---|---|
| Signed PDF | Named SGC admin only | Commercial Desk sign-off + legal review |
| Audit certificate | Named SGC admin only | Commercial Desk sign-off + legal review |
| Audit log entries | **No one** | Append-only — deletion is technically blocked |
| Draft invoices (voided) | Finance | SDR manager sign-off |

A deletion is logged in a separate `deletion_log` table with: document reference, deleted_by (user ID), deletion_date, reason, approving_authority.

### Storage

| Document | Primary storage | Secondary / backup |
|---|---|---|
| Signed PDF | SGC's own document store (AWS S3, Google Drive, or equivalent) | Zoho Sign's hosted copy |
| Audit certificate | Same as signed PDF | Zoho Sign's hosted copy |
| Audit log entries | PostgreSQL or equivalent (webhook handler's database) | Daily encrypted backup |
| Odoo attachments | Odoo's document management (ir.attachment) | Odoo database backups |

### Integrity verification

- SHA-256 hash of every signed PDF is recorded in `manifest.yaml` and in the Odoo opportunity custom field `x_signed_pdf_hash`.
- The append-only audit log is stored in a database with write-access controlled to the webhook handler service account only.
- Database backups are encrypted and stored in a separate AWS account or equivalent, not accessible to the webhook handler service account.

---

## Hash chain

The integrity chain is:

```
manifest.yaml: frozen_sha256
    ↓
  frozen PDF rendered for send
    ↓
  SHA-256(frozen PDF) = frozen_sha256 → stored in manifest.yaml + Odoo x_frozen_pdf_hash
    ↓
  Zoho Sign → signs → produces signed PDF
    ↓
  SHA-256(signed PDF) = signed_pdf_hash → webhook handler downloads and verifies
    against frozen_sha256 before any Odoo write-back
    ↓
  signed_pdf_hash stored in Odoo x_signed_pdf_hash
    ↓
  audit log records: frozen_sha256 + signed_pdf_hash + reconciliation_status
```

If at any point `SHA-256(downloaded_signed_pdf) != frozen_sha256`:
1. The webhook handler **does not write to Odoo**
2. An immediate human alert is sent
3. The discrepancy is logged to the audit log with `reconciliation_status: FAILED`
4. The human investigates and determines the correct resolution
