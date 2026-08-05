# Options & Inclusions

## Phase 2 options (not included in this proposal's pricing)

| Option | Description | Reference price |
|---|---|---|
| Portal sync — Property Finder | Automated listing sync and enquiry ingestion | AED 3,900 one-time — `phase2-catalogue.yaml`. Conditional on 5 preconditions (valid RERA/DLD licence, agency RERA ID, portal-side verification, image-standard compliance, Client's own portal API subscription in place) — **not yet confirmed for this deal, see verbal-promises.md** |
| Portal sync — Bayut & Dubizzle | Automated listing sync and enquiry ingestion | AED 3,400 one-time — `phase2-catalogue.yaml`. Same preconditions as above |
| AI Lead Scorer — Lite | Rule-based scoring | AED 495/mo — `phase2-catalogue.yaml` |
| Additional users beyond 40 | Per-user, non-discountable | AED 250/user/month — `phase2-catalogue.yaml` |

These are available to add at any point; adding one after go-live does not
require re-opening this proposal, only a short scoping note and updated
`pricing-worksheet.yaml` for that increment.

**Not currently priceable**: WhatsApp Business API integration has no
basis in this repo's `hour-lookup.yaml` or `phase2-catalogue.yaml` — it
must be scoped and escalated before ever being quoted, not estimated by
analogy to another line item.

## Assumptions

- Data quality on the 500 migrated records is unconfirmed — not yet
  assessed against source Sheets data.
- RERA/DLD licensing status and any third-party portal (listing feed) API
  access remain the Client's responsibility and are assumed already in
  place if portal sync is added; SGC's scope does not include obtaining
  or renewing these.
- The Client's decision maker(s) are available for discovery and
  requirements confirmation within the proposed timeline — not yet
  confirmed given the incomplete BANT gate on this deal.

## Exclusions

The following are excluded from the scope and pricing of this proposal
unless explicitly listed as an included module, work package, or option
elsewhere in this document:

- Third-party software licensing costs not explicitly listed in this
  proposal's commercial terms, including any client-side portal
  subscription fees (e.g. Property Finder API access), which remain the
  Client's own recurring cost.
- Custom development or configuration beyond the work packages listed in
  §06 Solution (Phase 1) and §07 Options & Inclusions.
- Portal sync (Property Finder, Bayut, Dubizzle), AI lead scoring, and
  WhatsApp Business integration — all separately priced or not yet
  priceable, see above.
- Data migration from source systems not identified in the Client's
  brief, or migration volumes materially exceeding the figures stated
  there.
- Ongoing change management, internal communications, or user adoption
  activity beyond the training sessions included in this proposal (see
  §09 Adoption).
- Hardware procurement, on-premise infrastructure, or network setup at
  the Client's premises.
- Regulatory, tax, or legal advisory services. Where this proposal
  references compliance requirements (RERA/DLD or similar), such
  references are operational configuration guidance only and do not
  constitute legal or tax advice.
- Integration with third-party systems not explicitly named in this
  proposal's scope.
- Support and maintenance beyond the tier and term specified in §11
  Support & SLA.
- Travel and accommodation beyond what is explicitly itemized.
- Group-level/multi-company rollout ("Kallat Group Command Center") —
  explicitly forward-looking, not priced in this proposal.

Any work requested outside this list is treated as a change request and
quoted separately, at the rates current in SGC TECH AI's rate card at the
time of the request.
