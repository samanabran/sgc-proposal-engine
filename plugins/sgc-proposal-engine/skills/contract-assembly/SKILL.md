---
name: contract-assembly
description: Parallel to drafting, steps 10–11. Assembles the MSA & SLA, Order Form, and consistency map. Sanity-checks the cross-document reconciliation.
version: 1.0.0
owner: SDR
position: 10-11
---

# contract-assembly

The contract-assembly stages. Runs in parallel with `proposal-drafting`
— same inputs, different outputs. Produces the Order Form, the
sanitized copy of the MSA & SLA ready for envelope inclusion, and the
cross-document consistency map.

## When to use

- Trigger phrases: "assemble the MSA", "fill the order form", "reconcile the documents", "build the consistency map", "prepare the envelope packets", "fill Appendix I", "check the entity fields".

If pricing is incomplete, refuse. If a draft is requested, route to
`proposal-drafting` — this skill does not write §01–§13 prose.

## Position in step gate

Steps 10 and 11. Runs in parallel with `proposal-drafting`. The fixed
sequence:

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

This skill **refuses to run** unless `subscription-pricing` has
produced `02-calc/gate-report.md` with `manifest.yaml: gates_passed: true`.

## Bundled knowledge files to read, in order

1. `contracts/msa-sla.html` — canonical MSA & SLA v2026.08
2. `contracts/order-form.template.html` — generic Order Form template
3. `knowledge/clause-library/` (24 files) — verbatim text for legal/financial wording
4. `knowledge/commercial-rules/subscription-guardrails.md`, `payment-plan-guardrails.md`, `protection-guardrails.md` — G1–G41
5. `knowledge/guardrails-g42-g53.yaml` (mirror) — G42–G45, G53
6. `06-brand/entity/legal-identity.yaml` — for the SGC signatory block (read via the desk's `published-floor-authoring` skill, never directly into a draft)
7. The client's `client-brief.yaml: client.legal_name` and the registered address — for the client cover page

## What it writes, where

- `<workspace>/sgc-proposals/<CLIENT-CODE>/08-consistency-map.md` (generic template, NOT the VGE-specific one) — the proposal ↔ MSA ↔ Order Form reconciliation
- `<workspace>/sgc-proposals/<CLIENT-CODE>/03-draft/<PROPOSAL-REF>_RevN/<PROPOSAL-REF>_RevN_OrderForm.pdf` — the filled Order Form, brand-styled
- `<workspace>/sgc-proposals/<CLIENT-CODE>/03-draft/<PROPOSAL-REF>_RevN/<PROPOSAL-REF>_RevN_MSA_SLA.pdf` — the MSA & SLA ready for envelope inclusion, brand-styled
- `<workspace>/sgc-proposals/<CLIENT-CODE>/03-draft/<PROPOSAL-REF>_RevN/signature-blocks.md` — the resolved signatory name, title, organisation, date placeholders

## What it refuses

- **Incomplete pricing** — refuses if `manifest.yaml: gates_passed` is anything other than `true`. Cite `step-gate.md` step 8.
- **Out-of-order invocation** — refuses if intake or pricing has not produced the three intake files and the pricing worksheets.
- **Open RESOLVE on an entity field** — refuses to issue a contract with any unresolved `RESOLVE:` on `client.legal_name`, `client.jurisdiction`, `client.trade_licence_number`, or `06-brand/entity/legal-identity.yaml: registered_address`. Cite `escalation-triggers.md:35-44`.
- **Paraphrased legal wording** — refuses to paraphrase any clause-library text. Wording is verbatim.
- **Edition misdescription in the MSA §A.9** — refuses to describe Community as Enterprise or omit the Enterprise exclusion list. Cite G36, G38, G44.
- **VAT status claims** — refuses to write "VAT inclusive", "VAT exempt", "free zone exempt", or any TRN field in the MSA §C.6. The gross-up clause from `clause-library/vat-gross-up.md` is mandatory. Cite G35, G45.
- **Order Form figures that don't reconcile with the worksheet** — refuses to write an Order Form whose figures differ from the pricing worksheet.
- **FZE** (legacy spelling) — the MSA is updated to FZCO per `06-brand/entity/legal-identity.yaml`. If the bundled `msa-sla.html` still says FZE, that file is the desk-side remediation target, not the SDR-side work. The SDR plugin accepts the desk-shipped copy verbatim and flags the drift to the desk via `escalations.md`.

## Consistency map

The map is a single markdown table with one row per shared variable, and three columns (Proposal / MSA / Order Form). A mismatch is a drafting defect; the skill refuses to mark this step complete with any open mismatch.

Required rows:

- client.legal_name
- client.trade_licence_number, client.trade_licence_authority
- client.jurisdiction (mainland | free_zone)
- client.registered_address
- edition (community | enterprise)
- term_months
- cadence
- mobilisation_amount_aed, mobilisation_pct
- subscription_monthly_aed (platform + recovery)
- platform_fee_monthly_aed
- recovery_fee_monthly_aed
- support_tier
- signatory name, title, organisation, date
- edition.upgrade_policy (verbatim from `editions.yaml`)
- vat.disclosure (verbatim from `clause-library/vat-gross-up.md` and `clause-library/vat-uae.md`)

## What this skill does NOT do

- It does not call Zoho Sign. `signature-dispatch` does that, after the approval record exists.
- It does not write the proposal §01–§13 prose. `proposal-drafting` does that.
- It does not change the canonical MSA template. The template lives in the desk plugin; the desk-side `walk-away-authoring` and `deal-card-review` skills author any template change. The SDR plugin's `contracts/msa-sla.html` is desk-shipped and verbatim.

## Escalation path

- **FZE drift in the bundled MSA** — write to `manifest.yaml: escalations` and `escalation-triggers.md` is the desk's authority. The SDR continues with a `RESOLVE:` placeholder in the cover page until the desk remediates.
- **Any legal wording not in the clause library** — escalate to counsel (desk-side). Cite `clause-library/*: requires_counsel_review: true`.
- **Edition trigger condition fires** — `RESOLVE: edition = enterprise (trigger: <condition>)`. The desk's `deal-card-review` may ratify.
- **Open RESOLVE on a Tier 1 client field** — the proposal and MSA both carry the `RESOLVE:` placeholder in the affected field; the deal cannot reach `issue-ready` per `sufficiency-rules.yaml: tier_1`.

## Acceptance check (self-test)

Before allowing `approval-gate` to run, this skill must be able to answer YES to each:

1. Order Form figures reconcile with the pricing worksheet?
2. MSA §A.9 carries the edition and the upgrade policy verbatim?
3. MSA §C.6 carries the gross-up clause verbatim?
4. Consistency map has every required row, no open mismatches?
5. No `RESOLVE:` on any entity field that the cover page or signature block requires?
6. The frozen PDFs for proposal / Order Form / MSA & SLA all exist and SHA-256s are recorded in `manifest.yaml`?
