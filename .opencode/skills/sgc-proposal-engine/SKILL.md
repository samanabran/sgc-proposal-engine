---
name: sgc-proposal-engine
description: >
  Run the SGC Proposal Engine — the governed, gated proposal pipeline for SGC TECH AI
  (Odoo subscription proposals for UAE real-estate brokerages). Use this skill whenever
  the user asks to create, price, gate-check, draft, validate, review, or issue a proposal,
  deal, quote, subscription, or contract; when they mention SGC, an SDR, a client intake,
  RFP/RFQ response, pricing worksheet, margin floor, walk-away card, gate report, or
  proposal revision; or when they say "run the engine", "connect the engine", "scaffold a
  client", "validate this deal", or "what stage is this deal". The skill embeds the engine's
  full operating contract (AGENTS.md + runbook + validate.py) so calling it runs the pipeline
  exactly as built: intake → risk assessment → calc → exposure → gate check → walk-away card
  → draft → QA → human review → issue. Trigger keywords: proposal, deal, sgc, subscription,
  quote, intake, RFP, pricing, gates, validate, SDR, Odoo, walkaway, margin.
---

# SGC Proposal Engine — pipeline runner

This skill is the **agent-side driver** for the SGC Proposal Engine at
`C:\sgc_proposal_engine`. The engine is not a code service — it is a governed sequence of
artifacts and hard gates that an agent executes. Invoking this skill = running that
sequence. You act as the SDR + agent; the human is Commercial Desk / sales leadership.

The authoritative contract lives in the engine repo. **Read it before acting** (Pre-flight
below). This file mirrors the contract so you execute correctly even before reading; when
in doubt, the engine repo wins.

---

## 1. Locate the engine root

Resolution order (first match wins):

1. `$SGC_PROPOSAL_ENGINE` env var, if set and valid.
2. Walk up from the current working directory: first ancestor containing both `AGENTS.md`
   and a `02-clients/` directory.
3. Fallback default: `C:\sgc_proposal_engine`.

Validate the root: it must contain `AGENTS.md`, `00-knowledge/`, `02-clients/`, `05-ops/validate.py`.
If none resolves, STOP — do not invent a pipeline. Tell the user the engine root is
unreachable.

> Use `python <root>/../../scripts/engine.py root` (the helper in this skill) or just check
> the directories directly. Helper location: this skill's `scripts/engine.py`.

## 2. Pre-flight — mandatory reads before ANY client-facing work

Read these seven, in order, BEFORE drafting a single line of client-facing prose
(AGENTS.md load order). Failure to read all seven is a contract violation.

1. `<root>/00-knowledge/PRECEDENCE.md` — resolution order; stricter rule wins; a ceiling is never an entitlement.
2. `<root>/00-knowledge/runbook/subscription-proposal-runbook.md` — the 9-stage pipeline (v2).
3. `<root>/00-knowledge/pricing/*.yaml` — rate-card, hour-lookup, policy, editions, payment-plans, hosting, support-training, saas-modules, concession-ladder, risk-security-matrix, phase2-catalogue.
4. `<root>/00-knowledge/commercial-rules/*` — guardrails G1–G41 (12-commercial-rules, subscription-guardrails, payment-plan-guardrails, protection-guardrails).
5. `<root>/07-protection/doctrine.md` — the cash-runway doctrine behind every gate.
6. `<root>/00-knowledge/market-data/vertical-notes/` — notes for the client's vertical.
7. `<client>/00-intake/client-brief.yaml` — this specific deal.

Plus: `<root>/AGENTS.md` (operating contract) and `<root>/05-ops/validate.md` (the gate
enforcement tool). For drafting, also read `<root>/01-templates/proposal/_section-map.md`
(§01–§13) and `<root>/06-brand/registry.yaml` (brand tokens — never anything outside it).

## 3. Command dispatch — map the request to a stage

