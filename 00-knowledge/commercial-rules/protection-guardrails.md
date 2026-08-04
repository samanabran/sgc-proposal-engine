# Protection Guardrails — G21–G41

Govern exposure, portfolio risk, legal defensibility, and edition/tax
honesty. See `PRECEDENCE.md` and `07-protection/doctrine.md`.

| Gate | Rule | Test | Owner |
|---|---|---|---|
| **G21** | All three exposures computed before issue | Contractual, cash, and economic exposure (`07-protection/exposure/exposure-model.md`) calculated for every option in the worksheet | SDR |
| **G22** | Walk-away deal card produced before any pricing conversation | `07-protection/walkaway/deal-card.template.md` completed and reviewed before the client hears a number | SDR |
| **G23** | Absolute margin floor 25% | No approver, at any authority level, may approve below `policy.gates.absolute_margin_floor` | Commercial Desk (absolute floor — see PRECEDENCE.md) |
| **G24** | Portfolio limits checked before signature | `07-protection/exposure/portfolio-limits.yaml` — peak cash exposure, concurrent deferred builds, concentration limits all checked against the live portfolio, not just this deal in isolation | Finance |
| **G25** | Liability capped | 12 months' fees paid; indirect/consequential damages excluded (`clause-library/liability-cap.md`, `requires_counsel_review: true`) | Counsel |
| **G26** | IP ownership stated correctly | Client owns data unconditionally; SGC owns configuration IP only until recovery completes — verified against LGPL obligations (`editions.yaml: community.lgpl_note`, `clause-library/ip-and-configuration.md`) | Counsel |
| **G27** | No named individual consultants | Every proposal reserves a substitution right (`clause-library/key-person-and-subcontractor.md`) — never promise "the consultant who built your system" by name as a guarantee | Commercial Desk |
| **G28** | Guarantees suspend on client-caused delay and non-payment | `clause-library/service-credit-guarantee.md` mandatory exclusions | Commercial Desk |
| **G29** | Evidence file complete before go-live sign-off | `07-protection/evidence/evidence-file-standard.md` checklist fully checked | SDR |
| **G30** | Abort criteria are absolute | An SDR who walks away on a triggered abort criterion (`07-protection/abort/abort-criteria.md`) acted correctly and is not penalised for the lost deal | Sales leadership |
| **G31** | Worst-case gate | Concessions + maximum guarantee-credit exposure, applied together, must still leave margin above 25%; combined ceiling is 12% of contract value (`payment-plans.yaml: hard_caps.combined_give_plus_guarantee_cap_pct`) | Finance |
| **G32** | Cash-positive within 30 days of kickoff | `policy.gates.cash_positive_within_days` | Finance |
| **G33** | Minimum cadence quarterly-in-advance | Until liquid reserves reach 3 months opex (`07-protection/exposure/portfolio-limits.yaml: runway.target_months`) | Finance |
| **G34** | Mobilisation minimum 33%, never less than any triggered third-party upfront cost | E.g. Enterprise annual licence prepayment (G40) sets a higher floor than 33% alone | Commercial Desk |
| **G35** | Never state or imply a tax registration status SGC does not hold | `policy.yaml: vat.registered: false` — no proposal may say "VAT-registered" or charge VAT while this is false. The sales proposal says nothing about VAT by default (per user decision 2026-08-04); the MSA (§C.6) always carries the accurate, binding position regardless | SDR + validate script (absolute floor — see PRECEDENCE.md) |
| **G36** | Edition declared at intake, never misdescribed | Community is never described as Enterprise, in writing or verbally, regardless of what the client hopes for | SDR |
| **G37** | Community upgrade policy stated explicitly | Every Community deal's MSA/Order Form (§A.9) states `editions.yaml: community.upgrade_policy` — silent upgrade obligations are prohibited there. The sales proposal states it only if the client or SDR asks (per user decision 2026-08-04, see `clause-library/edition-and-upgrades.md`) | SDR |
| **G38** | Community exclusions disclosed in writing before signature | Satisfied by the MSA/Order Form (§A.9), which always carries it — not buried in an appendix. The client-facing proposal §06 omits it by default and states it only if asked; proposal silence never substitutes for the MSA's disclosure or excuses omitting it there | SDR |
| **G39** | Third-party/OCA modules assessed for maintenance status | Abandoned modules excluded from scope regardless of feature fit | SDR + Solution Architect |
| **G40** | Enterprise proposals require mobilisation covering full annual licence prepayment | `editions.yaml: enterprise.mobilisation_must_cover_licence` | Finance |
| **G41** | Demo environment matches the edition being sold | Never demo Enterprise features to close a Community deal | SDR |

## On a failed gate

G23, G18, G16, G35 are absolute floors per `PRECEDENCE.md` — no
escalation path overrides them, only a scope or structure change that
actually clears them. G30 (abort criteria) is the one gate whose "failure"
is the correct outcome: walking away from a deal that trips an abort
criterion is not a defect to fix, it's the system working.
