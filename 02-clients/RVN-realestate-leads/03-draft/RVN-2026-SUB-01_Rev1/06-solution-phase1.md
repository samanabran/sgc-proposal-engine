# Solution — Phase 1

## Work packages

| Work package | Deliverable | Hours | Complexity |
|---|---|---|---|
| Discovery | Confirmed workflow, priorities, data-quality check | 5 | Standard |
| CRM & leads configuration | Lead capture, automated + one-click manual distribution, per-agent CRM activity logging (call outcome, notes, follow-up flag) | 6 | Standard |
| Users, roles & agent performance | Role-based access for 7 sales/telesales/broker seats; agent activity views | 4 | Standard |
| Reporting dashboard | Logged call activity per agent per day, vs. 250-calls/day target | 4 | Standard |
| Data migration | Existing Google Sheet lead records migrated into CRM | 6 | Standard |
| Migration record validation & sign-off | Post-migration data-quality check and sign-off | 8 | Standard |

**Total: 49 hours all-in** (work packages + Class B per-user provisioning
+ documentation + QA + training + hypercare go-live support), at the
startup_boutique blended rate (AED 280/hr) plus per-task Class B rates —
see `02-calc/pricing-worksheet.yaml` for the full breakdown.

## What "done" looks like for Phase 1

- Every lead from your Meta/Google ad pipeline is visible and assigned
  in the CRM within your defined SLA, with no manual sheet-copying step.
- **New-lead notification, day one**: the assigned agent gets an in-app
  CRM notification the moment a lead is distributed to them — this
  replaces today's WhatsApp-based instant-lead alerting, so nothing is
  slower at go-live than it is now. No catalogue entry states a specific
  notification-latency SLA (e.g. "within N seconds") — that figure is
  TBD, to be confirmed during discovery, not assumed here. This does not
  require WhatsApp Business API and does not change Phase 1 pricing.
- Every call an agent makes is logged against the lead record with an
  outcome and notes — no end-of-day recall required.
- Management can see, per agent per day, logged call volume against the
  250-calls/day target from a single dashboard.
- Ms. Dia and the sales/telesales team are trained and able to operate
  the system independently.

## What this does NOT include (see §05 for the honest version)

Native Odoo Community CRM activity logging covers manual call-outcome
recording. It does **not** automatically detect or count calls made from
a phone system — that requires the telephony integration scoped
separately in §07. Similarly, attendance/break tracking here is not
included until your sensor system's vendor and API access are known —
also §07.

## Migration scope

400-600 leads/month volume was confirmed on the discovery call; the
exact total backlog record count in your Google Sheets was not stated.
This proposal's `data_migration_500` work package is sized against the
nearest available catalogue band — if your actual backlog materially
exceeds ~500 records, this is flagged for re-confirmation before
kickoff, per the standard exclusions in §07.
