# Worked Example — 5-User Real Estate Brokerage, 24-Month Subscription

Anonymised, fully-worked `SUB` (subscription) calc, end to end, for a
5-user boutique real estate brokerage. Use this as a template for any
`startup_boutique` subscription deal — the arithmetic pattern is the point,
not the specific numbers. Every figure below cites its source file and key;
if you copy this example for a live deal, re-pull each cited value from the
current `00-knowledge/pricing/*.yaml` rather than hardcoding what's written
here — this file is not itself a pricing source.

**Do not use this file as a source of truth for pricing.** It is a worked
illustration. The only sources of truth are `00-knowledge/pricing/*.yaml` and
`00-knowledge/commercial-rules/*`.

---

## 0. Client snapshot (fictional, anonymised)

- 5 named users: 2 agents, 1 broker/principal, 1 finance/admin, 1 office
  manager.
- Vertical: UAE real estate brokerage (not a developer — see
  `market-data/vertical-notes/uae-real-estate.md`, which explicitly warns
  against sizing a brokerage against the developer-scale
  `industry_pricing_bands_aed.real_estate_developer` band).
- Scope: CRM + Sales + Accounting, including RERA/DLD-adjacent trust
  accounting and commission handling (per the vertical note — this is a
  finance-configuration requirement, not a CRM feature).
- Model: `SUB`, 24-month term.
- Current spend (client-stated, from `00-intake/client-brief.yaml` in a real
  deal): ~AED 3,600/mo across a generic real-estate CRM SaaS tool and
  separate accounting software. **This is a client-brief fact, not a
  `pricing/*.yaml` value** — flagged here because it feeds G9 below.
- No previously rejected budget on file (`budget_rejected_aed`: none) —
  relevant to G10 below.

## 1. Segment determination

`pricing/policy.yaml: segments.startup_boutique.max_users` = 10. 5 users ≤
10 → **segment = `startup_boutique`**, `blended_rate_aed` = 280,
`pm_pct` = 0.10, `contingency_pct` = 0.05 (`policy.yaml: segments.
startup_boutique`). 280 AED/hr is pinned to `rate-card.yaml:
roles.startup_consultant.rate_aed_hr` (280) — confirmed matching, no drift
(see `failure-modes/known-defects.md #1` for why this cross-check matters).

## 2. `number_1_cost_to_serve`

All inputs from `policy.yaml: cost_to_serve`.

| Component | Basis | Source key | AED/mo |
|---|---|---|---|
| Hosting node (internal true cost) | 5 users fits inside one node (capacity 20) | `cost_to_serve.hosting_node_true_cost_aed` | 360 |
| Tooling | flat per client | `cost_to_serve.tooling_flat_aed` | 50 |
| Support labour | `support_hours_per_5_users` (1) × 5 users = 1 hr/mo × `support_rate_aed` (280) | `cost_to_serve.support_hours_per_5_users`, `cost_to_serve.support_rate_aed` | 280 |
| Account management | 5 users → `tier_5` bracket | `cost_to_serve.account_mgmt_aed.tier_5` | 100 |
| **Monthly cost-to-serve** | | | **790** |

`cts_total_aed` is a **monthly** figure — it and `platform_floor_aed` are
compared against the monthly recurring subscription price in G1 (see
`commercial-rules/subscription-guardrails.md`, G1), not against term-length
build/financing totals. `cts_total_aed` = **790 AED/mo** (the table above).

`platform_floor_aed` = `cts_total_aed` × `gates.platform_floor_multiplier`
(1.25) = 790 × 1.25 = **987.5 AED/mo**, rounded to **988 AED/mo**.

## 3. `number_2_build`

### 3a. Work-package hours

Picked from `pricing/hour-lookup.yaml: work_packages`, medium band unless a
vertical note gives an explicit reason to move (per hour-lookup.yaml's own
guidance: "pick medium unless the client brief gives a specific reason").

| Work package | Band | Reason for band | Hours |
|---|---|---|---|
| `discovery_workshop` | medium | default | 12 |
| `project_kickoff` | medium | default | 8 |
| `requirements_workshops` | medium | default | 26 |
| `finance_setup` | **high** | `vertical-notes/uae-real-estate.md`: "expect finance_setup hours to run toward the high end... even for a small user count" (trust accounting + commission-linked journals) | 60 |
| `uae_vat_localization` | medium | default | 14 |
| `sales_crm_configuration` | medium | default | 24 |
| **Work-package subtotal** | | | **144** |

No `inventory_warehouse_setup` or `purchase_configuration` — out of scope
(CRM + Sales + Accounting only).

Complexity/risk/industry/customization multipliers
(`hour-lookup.yaml: complexity_multiplier_reference`): all set to **1.00
(low)** — a 5-user brokerage on a standard module set has no elevated
complexity, risk, industry, or customization factor beyond the finance_setup
band already elevated above. No additional loading applied.

