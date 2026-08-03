# Current State

## Systems in use today

PropSpace for listings and CRM (estimated AED 1,100–1,760/mo depending on
tier). Invoicing and maintenance-request handling run separately on
spreadsheets, with no link back to the property or tenancy record.

## Process pain points

- Tenancy renewal reminders are manual and have been missed before.
- Raising an invoice from a maintenance request means retyping
  information already captured elsewhere.
- No visibility into agent-level closing performance, only raw activity
  logs.
- Listings are entered once in PropSpace, then re-entered manually for
  any portal not directly integrated.

## Constraints and dependencies

- Portal sync (Property Finder, Bayut, Dubizzle) depends on the client's
  own RERA/DLD licensing and each portal's own feed-access terms — see
  `market-data/vertical-notes/uae-real-estate.md` and
  `phase2-catalogue.yaml: portal_dependency_note`. This is Phase 2, not
  Phase 1 — see §07.
- Migration data quality is rated medium confidence for the ~480 records
  and ~210 documents identified at intake.
