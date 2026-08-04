---
name: approval-gate
description: Step 12 of the SDR pipeline. The mandatory human approval gate. Nothing reaches a client without a recorded decision from the named approver. Hash-binds the approval to one exact artifact.
version: 1.0.0
owner: SDR (read-only invocation); sole approver: Ali Asghar Teli Muhammad Iqbal Teli
position: 12
---

# approval-gate

The heart of the build. The gate that makes every other gate
honourable: no envelope is created without this gate having produced
a valid `approval-record.yaml`.

## When to use

- Trigger phrases: "approve the proposal", "request approval", "send to the approver", "produce the approval packet", "issue-ready check".

If any prior step is incomplete, refuse. If an envelope send is
requested, route to `signature-dispatch` — which will refuse without a
valid approval record (G53).

## Position in step gate

Step 12. The fixed sequence:

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

This skill **refuses to run** unless:

- `manifest.yaml: gates_passed: true`
- Zero open `RESOLVE:` fields
- Validator is clean (or only the expected entity-resolution blocker is open — and there are no open RESOLVEs on entity fields)
- `04-review/qa-checklist.md` and `04-review/brand-qa-checklist.md` are both complete
- The consistency map reconciles proposal ↔ MSA ↔ Order Form with zero mismatches
- The frozen PDF lives at `<workspace>/sgc-proposals/<CLIENT-CODE>/04-issued/<PROPOSAL-REF>_RevN/...` and SHA-256 is recorded in `manifest.yaml`

This skill's first action is to compute SHA-256 of the on-disk PDF
and check it against the recorded `frozen_sha256`. A mismatch is a
G53 hard stop.

## Bundled knowledge files to read, in order

