# Cost-Class Model (Classes A–D)

Source: `.omc/plans/pricing-engine-cost-class-model.md` (Rev.2, approved).
Replaces the scalar `hours ≈ k × users` model and its last incarnation,
`policy.yaml overlays.rollout_hours_per_user` (v2.1, deleted in this same
pass — see `CHANGELOG.md` pricing v3.0 entry). Every cost line in a
worksheet is classified into exactly one class below; the class is stated
in the worksheet. Mixing classes produced the Kallat Rev1 defect (120
rollout hours billed at the mid_market blended rate, 525 AED/hr, for work
that is structurally Class B).

## Class A — scope-driven, user-invariant (one-time)

Discovery, module config, workflow build, integrations, reporting,
migration engineering. `A_hours = Σ` over `(task × complexity)` from
`hour-lookup.yaml`. Independent of N — two clients configuring the same
scope incur the same A_hours at 5 users and at 400 users.

As of v2.1 (2026-08-05), `hour-lookup.yaml` also carries three entries
that are conditionally triggered by N crossing a documented threshold but
are still Class A once triggered (flat, not scaling further with N):
`bulk_user_import_csv` (N>25), `training_content_design_multiagent`
(N>10), and `migration_record_validation_signoff` (always present when a
migration is in scope, flat regardless of N — moved here from Class B,
see D-4 below). This is a genuine, documented step in A_hours at N=25/N=10
— not a violation of "A_hours invariant in N," but a discontinuity that
must be stated (same treatment as a Class C boundary — see T3).

## Class B — per-user, one-time

Account creation, role/permission assignment, per-agent sign-off,
individual onboarding, exception handling. The ONLY class carrying a
per-user multiplier. Charged ONCE per user at provisioning. Must NEVER
appear in a recurring line. See `class-b-task-inventory.yaml` for the
full task list, O/M/P estimates, `time_basis` (steady-state vs
first-unit, D-3), and per-task `role`.

**Rate-mix ceiling is per-task-role (D-5), not class-wide**: clerical
tasks (account creation, onboarding, sign-off, exception allowance, bulk
validation) are ceilinged at `rate-card.yaml: passthrough_band` (60–120
AED/hr — xlsx `Market Positioning` sheet row 7, D-6). Solution-design
tasks (`role_permission_design`) are priced at their own role
(`business_analyst`, 450 AED/hr, `rate-card.yaml:26`) — exempt from the
clerical ceiling, with the justification stated inline in
`class-b-task-inventory.yaml`. Applying an L2+ segment-blended rate
(e.g. 525 AED/hr `senior_consultant`) to any Class B task is a hard V2
failure unless a written per-task justification is attached — this is
the exact shape of Kallat Rev1's real, uncorrected defect.

**Record-level validation is Class A, not Class B (D-4)**: it scales
with the fixed migration record count, not with headcount — dividing a
fixed record pool by agent count and applying a per-agent learning curve
produced total validation hours that *fell* as headcount rose, a
category error. Class B retains only a small per-agent sign-off step
(`class-b-task-inventory.yaml: per_agent_signoff`), which correctly
scales with N.

**Bulk threshold**: above `n_bulk` (25, Grade D), per-user account
creation/onboarding is replaced by one Class A engineering line
(`hour-lookup.yaml: bulk_user_import_csv`) plus a much smaller Class B
per-user validation line (`class-b-task-inventory.yaml:
bulk_path_validation`). Modeled as an explicit crossover, not run
linearly to N=400.

**Learning curve**: Wright's law, `unit_time(n) = T1 × n^-b`,
`b = 0.15` (Grade D, bounded 0.05–0.25). `T1` is derived from each task's
`time_basis` (see `class-b-task-inventory.yaml` — most tasks here were
elicited as steady-state means, not first-unit times, and are converted
accordingly, D-3).

## Class C — banded, step-function (recurring)

Hosting, DB, backup, monitoring, support capacity. Steps at documented
boundaries: `hosting.yaml` Foundation ≤20 = AED 990/mo, Growth ≤50 =
AED 1,950/mo, Enterprise 51+ = AED 3,490/mo. Marginal infra cost within a
band is ZERO — model as steps, never as slope, never interpolate within
a band. Note the two-tier structure: sales bands step at 20/50/∞, but
true bundled infra cost (`policy.yaml: cost_to_serve.hosting_node_true_cost_aed`,
`hosting_node_user_capacity=20`) steps every 20 users — a bundled
cost-to-serve calculation must use the finer node-cost step, not the
coarser sales tier (`hosting.yaml`'s own COST BASIS NOTE already warns
of this).

`support-training.yaml: hypercare.hypercare_golive_support` (v2.1,
2026-08-05) is a one-time, time-boxed go-live support allocation — Class
A in timing (one-time, not perpetually recurring) but priced via the
support-capacity rate basis, scaling with 5-user pods (mirroring
`cost_to_serve.support_hours_per_5_users`'s own pod shape). Extracted
from the deleted overlay's bundled "hypercare support fanned across more
people" language. Never fold into the recurring `support:` block above
it in the same file.

## Class D — true per-user recurring vendor cost

Vendor per-seat licence cost only. For Odoo COMMUNITY this class is
EMPTY — LGPL, no seat licence, zero per-user vendor cost
(`editions.yaml:11`). The engine is structurally incapable of emitting a
Class D cost line for a Community deployment — all four corpus clients
(VGE, MRD, Kallat, Prosper) are Community by explicit, logged override of
the `users_above_15` Enterprise trigger. For Enterprise edition, D =
`editions.yaml:36` (72 AED/user/mo) or the `saas-modules.yaml` per-module
stack, nothing else.

## Price-vs-cost separation

SGC's own module list prices (`saas-modules.yaml` CRM/Sales/Accounting =
AED 60/user/mo) are Enterprise licence *prices*, not Community *costs*.
Under Community their underlying cost is ~0 — the highest-margin line in
the model and the natural discount lever (see `phase2-catalogue.yaml`'s
platform-capacity-fee restructure, replacing the flat `additional_user`
line). Cost and price are separate ledgers; a price line is never
justified by an absent cost line.

## Mandatory overlays on A+B (unchanged, Commercial Rules 4–8)

PM (15% standard / 10% startup segment, Rule 6), QA (% of dev effort,
base shown, Rule 5), Docs (every custom feature, Rule 4), Training
(billed once, no overhead stacked, Rule 8). Full effort price computed
before any discount line (Rule 1); discount never alters hours (Rule 2).