### 3b. Overlays

Training billed once, in the build, not the recurring line (Commercial
Rule 8, `12-commercial-rules.md`): `overlays.training_sessions` (2) ×
`overlays.training_hours_per_session` (2) = **4 hours**, folded into the
delivery-hour base below.

*Judgment call*: the runbook doesn't specify whether bundled training hours
count toward the "delivery hours" base that documentation/QA percentages
are computed from. This example includes them (148 = 144 + 4) on the
reasoning that training is billable build effort like any other work
package and should carry its share of documentation/QA/PM/contingency
rather than being a silent add-on. Flag if the Commercial Desk has a
different convention.

Delivery hours = 144 (work packages) + 4 (training) = **148**

`documentation_hours` ≥ max(`overlays.documentation_hours_min` = 2, 5% ×
148 = 7.4) → binding value is 7.4, rounded up to **8 hours** (whole-hour
billing; rounding convention is an operating choice, not a sourced rule).

`qa_hours` ≥ max(`overlays.qa_hours_min` = 3, 8% × 148 = 11.84) → binding
value 11.84, rounded up to **12 hours**.

### 3c. Subtotal, PM, contingency

Total billable hours = 148 + 8 (docs) + 12 (QA) = **168 hours**

Rate = 280 AED/hr (`policy.yaml: segments.startup_boutique.blended_rate_aed`)

- Subtotal = 168 × 280 = **47,040 AED**
- PM (10%, startup segment, `segments.startup_boutique.pm_pct`) = 0.10 ×
  47,040 = **4,704 AED**
- Contingency (5%, `segments.startup_boutique.contingency_pct`) = 0.05 ×
  47,040 = **2,352 AED**

**`build_value_aed` = 47,040 + 4,704 + 2,352 = 54,096 AED**

*Sanity-check aside*: `market-data/benchmarks.yaml: sgc_packages.starter`
lists a 5-user CRM+Sales+Accounting package at AED 12,900. This worksheet
prices well above that because it carries real-estate-specific trust/
commission accounting scope (`finance_setup` at the high band) that the
generic starter package doesn't include. Don't substitute the package price
for the worksheet — they answer different questions.

## 4. `number_3_financing`

Mobilisation default = `gates.default_mobilisation_pct` (0.25) ×
`build_value_aed` (54,096) = **13,524 AED**.

Recovery still owed after mobilisation (Option A) = 54,096 − 13,524 =
40,572 AED.

Uplift: `financing_uplift.months_24` = **0.12**.

Amount to recover through the subscription, with uplift = 40,572 × 1.12 =
**45,440.64 AED**, spread evenly across the 24-month term = 45,440.64 / 24 =
**1,893.36 AED/mo** (build-recovery component of the monthly subscription).

Recurring SaaS + hosting pass-through (added to the build-recovery
component to form the full monthly subscription fee):

| Item | Basis | Source key | AED/mo |
|---|---|---|---|
| Odoo CRM | 5 users × 18 | `saas-modules.yaml: modules.erp.odoo_crm.price_aed_mo` | 90 |
| Odoo Sales | 5 users × 20 | `saas-modules.yaml: modules.erp.odoo_sales.price_aed_mo` | 100 |
| Odoo Accounting | 5 users × 22 | `saas-modules.yaml: modules.erp.odoo_accounting.price_aed_mo` | 110 |
| Hosting (Foundation, ≤20 users) | dedicated node, not per-seat | `hosting.yaml: tiers.foundation.price_aed_mo` | 990 |
| **Recurring pass-through subtotal** | | | **1,290** |

## 5. Assembly — Option A vs Option B

### Option A — with mobilisation (25%)

- Mobilisation (due at signing): **13,524 AED**
- Monthly subscription = build-recovery (1,893.36) + recurring pass-through
  (1,290) = **3,183.36 AED/mo**
- Year-1 client cost = 13,524 + (12 × 3,183.36) = 13,524 + 38,200.32 =
  **51,724.32 AED**
- 24-month total = 13,524 + (24 × 3,183.36) = 13,524 + 76,400.64 =
  **89,924.64 AED**

### Option B — zero mobilisation

Uplift includes `financing_uplift.zero_mobilisation_surcharge` (0.03) on
top of the term uplift: total uplift = 0.12 + 0.03 = **0.15**. No
mobilisation is collected, so the *full* build value is recovered through
the subscription rate.

- Amount to recover with uplift = 54,096 × 1.15 = **62,210.40 AED**
- Monthly build-recovery = 62,210.40 / 24 = **2,592.10 AED/mo**
- Monthly subscription = 2,592.10 + 1,290 = **3,882.10 AED/mo**
- Year-1 client cost = 12 × 3,882.10 = **46,585.20 AED**
- 24-month total = 24 × 3,882.10 = **93,170.40 AED**

