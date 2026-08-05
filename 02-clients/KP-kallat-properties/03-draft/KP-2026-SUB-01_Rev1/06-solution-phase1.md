# Solution — Phase 1

## Modules

| Module | Source | Included |
|---|---|---|
| Odoo CRM | `saas-modules.yaml: erp.odoo_crm` | ✓ |
| Odoo Sales | `saas-modules.yaml: erp.odoo_sales` | ✓ |
| Odoo Accounting (TRN invoicing) | `saas-modules.yaml: erp.odoo_accounting` | ✓ |

## Work packages

| Work package | Deliverable | Hours | Complexity |
|---|---|---|---|
| Discovery | Requirements confirmation, priorities | 5 | Standard |
| Property/unit register | Property and unit records | 8 | Standard |
| Tenancies, contracts & reminders | Tenancy tracking, renewal reminders | 9 | Standard |
| TRN invoicing | Invoicing tied to deal/tenancy records | 5 | Standard |
| CRM & lead pipeline | Centralized lead pipeline, source attribution | 6 | Standard |
| Agent roles & accountability | Lead-locking, callback logging, SLA escalation | 4 | Standard |
| Reports & dashboard | Real-time reporting, replaces Google Sheets | 4 | Standard |
| Data migration (500 records) | Historical lead/contact migration | 6 | Standard |
| Rollout (40 users) | Role/permission setup, individual onboarding coordination, per-agent data validation | 120 | — |
| Documentation | — | 8 | — |
| QA | — | 13 | — |
| Training | 2 sessions × 2 hrs | 4 | — |

**Total: 192 hours** at the mid_market blended rate (AED 525/hr).

## What "done" looks like for this phase

- Every active lead visible in a centralized pipeline with source
  attribution and correct stage.
- Every lead locked to its assigned agent with mandatory callback logging
  and timestamps — the accountability gap directly addressed.
- Automated escalation triggers when an agent fails to act within an SLA
  window, visible to management.
- TRN-compliant invoicing tied to the underlying deal/tenancy record.
- Full 40-agent team onboarded with role-appropriate access.

## Migration scope

500 historical records from up to two source files (Google Sheets export).
Data quality confidence is unknown at this stage — not yet assessed
against source data, since this deal has not reopened with the client.