| User says | You run |
|---|---|
| "new client / intake / scaffold" | Stage 0 (scaffold) + Stage 1 (intake) |
| "price / calc / cost it / how much" | Stages 2–3 (risk + calc) → **stop before presenting pricing** |
| "present pricing / send numbers" | Stages 4–5 (exposure + walk-away card + gate check) — card MUST predate any pricing conversation (G22) |
| "draft the proposal / write it" | Stage 6 (draft) — only if `gates_passed: true` |
| "QA / check / validate" | Stage 7 (QA) + **run validate.py** |
| "review / approve" | Stage 8 (human review) — **run validate.py first** |
| "issue / send it" | Stage 9 (issue) — **run validate.py first**, then move to `05-issued/` |
| "what stage / status" | Read `<client>/manifest.yaml` `stage` field + gate report |

Never skip stages. If the user asks for a later stage and prerequisites don't exist
(e.g. draft without a passing gate report), refuse and run the missing stages first —
this is the engine's whole point.

## 4. The pipeline — stage by stage

Client folder: `<root>/02-clients/{PREFIX}-{slug}/`. Naming per
`<root>/05-ops/naming-conventions.md` (e.g. `MRD-meridianview-realty`).

### Stage 0 — Scaffold
- `cp -r <root>/02-clients/_SCAFFOLD <root>/02-clients/{PREFIX}-{slug}`. **Never** copy a
  peer client folder — copy only `_SCAFFOLD`.
- Helper: `python <skill>/scripts/engine.py scaffold <name>`.

### Stage 1 — Intake
- **Entry:** scaffolded folder.
- Fill `00-intake/client-brief.yaml`: opportunity_id, client_legal_name, jurisdiction
  (mainland|free_zone), client_trn, decision_maker, sdr_owner, vertical, user count,
  edition_trigger fields. Edition: **Community by default** — Enterprise only if
  `editions.yaml` trigger conditions are met.
- Segment: derive from user count vs `policy.yaml: segments` (startup_boutique|smb|mid_market).
- Log every verbal promise the same day in `00-intake/verbal-promises.md`, each marked
  **PRICED / DEFERRED / EXCLUDED**.
- **Exit artifact:** completed `client-brief.yaml` + `verbal-promises.md`.
- **Hard stop:** no client-brief → cannot proceed to calc.

### Stage 2 — Risk assessment (BEFORE any pricing conversation)
- Score the client against `<root>/00-knowledge/pricing/risk-security-matrix.yaml`.
- Band: low | moderate | elevated | high | refuse. Band drives security instruments and
  feeds the walk-away card + mobilisation/cadence terms.
- **Exit artifact:** `02-calc/risk-assessment.yaml`. Record `risk_band` in manifest.
- **Hard stop:** risk band `refuse` → abort (walk away is a correct outcome, G30). Log in
  manifest, stop.

### Stage 3 — Calc (three-number model) → `02-calc/pricing-worksheet.yaml`
Worked formulas (authoritative detail in runbook §3):

- **Number 1 — CTS (monthly)**: `licences + hosting_allocation + tooling + support_labour + account_mgmt`
  - `hosting_allocation = 360 × (users ÷ 20)`; `support_labour = ceil(users/5) × 280`; `licences = 0` for Community.
  - `platform_floor = CTS × 1.25` (25% margin floor G23).
- **Number 2 — Build value**: `(total_hours × segment_rate) × (1+pm_pct) × (1+contingency_pct)`
  - `delivery_hours` from `hour-lookup.yaml` packages (simple/standard band) + documentation + qa + training.
  - `internal_build_cost = total_hours × 150`.
  - `segment_rate` MUST exist on `rate-card.yaml: roles.*`; **reject forbidden_rates (690)** (G9). Never invent an hourly rate.
- **Number 3 — Financing** (deferred structures only):
  - `deferred = build_value − mobilisation`; `recovery_total = deferred × (1+uplift)`; `recovery_monthly = recovery_total ÷ recovery_months`.
  - Disclose financing in exactly one line (clause-library/financing-disclosure.md).
