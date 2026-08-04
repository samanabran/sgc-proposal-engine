---
name: proposal-drafting
description: Steps 9–11 of the SDR pipeline. Renders the 13-section proposal HTML from the pricing worksheet, applies the brand, and produces the frozen PDF with SHA-256.
version: 1.0.0
owner: SDR
position: 9-11
---

# proposal-drafting

The drafting, brand, consistency, and PDF-render stages. Runs after
pricing is complete and gates pass, before approval.

## When to use

- Trigger phrases: "draft the proposal", "render section 06", "produce the HTML", "apply the brand", "freeze the PDF", "write §10 commercial terms", "draft §13 next steps".

If pricing has not completed, this skill will refuse. If an envelope
send is requested, route to `signature-dispatch`.

## Position in step gate

Steps 9, 10, 11. The fixed sequence:

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

This skill **refuses to run** unless `subscription-pricing` has
produced `02-calc/gate-report.md` with `manifest.yaml: gates_passed: true`.

## Bundled knowledge files to read, in order

1. `templates/proposal/_section-map.md` — required contents of §01–§13
2. `templates/proposal/01-executive-summary.md` through `13-next-steps.md` — section templates
3. `brand/tokens/color.yaml`, `type.yaml`, `grid.yaml`, `decor.yaml` — render tokens
4. `brand/styles/proposal.pdf.css` — A4 portrait, 20mm margins
5. `knowledge/clause-library/` (24 files) — verbatim text for legal/financial wording
6. `knowledge/policy.yaml`, `editions.yaml`, `hosting.yaml`, `payment-plans.yaml`, `concession-ladder.yaml` (sanitized derivatives) — for the figures in §10
7. `contracts/msa-sla.html` — for the legal-entity fields in the cover page and signature block
8. `knowledge/guardrails-g42-g53.yaml` (mirror) — for the disclosure rules on edition (G44) and VAT (G45)

The desk-controlled renderer (with the watermark rotation in
`06-brand/rotation.yaml`) lives in the desk plugin. The SDR plugin
calls the renderer over the Den-managed MCP connection.

## What it writes, where

- `<workspace>/sgc-proposals/<CLIENT-CODE>/03-draft/<PROPOSAL-REF>_RevN/§01-§13_*.md` (per-section markdown)
- `<workspace>/sgc-proposals/<CLIENT-CODE>/03-draft/<PROPOSAL-REF>_RevN/<PROPOSAL-REF>_RevN_Proposal.html` (the rendered HTML)
- `<workspace>/sgc-proposals/<CLIENT-CODE>/03-draft/<PROPOSAL-REF>_RevN/<PROPOSAL-REF>_RevN_Proposal.pdf` (the rendered PDF, not yet frozen)
- `<workspace>/sgc-proposals/<CLIENT-CODE>/08-consistency-map.md` (the proposal ↔ MSA ↔ Order Form reconciliation)
- `<workspace>/sgc-proposals/<CLIENT-CODE>/04-review/qa-checklist.md`
- `<workspace>/sgc-proposals/<CLIENT-CODE>/04-review/brand-qa-checklist.md`

`<PROPOSAL-REF>` is the standard PREFIX-YEAR-TYPE-NN form (e.g.
`VGE-2026-SUB-01`). The revision number increments on every re-issue.

## What it refuses

- **Incomplete pricing** — refuses if `manifest.yaml: gates_passed` is anything other than `true`. Cite `step-gate.md` step 8.
- **Out-of-order invocation** — refuses if the consistency-map, validate, and QA files are not yet produced (steps 11–13).
- **Any client-attributed statement without an origin tag** — every fact in the draft must trace to `sdr` / `document:<file>#<loc>` / `client-words` in the session log. Cite `fabrication-rules.md:14-25`.
- **Any number not traceable to a published source** — every commercial figure traces to the worksheet; every clause-library clause is used verbatim. Cite `fabrication-rules.md:40-42`.
- **Edition misdescription** — refuses to call Community "Enterprise" (G36, G44) or omit the Enterprise exclusion list (G38).
- **VAT status claims** — refuses to write "VAT inclusive", "VAT exempt", "free zone exempt", or any TRN field (G35, G45). The MSA §C.6 carries the gross-up clause from `clause-library/vat-gross-up.md`.
- **Forbidden phrases** — refuses to write any of the phrases in `01-templates/qa/pre-send-checklist.template.md:18-51` (desk reference; mirror this list in the QA output).
- **Paraphrased legal wording** — refuses to paraphrase any clause-library text. Wording is verbatim.
- **Three options** — refuses to construct a third pricing option. Two options (A: mobilisation paid; B: zero upfront, currently WITHDRAWN) — never a third tier.

## Brand resolution

The renderer reads `brand/tokens/*.yaml` and `brand/styles/proposal.pdf.css` from this plugin. The watermark rotation per section lives in the desk-controlled renderer; the SDR plugin never reads `06-brand/rotation.yaml` directly. The proposal is rendered with a watermark from the rotation table that the desk has authorised for that section; the renderer call is via Den-managed MCP.

## Consistency map

`08-consistency-map.md` reconciles every shared variable across proposal, MSA, and Order Form:

- client legal name (matches `client-brief.yaml: client.legal_name` and `06-brand/entity/legal-identity.yaml`)
- edition (community / enterprise)
- term (months)
- cadence (cadence_table entry)
- mobilisation amount, percentage, and date
- subscription monthly AED (platform + recovery)
- support tier
- jurisdiction
- signatory names and titles

A mismatch in any row is a drafting defect, not a rounding difference to wave through. The skill refuses to mark this step complete with any open mismatch.

## PDF render and SHA-256

After the HTML draft passes the consistency map and the QA checklist, render the PDF. Compute SHA-256 of the rendered PDF and record it in `manifest.yaml: revisions[].frozen_sha256`. The frozen PDF is the artifact bound to the approval record (G53).

## Escalation path

- **Edition uncertainty** — `RESOLVE: edition = ? (Community default; only an explicit trigger condition moves to Enterprise)`. The desk-side `walk-away-authoring` may resolve.
- **Watermark missing for a section** — escalate to the desk's `brand-qa-checklist`; the SDR plugin never reads rotation.yaml directly.
- **Consistency mismatch** — fix the proposal or the MSA/Order Form before proceeding; the desk-side `consistency-map.template.md` is the canonical schema.
- **Section too thin** — if the section-map requires content that the brief does not support, emit `RESOLVE:` and route back to intake; do not pad.

## Acceptance check (self-test)

Before allowing `approval-gate` to run, this skill must be able to answer YES to each:

1. All 13 sections rendered, none thin per `_section-map.md`?
2. Consistency map reconciles every shared variable across proposal ↔ MSA ↔ Order Form?
3. QA checklist complete with every verbal-promise item reflected?
4. Brand QA complete; no off-palette tokens?
5. Forbidden-phrase scan: zero hits?
6. PDF rendered, SHA-256 computed, recorded in `manifest.yaml`?
7. The frozen PDF lives at `<workspace>/sgc-proposals/<CLIENT-CODE>/04-issued/<PROPOSAL-REF>_RevN_<PROPOSAL-REF>_RevN_Sent.pdf` (moved from `03-draft/` to `04-issued/` at this point)?
