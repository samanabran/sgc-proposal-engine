# Subscription Proposal Runbook

The operating procedure for building a subscription-model (`SUB`) Odoo
proposal, end to end. Read this before opening a client folder. For project
(`PRJ`) or retainer (`RET`) models, the sequence is the same; only the
`assembly` block in the calc worksheet differs (see §5 below).

## 1. Intake

- Copy `02-clients/_SCAFFOLD` to `02-clients/{PREFIX}-{slug}/` (see
  `05-ops/naming-conventions.md`). Never copy a peer's folder — the scaffold
  is empty of numbers by design.
- Fill `00-intake/client-brief.yaml` from the discovery call. If a call
  happened, transcribe it to `00-intake/call-transcript-{date}.md`.
- Log every verbal commitment — a promised discount, a promised go-live date,
  a promised feature — in `00-intake/verbal-promises.md` the same day.
  Anything said aloud is scope.
- Determine `segment` (`startup_boutique` / `smb` / `mid_market`) from user
  count against `pricing/policy.yaml: segments.*.max_users`, and `vertical`
  from the client's industry. Read the matching file in
  `market-data/vertical-notes/` before going further — vertical rules (VAT
  class, regulatory bodies, portal gating) change what's in scope.

## 2. Calc

- Complete `02-calc/pricing-worksheet.yaml` in full, following
  `01-templates/calc/pricing-worksheet.template.yaml`. Work through it in
  order — `number_1_cost_to_serve` → `number_2_build` → `number_3_financing`
  → `assembly`. Do not skip to assembly.
- **Cost to serve** (`number_1_cost_to_serve`): licence cost from
  `pricing/saas-modules.yaml`, hosting from `pricing/hosting.yaml`, support
  labour and account management from `pricing/policy.yaml: cost_to_serve`.
  `platform_floor_aed` = `cts_total_aed` × `gates.platform_floor_multiplier`
  (1.25).
- **Build** (`number_2_build`): look up each work package's hours in
  `pricing/hour-lookup.yaml`. Add `documentation_hours` (≥
  `overlays.documentation_hours_min`, or 5% of dev hours, whichever is
  larger) and `qa_hours` (≥ `overlays.qa_hours_min`, or 8% of delivery hours).
  Rate = the segment's `blended_rate_aed` from `policy.yaml`. PM and
  contingency are the segment's `pm_pct` / `contingency_pct` applied to the
  subtotal.
- **Financing** (`number_3_financing`): mobilisation defaults to
  `gates.default_mobilisation_pct` (25%) of `build_value_aed` unless the
  client brief specifies otherwise. Uplift comes from
  `financing_uplift.months_{term}`; add `zero_mobilisation_surcharge` if
  mobilisation is 0.
- **Assembly**: Option A (with mobilisation) and Option B (zero
  mobilisation, uplift includes the surcharge). Year-1 client cost =
  mobilisation + 12 × monthly subscription (Option A) or 12 × monthly
  subscription alone (Option B, since mobilisation is folded into the rate).

## 3. Gate check

Run every gate in `commercial-rules/subscription-guardrails.md` (G1–G10)
against the completed worksheet and write `02-calc/gate-report.md`. See
`05-ops/validate.md` for the exact procedure.

**If any gate fails, stop.** Do not discount to force a pass — see
`AGENTS.md: On uncertainty`. Reduce scope (fewer modules, fewer users, a
lower support tier) and re-run the calc, or escalate in `manifest.yaml`.

## 4. Draft

Only once `gates_passed: true` in `manifest.yaml`: render each section in
`01-templates/proposal/` (§01–§13, see `_section-map.md`) into
`03-draft/{PROPOSAL-REF}_RevN/`. Pull tax/legal wording verbatim from
`clause-library/` — never paraphrase VAT, financing disclosure, clawback, or
term clauses.

## 5. Model-specific assembly notes

- **SUB (subscription)**: `assembly` block as described in §2 above —
  mobilisation + recurring subscription, two options.
- **PRJ (fixed project)**: `assembly` collapses to a single fixed-fee figure
  = `build_value_aed` (no recurring subscription line); financing block is
  typically unused unless the client requests staged payment (see
  `market-data/sources.md` payment-structure patterns — 40/40/20 is the
  SGCTECH default for fixed-fee delivery once discovery is complete).
- **RET (retainer)**: `assembly` uses a monthly retainer figure sized from
  `support-training.yaml` support tiers plus a capped usage pool; no
  mobilisation line.

## 6. QA checklist

Complete `04-review/qa-checklist.md`
(`01-templates/qa/pre-send-checklist.template.md`). Confirm:
`verbal_promises_logged`, `adoption_clause_included`, `clawback_included`,
`exclusions_confirmed` are all true in the worksheet/manifest, and every
number in the draft still traces to a `pricing/*.yaml` key.

## 7. Human review

A human reviewer reads `02-calc/gate-report.md` and the draft, and either
approves for issue or returns `04-review/reviewer-notes.md` with required
changes. No revision is issued without this step.

## 8. Issue

Move the approved draft to `05-issued/{PROPOSAL-REF}_RevN/`. Update
`manifest.yaml`: `stage: issued`, append the revision to `revisions`, set
`current_revision`. **`05-issued/` is immutable from this point** — a
correction is a new revision, never an edit. If a sent proposal must be
retracted, use `01-templates/comms/correction-notice.md`, not a silent edit.
