# Solution — Phase 1

## Modules

| Module | Source | Included |
|---|---|---|
| Odoo CRM | `saas-modules.yaml: erp.odoo_crm` | ✓ |
| Odoo Sales | `saas-modules.yaml: erp.odoo_sales` | ✓ |
| Odoo Accounting | `saas-modules.yaml: erp.odoo_accounting` | ✓ |

## Work packages

| Work package | Deliverable | Hours | Complexity |
|---|---|---|---|
| Discovery workshop | Agenda, findings, priorities | 12 | Medium |
| Business process assessment | As-is maps, pain-point log | 24 | Medium |
| Solution blueprint | Scope, architecture, roadmap | 32 | Medium |
| Project kickoff | Governance pack, plan, RAID log | 8 | Medium |
| Requirements workshops | Process requirements by module | 26 | Medium |
| Finance setup (trust/commission) | COA, taxes, journals, controls | 60 | High |
| UAE VAT localization | VAT mapping, test cases | 14 | Medium |
| Sales/CRM configuration | Pipeline, quotations, approvals | 24 | Medium |
| Documentation | — | 10 | — |
| QA | — | 16 | — |
| Training | 2 sessions × 2 hrs | 4 | — |

**Total: 230 hours** at the smb blended rate (AED 395/hr).

## What "done" looks like for Phase 1

- Every open deal migrated and visible in the CRM pipeline with correct
  stage.
- Trust and commission accounting configured so commission postings
  trigger automatically from deal-stage changes, with a reviewable audit
  trail.
- UAE VAT correctly applied across sales and accounting flows.
- Yusuf and agent team trained and able to operate the system
  independently.

## Migration scope

~850 historical deal/contact records and ~400 documents (signed
contracts, ID docs, title deeds). Data quality confidence is rated medium
at intake — the discovery and business-process-assessment work packages
above include a validation pass on this data before migration executes.
