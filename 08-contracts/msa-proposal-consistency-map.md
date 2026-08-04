# MSA / Proposal / Order Form — Consistency Map

**Rule**: the accompanying proposal may not be issued unless every row
below reconciles between the proposal, the MSA & SLA v2026.08, and the
Order Form. A mismatch in any row is a drafting defect, not a rounding
difference to wave through.

## Reconciliation table — VGE-2026-SUB-01_Rev3

| Variable | Proposal section | MSA reference | Order Form field | Reconciled? |
|---|---|---|---|---|
| Legal entity name | Cover + §03 | Cover page | `{{CLIENT_LEGAL_NAME}}` | ☐ |
| Client contact | Cover + §13 | — | `{{CLIENT_SIGNATORY}}` | ☐ |
| Reference | Cover, footer | — | `{{ORDER_FORM_REF}}` | ☐ |
| Revision | Cover, footer, Document control | — | `Rev3` | ☐ |
| Effective date | Cover | Cover page | `{{EFFECTIVE_DATE}}` | ☐ |
| Kickoff date | §08, §13 | §A.2 (Kickoff), §A.6 | `{{KICKOFF_DATE}}` | ☐ |
| Odoo Edition | §06, §11, §07 | §A.9 | `{{ODOO_EDITION}}` | ☐ |
| Service tier | §11 | Part B tables | `{{SERVICE_TIER}}` | ☐ |
| Initial Term | §05, §11 | §A.6, §A.7 | `{{INITIAL_TERM_MONTHS}}` | ☐ |
| Implementation Value | §05, §11 | §A.2, §C.1 | `{{IMPLEMENTATION_VALUE}}` | ☐ |
| Mobilisation Fee | §05, §11 | §A.2, §C.2 | `{{MOBILISATION_FEE}}` | ☐ |
| Recovery Component | §05, §11 | §A.2, §C.3 | `{{RECOVERY_COMPONENT}}` | ☐ |
| Platform Component | §05, §11 | §A.2, §C.4 | `{{PLATFORM_COMPONENT}}` | ☐ |
| Subscription Fee | §02, §11 | §A.2 | `{{SUBSCRIPTION_FEE}}` | ☐ |
| Billing cadence | §05, §11 | §C.5 | `{{BILLING_CADENCE}}` | ☐ |
| Upgrade policy | §06, §11 | §A.9 | `{{UPGRADE_POLICY}}` | ☐ |
| VAT position | §11 | Part A §A.2-tax, Part C §C.6 | Order Form field | ☐ |

## Order Form template — populated fields

```
order_form_ref:                  VGE-2026-SUB-01_OF_Rev3
client_legal_name:               Von Geyern Real Estate L.L.C
client_trading_name:             Von Geyern Real Estate
client_jurisdiction:              mainland
client_decision_maker:           Ms. Nadja, Owner
client_contact_email:            info@vongeyern.de
client_contact_phone:            +971 58 551 8040
odoo_edition:                    community
odoo_deployment:                 version-pinned
upgrade_policy:                  version-pinned_with_quoted_upgrades  # OCA-standard Community practice; see proposal §04
service_tier:                    growth
included_users:                  3
additional_user_price_aed_mo:    250
initial_term_months:             24
kickoff_date:                    target within 30 days of proposal issue date; exact date fixed at Order Form signature
cadence:                         quarterly_in_advance
implementation_value_aed:        14800
mobilisation_fee_aed:            4900
financed_remainder_aed:           9900
financing_uplift_pct:             0.18
recovery_component_aed_mo:       487
platform_component_aed_mo:       1163
subscription_fee_aed_mo:         1650
quarterly_billing_aed:           4950
year1_total_aed:                  24700
full_24mo_commitment_aed:         44500
vat_position:                     not_charged_gross_up_applies
sgc_signatory:                    Ali Asghar Teli Muhammad Iqbal Teli, Company Manager (hello@sgctech.ai / +971 52 198 5231)
sgc_licence_authority:            Dubai Integrated Economic Zones Authority (DIEZA), operating via IFZA — Dubai Silicon Oasis; License No. 45160
sgc_registered_address:           Maseed Building, Office No. 304, 119/12 St, Al Rigga, Dubai, United Arab Emirates
```

**Resolved 2026-08-04**: `sgc_signatory`, `sgc_licence_authority`, and
`sgc_registered_address` sourced from the government-issued DIEZA/IFZA
trade license (License No. 45160, entity legal status FZCO) and the
Odoo company record. Legal name corrected from a prior "FZE" mismatch
to "Scholarix Global Consultants FZCO" per the license. Registered
address uses the Odoo operational address (Al Rigga), not the
free-zone premises address on the license itself, per user decision.
See `06-brand/entity/legal-identity.yaml` for the single source of
truth these fields must stay in sync with.

## Reconciliation rule

The MSA prevails on legal terms; the Order Form prevails on commercial
figures; the proposal summarises both in plain English. Where the
proposal's wording diverges from either, the Order Form / MSA wording
governs and the proposal must be re-issued before client-facing use.