- **Assembly**: `mobilisation = build_value × 0.33`; `platform_portion = max(CTS × 1.25, market_defensible_floor)`; `subscription = platform_portion + recovery_monthly`, round to nearest 50.
- **G12 ceiling**: `max_give_aed = revenue_baseline − (build_cost + CTS × term) ÷ (1 − min_margin)`; `applied_give = min(cadence_table_ceiling, max_give_aed)`. A cadence table value is a ceiling, not an entitlement.
- **Term**: build ≤ AED 8,000 w/ mobilisation → 12 mo; 8,000–20,000 → 24 mo; > 20,000 → 24–36 mo with mandatory mobilisation.
- **Options: exactly two, never three.** Option A = mobilisation paid. **Option B (zero upfront) is WITHDRAWN** (`payment-plans.yaml: withdrawn.option_b_zero_mobilisation`) — do not offer it.
- Sub < AED 2,500/mo → quarterly reviews only (defect #19).
- **Exit artifact:** complete `02-calc/pricing-worksheet.yaml`. Every number traces to a pricing YAML.

### Stage 4 — Exposure + walk-away card (BEFORE any pricing conversation, G21/G22)
- Compute all three exposures per option: **contractual** (clawback G4/G16), **cash**
  (mobilisation + cadence G3/G33/G34 — the runway-threatening one), **economic**
  (staged delivery / self-help instruments).
- Complete the walk-away deal card: `<root>/07-protection/walkaway/deal-card.template.md` → `02-calc/deal-card.md`. What you walk away from, at what number, and why.
- Set `walkaway_card_produced: true` in manifest — must predate first pricing conversation.
- **Hard stop:** no walk-away card → do not discuss price.

### Stage 5 — Gate check → `02-calc/gate-report.md`
- Evaluate **all 41 gates** (subscription / payment-plan / protection guardrails) against the completed worksheet.
- Any gate fails → **STOP**: reduce scope or work the concession ladder
  (`concession-ladder.yaml`). NEVER discount around a failed gate.
- Set `gates_passed: true` in manifest only when the report says so.
- **Exit artifact:** `gate-report.md` with all 41 evaluated, `gates_passed: true` required before draft.
- **Hard stop:** no passing gate report → no draft.

### Stage 6 — Draft → `03-draft/{PROPOSAL-REF}_RevN/`
- Render §01–§13 per `<root>/01-templates/proposal/_section-map.md`.
- Tax, legal, VAT, and edition wording **verbatim** from `00-knowledge/clause-library/` — never paraphrase. Clauses with `requires_counsel_review: true` are draft-only until human sign-off.
- **Hard stop:** never write a payment/security/guarantee clause outside the clause library; never claim VAT registration (G35); never call Community "Enterprise" (G36); never imply an iOS/Android app for Community.

### Stage 7 — QA + brand QA
- Complete `04-review/qa-checklist.md` and `04-review/brand-qa-checklist.md`.
- Every verbal promise reflected in the draft (PRICED → in scope, DEFERRED → scheduled, EXCLUDED → absent).
- Forbidden phrases check (also enforced by validate.py check 18): `bargain`, `not on our public list`, `will not be extended to any other brokerage`, `no VAT applies`, `VAT-registered`, `Odoo Enterprise` (if community), `iOS / Android app` (if community).
- Brand tokens only from `06-brand/registry.yaml`.

### Stage 8 — Human review
- **RUN validate.py FIRST** (see §6). Then present gate-report + draft to the human.
- Human approves, or returns `04-review/reviewer-notes.md` → fix and re-validate. No self-approval.

### Stage 9 — Issue → `05-issued/{PROPOSAL-REF}_RevN/`
- **RUN validate.py FIRST.** Move approved draft into `05-issued/` (immutable — never edit
  after issue; corrections = a new revision).
- Update `manifest.yaml`: stage, current_revision, revisions[] entry (ref, issued_date,
  path, status), `knowledge_version_used`, `verbal_promises_logged`, `adoption_clause_included`, `clawback_included`.

---

## 5. Absolute rules (AGENTS.md — encoded)

**NEVER**
- Write to `00-knowledge/`, `01-templates/`, `06-brand/`. Missing rate/module/hour/clause/brand token = escalation (see §7), never a silent invention.
- Invent a rate, hour figure, or percentage — every number traces to `00-knowledge/pricing/*.yaml`.
- Edit anything inside a client's `05-issued/` once sent — issue a new revision instead.
- Discount the recovery portion of a subscription (G11) — discounts apply to the platform portion only.
- Present a payment cadence without running the G12 margin-floor ceiling calc (a cadence value is a ceiling, not an entitlement).
- Draft payment/security/guarantee clauses outside the clause library.
- State or imply a tax registration SGC does not hold (G35): SGC is **not** VAT-registered and holds no TRN.
- Describe Odoo Community as Enterprise (G36).

**ALWAYS**
- Produce the walk-away deal card before any pricing conversation (G22).
- Complete `02-calc/pricing-worksheet.yaml` before drafting prose.
- Compute all three exposures (contractual, cash, economic) for every option (G21).
- Write `02-calc/gate-report.md` covering all 41 gates; any failure → STOP and escalate.
- Pin `knowledge_version_used` in manifest.yaml.
- Run validate.py before every human review and before every issue.
- Reduce scope, never price. On any uncertainty → escalate, don't guess.

## 6. Deterministic enforcement — validate.py

Run: `python <root>/05-ops/validate.py <root>/02-clients/{client}/`

- **Exit 0 = clean** — proceed.
- **Non-zero** = failure printed. Read the output; fix the listed issues; re-run until clean.
- 18 checks: pricing YAMLs parse & no forbidden_rates (1); worksheet completeness & rate
  traceability (2); PM/QA/doc/contingency present (3); hours ≥ ~9.2/user benchmark (4);
  §06 capabilities ↔ delivery_hours cross-ref (5); all 41 gates evaluated, no false blocks
  (6); worst-case G31 clears 25% margin floor (7); cash-positive within policy days (8);
  cadence ≥ quarterly-in-advance unless logged exception (9); mobilisation ≥ 33% and ≥
  triggered 3rd-party upfront (10); no VAT charged / no VAT-registration claim (11); edition
  declared + Community upgrade policy & exclusions (12); clawback on any deferred structure
  (13); entity fields resolved in `06-brand/entity/legal-identity.yaml` (14); brand tokens
  only from registry (15); verbal-promises logged & marked (16); evidence checklist complete
  (17); no forbidden phrases (18).

**Check-14 nuance:** entity fields in `06-brand/entity/legal-identity.yaml` are currently
UNRESOLVED (licence_authority, licence_number, registered_address, contact fields).
validate.py reports check 14 as `[BLOCKED — by design]` **and still exits 0** — it is an
*administrative* blocker (blocks issue, not commercially unclean), NOT a gate failure.
When you see it: proceed with drafting/review, log an escalation in manifest.yaml, flag it
prominently to the human, and **do not issue** until Commercial Desk supplies the entity
facts. Only non-zero exits from checks 1–13 / 15–18 block the deal itself.

Helper: `python <skill>/scripts/engine.py validate <client>` (locates root, runs
validate.py, annotates check-14, prints stage).

## 7. Escalation protocol

When a rate, module, hour figure, clause, brand token, or entity fact doesn't exist in the
knowledge layers:

1. **STOP** the pipeline at that point. Do not discount around it, do not substitute.
2. Log the gap in `<client>/manifest.yaml` under `escalations` (what's missing, where it was
   needed, what blocked).
3. Report to the human. Resume only after the gap is resolved by Commercial Desk.

If a risk- or protection-gate fails: reduce scope or use the concession ladder, re-run the
gate check. Walking away remains a correct outcome (G30).

## 8. Definition of done

A stage is done only when its exit artifact exists and its hard stop didn't fire. A deal is
"issued" only when: gate report passes, validate.py exit 0 (or only check-14 flagged +
escalated), human approved, revision moved to `05-issued/`, manifest updated.

Do not claim completion without: (a) the artifact, (b) validate.py evidence, (c) manifest
state updated.