**Trade-off, shown by the numbers**: Option B has no upfront cash
requirement but costs more over the full term (93,170.40 vs. 89,924.64 —
the zero-mobilisation surcharge is real money, not a formality). Year-1
cash cost is lower under Option B (46,585.20 vs. 51,724.32) because the
mobilisation lump sum is spread instead of front-loaded — useful framing
for a client who is cash-conscious in year 1 but will pay more in total.

## 6. Gate report — G1 through G10

Worked against Option A figures (the more conservative of the two on
gates that reference `year1_client_cost_aed`).

**G1 — Platform floor.** Recurring subscription price (Option A,
3,183.36 AED/mo) ≥ `platform_floor_aed` (988 AED/mo, from §2 above).
**PASS** (3,183.36 ≥ 988; the recurring fee alone clears the monthly
cost-to-serve floor with more than 3x headroom, before any build-recovery
component is even counted separately).

**G2 — Term ≥ recovery.** Mobilisation (13,524, collected at signing) +
recovery_total (45,440.64, collected in 24 equal instalments) is
structured to complete exactly at month 24 of a 24-month term.
**PASS** (recovery completes at month 24 ≤ term_months 24 — no slack, but
no shortfall either; see note below).

*Note*: this is a tight pass, not a comfortable one — recovery completes on
the last day of the term. If the client later asks to shorten the term, G2
must be re-run; it will fail unless mobilisation or the uplift structure
changes. This is the situation `known-defects.md #9` describes.

**G3 — Rate provenance.** Every figure above cites a `pricing/*.yaml` key
(280 AED/hr → `policy.yaml segments.startup_boutique.blended_rate_aed`;
module prices → `saas-modules.yaml`; hosting → `hosting.yaml`; CTS
components → `policy.yaml cost_to_serve.*`; uplift → `policy.yaml
financing_uplift.*`; mobilisation % → `policy.yaml gates.
default_mobilisation_pct`). **PASS**.

**G4 — Documentation coverage.** documentation_hours (8) ≥ max(2, 5% ×
148 = 7.4). **PASS** (8 ≥ 7.4).

**G5 — QA coverage.** qa_hours (12) ≥ max(3, 8% × 148 = 11.84).
**PASS** (12 ≥ 11.84).

**G6 — PM coverage.** PM line (4,704) = 10% × subtotal (47,040) for the
startup segment. **PASS** — matches `segments.startup_boutique.pm_pct`
exactly by construction.

**G7 — Segment rate integrity.** blended_rate_aed used (280) matches
`policy.yaml segments.startup_boutique.blended_rate_aed` (280), and the
5-user count correctly sits under `max_users: 10` for this segment (not
mis-defaulted to `smb` — see `known-defects.md #12`). **PASS**.

**G8 — Gross margin floor.** internal_build_cost_aed = total billable
hours (168) × `cost_to_serve.internal_consultant_cost_aed_hr` (150) =
**25,200 AED**. Margin = (build_value_aed − internal_build_cost_aed) /
build_value_aed = (54,096 − 25,200) / 54,096 = 28,896 / 54,096 = **53.4%**.
**PASS** — well above the 30% floor and the 35% target
(`policy.yaml gates.min_gross_margin`, `gates.target_gross_margin`).

**G9 — Market test.** year1_client_cost_aed (51,724.32) ≤
incumbent_benchmark_aed_mo (3,600, client-stated) × 12 ×
`gates.max_multiple_of_incumbent` (1.30) = 3,600 × 12 × 1.30 = **56,160**.
**PASS** (51,724.32 ≤ 56,160; roughly 8% of headroom under the ceiling —
worth flagging to the client as "15–20% under mid-tier" positioning per
`market-data/benchmarks.yaml: strategic_position`, not as a wide-margin
pass).

**G10 — Budget test.** No `budget_rejected_aed` on file for this client
brief. **PASS (not triggered)** — gate only fires when a prior rejected
budget exists to check against.

**Result: `gates_passed: true`, 10/10.** This worksheet is clear to move
from calc to draft per `runbook/subscription-proposal-runbook.md` §3–4.

## 7. What to change for a different deal

- More users → re-run segment determination first (§1); a `smb`-segment
  deal changes the rate, PM%, and every downstream number, not just the
  headcount-scaled lines.
- Different vertical → re-check the matching `market-data/vertical-notes/`
  file before reusing this hour allocation; the `finance_setup` high-band
  justification here is real-estate-specific.
- Shorter term → G2 above is already a tight pass at 24 months; a 12- or
  18-month term will very likely fail G2 at this build value unless
  mobilisation is raised. Re-run the recovery check, don't assume it still
  clears.