1. `knowledge/guardrails-g42-g53.yaml` (mirror) — G42–G45, G53
2. `knowledge/commercial-rules/protection-guardrails.md` — G21–G41
3. `knowledge/commercial-rules/payment-plan-guardrails.md` — G11–G20
4. `knowledge/commercial-rules/subscription-guardrails.md` — G1–G10
5. `knowledge/12-commercial-rules.md` (this plugin's `knowledge/commercial-rules/`) — the 12 base Commercial Rules
6. The client's `manifest.yaml` and `02-calc/gate-report.md`
7. The client's `00-intake/session-log.md` (confirmed fact ledger)
8. The client's `00-intake/verbal-promises.md` (every row reflected)
9. The client's `02-calc/deal-card.md` (walk-away card)
10. The client's `02-calc/payment-plan-worksheet.yaml` (cadence, mobilisation)

## What it writes, where

- `<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/approval-request.md` — the packet the approver reads
- `<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/approval-record.yaml` — the binding decision record (written by the approver, not by this skill)

This skill produces the request and **stops**. It does not draft the
covering email. It does not create an envelope. It does not pre-fill
Zoho Sign. It does not move the artifact. It waits.

## The refusal protocol

This skill refuses to run until every gate G1–G53 has a recorded pass status, the fact ledger is confirmed by the SDR with every client-attributed statement traced to `sdr` / `document:<file>#<loc>` / `client-words`, zero `RESOLVE:` fields remain open, the validator is clean, the QA checklist is complete, the consistency map reconciles the proposal to the MSA to the Order Form, and the PDF is rendered with SHA-256 recorded.

Once those are present, it produces the approval packet and **stops**. It does not draft the covering email, does not create an envelope, does not pre-fill Zoho Sign. It waits for a recorded decision from the named approver.

## The approval packet (`approval-request.md`)

In this order:

1. **Client and reference** — `client.legal_name`, jurisdiction, `client.trade_licence_number`; `PROPOSAL-REF`; revision number
2. **Complete commercial table** — every line item, every cadence, every term, with units
3. **What the client pays at Kickoff** — mobilisation AED, % of contract value, cash-positive date
4. **What the client pays in total** — total contract value over term
5. **Term and cadence** — verbatim
6. **Edition and upgrade policy** — verbatim from `editions.yaml`
7. **Every gate G1–G53 with pass/fail and one-line reason** — the gate report is appended as a sub-section
8. **Every open `RESOLVE:` field at intake time and how it was closed** — sourced from `session-log.md`
9. **Every concession granted with its compensator** — names only; AED values come from the desk's `walk-away-authoring` log
10. **Fact ledger** — the confirmed origin-tagged table from `session-log.md`
11. **Peak cash exposure and cash-positive date** — from the desk-computed `exposure-calculator.yaml`
12. **Recovery balance at month 6 and month 12** — formulas named; the AED values are desk-computed
13. **Frozen PDF path and SHA-256 hash** — verified by this skill before writing
14. **Plain-English paragraph** — 3–5 sentences stating what the client is being asked to agree to, in non-technical language

## The approval record (`approval-record.yaml`)

Written by the named approver (or by a tool the approver operates).
This skill **never writes the approval record itself**. The record:

```yaml
approval:
  artifact_path: 04-issued/<PROPOSAL-REF>_RevN/<PROPOSAL-REF>_RevN_Sent.pdf
  approved_artifact_sha256: <hex>
  approver: "Ali Asghar Teli Muhammad Iqbal Teli"
  approved_at: 2026-08-04T13:00:00Z
  decision: approved | rejected | conditional
  conditions: []
  gates_snapshot:
    G1: { status: pass, note: "..." }
    G53: { status: pass, note: "approval-record matches hash" }
  resolved_fields:
    - { field: "client.registered_address", from: "RESOLVE", to: "..." }
  re_approval_required_if:
    - artifact_html_changes
    - artifact_pdf_changes
    - any_figure_changes
    - any_term_or_cadence_changes
    - any_clause_substitution
    - any_new_concession
    - validity_expires
    - approved_hash_mismatch
validity_days: 30
expires_at: 2026-09-03T13:00:00Z          # = approved_at + 30d
```

## Re-approval rules

Any of the following voids an existing approval and requires a fresh one:

- Any change to the HTML or the PDF (any artefact edit, any regeneration)
- Any figure change (a number in the commercial table moved)
- Any term or cadence change
- Any clause substitution (the MSA §A.9 edition text, the §C.6 VAT text, the cadence table)
- Any new concession (even if logged in `manifest.yaml: escalations`)
- An expired 30-day validity window
- A hash mismatch (the on-disk PDF doesn't match `approved_artifact_sha256`)

Re-approval is a **new** `approval-record.yaml`, never an edit of the
old one. A new approval packet (`approval-request.md`) accompanies it.

## What it refuses

- **Any missing preflight condition** — the gate refuses to even present a proposal for approval unless every item above is satisfied. Each item is reported individually with its result.
- **Stale hash** — refuses if the SHA-256 of the on-disk PDF doesn't match `frozen_sha256` in `manifest.yaml`. Cite G53.
- **Approver name other than the literal** — refuses to accept an approval signed by anyone other than `Ali Asghar Teli Muhammad Iqbal Teli`. Cite G53.
- **Approver signature via "agent on behalf of"** — refuses any record that does not name the approver directly. No delegation. No alternate.
- **Approval past 30 days** — refuses to use an expired `approval-record.yaml` even if all other fields are valid.
- **Approval tied to a non-existent artifact** — refuses if the PDF at `approved_artifact_sha256`'s path doesn't exist or is in `03-draft/` (must be in `04-issued/`).
- **Approved an artifact that has been edited since** — refuses if the on-disk PDF hash differs from `approved_artifact_sha256`.

## Escalation path

- **Preflight failure** — list the failed preflight, fix the upstream step, re-run. The gate does not paper over.
- **Below published floor discovered at this step** — `RESOLVE:` and route to the desk's `published-floor-authoring` skill. The gate refuses to produce an approval packet with a below-floor figure.
- **Approver unavailable** — the deal is paused. No alternate, no delegation. The skill emits a `RESOLVE:` placeholder and stops.
- **Conditional approval** — if `decision: conditional` with `conditions: [...]` that are unmet at the time the envelope would be created, `signature-dispatch` (G53) refuses.

## Sole approver

`Ali Asghar Teli Muhammad Iqbal Teli` — Company Manager, Scholarix
Global Consultants FZCO / SGC TECH AI. No delegation, no alternate, no
"approved by agent on behalf of." This is encoded as a literal string
in `knowledge/guardrails-g42-g53.yaml: approver.name` and re-stated
here. The approval gate enforces this in both directions: the request
names the approver; the record requires the same name.

## What this skill does NOT do

- It does not write the approval record — the approver does.
- It does not create the envelope — `signature-dispatch` does.
- It does not move the artifact to `04-issued/` — the drafting skill
  did that before this skill ran.
- It does not send email. The covering email is drafted by the SDR
  *after* the approval is recorded, never before, never by this skill.
