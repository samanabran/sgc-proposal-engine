# Glossary

The repo's own vocabulary, plus the Odoo/UAE-specific terms used
throughout `00-knowledge/`. Plain-language definitions — for the
mechanical detail behind any of these, follow the cited source file.

## Repo vocabulary

**Gate (G1–G41)** — one of 41 mechanical pass/fail checks a subscription
worksheet must clear before drafting can begin, split across deal-shape
(`subscription-guardrails.md`, G1–G10), payment/cadence
(`payment-plan-guardrails.md`, G11–G20), and protection
(`protection-guardrails.md`, G21–G41) concerns. Run per the procedure in
`05-ops/validate.md`.

**Segment** — one of three client-size bands (`startup_boutique`, `smb`,
`mid_market`) determined by user count against `policy.yaml: segments.*.
max_users`. Each segment carries its own blended rate, PM percentage, and
contingency percentage — segment determination happens once, early, and
drives most of the rest of the calc.

**Blended rate** — the single AED/hour rate used to price build hours for
a given segment (280 / 395 / 525 for startup / smb / mid_market), pinned
in `policy.yaml: segments.*.blended_rate_aed` to a specific role in
`rate-card.yaml`. "Blended" because it stands in for a mix of consultant
levels at one representative rate, rather than billing each task at its
individual role's rate.

**Platform floor** — the minimum recurring subscription price a deal must
clear: `cts_total_aed × gates.platform_floor_multiplier (1.25)`. Enforced
by G1. This governs the recurring platform portion specifically — before
any build-recovery amount is even added — so that the ongoing fee alone
covers what it actually costs SGC to keep serving the client, independent
of whether the one-time build has been recovered yet.

**Cost-to-serve (CTS)** — SGC's internal, ongoing cost to keep a
subscription client served: hosting node cost, tooling, support labour,
and account management, from `policy.yaml: cost_to_serve`. This is a cost
figure (COGS), not a client-facing price — the client-facing hosting and
support prices live in `hosting.yaml` / `support-training.yaml` and are
typically higher, since they include margin.

**Mobilisation** — the upfront payment collected at kickoff on a
subscription deal, before recurring billing starts. Defaults to 33% of
`build_value_aed` (`policy.yaml: gates.default_mobilisation_pct`, G3).
Zero-mobilisation ("Option B") is currently withdrawn — see
`payment-plans.yaml: withdrawn`.

**Recovery** — the process of recouping the remaining (non-mobilisation)
build cost through the recurring subscription payments over the
contract term, with a financing uplift added. G2 checks that recovery
completes within the term, not after it.

**`knowledge_version_used`** — the semver value from `CHANGELOG.md`
pinned in a client's `manifest.yaml`, recording exactly which version of
`00-knowledge/` was active when that client's worksheet was built. Exists
so a later pricing change never silently revalues an in-flight proposal.

**Escalation** — the required response when a gate fails, a rate/module
isn't on the card, a budget is below the floor, a legal clause needs
paraphrase, or an issued proposal needs correcting: stop, log it in
`manifest.yaml: escalations`, and route to the Commercial Desk — never
improvise around it. Full trigger list in `04-governance/
escalation-triggers.md`.

**Revision** — a new, numbered version of a proposal (`_Rev1`, `_Rev2`,
...) issued to a client. `05-issued/` is immutable once a revision has
been sent; any correction is a new revision, never a silent edit to an
existing one.

## Odoo / UAE-specific terms

**TRN (Tax Registration Number)** — the unique number the UAE Federal Tax
Authority assigns to a business once it registers for VAT. Required in a
client's `manifest.yaml: client_trn`; a client without one may be below
the voluntary VAT registration threshold (`policy.yaml: vat.
voluntary_threshold_aed`, 187,500 AED).

**RERA (Real Estate Regulatory Agency)** — the UAE regulator governing
real estate brokerage licensing and listing compliance. Relevant to
scoping any real estate client's finance and commission-tracking
configuration — see `market-data/vertical-notes/uae-real-estate.md`.

**DLD (Dubai Land Department)** — the Dubai-specific land authority
overseeing property registration and, alongside RERA, brokerage licensing
within Dubai specifically. Relevant to portal/API integration
dependencies noted in the real estate vertical note.

**ZATCA (Zakat, Tax and Customs Authority)** — Saudi Arabia's tax
authority, responsible for e-invoicing and VAT compliance rules in KSA —
distinct from UAE VAT handling, which uses the UAE's own FTA rules. Not
currently in scope for this repo's real-estate-brokerage work-package
catalogue (`pricing/hour-lookup.yaml`), which is UAE-only; retained here
as a term in case a future GCC-scope deal needs it.

**VAT (Value Added Tax)** — the UAE's standard consumption tax, 5%
standard rate. **SGC TECH AI is not currently registered and charges no
VAT** (`policy.yaml: vat.registered: false`, `vat.charge_vat: false`) —
see `clause-library/vat-uae.md` and `vat-gross-up.md`. This is about
SGC's own registration status, distinct from a client's own VAT
registration, which is a separate fact captured in `client-brief.yaml`.

**VAT Designated Zone** — a specific free-zone classification under UAE
VAT law where qualifying goods transactions (not services, generally) can
receive VAT-free treatment under narrow conditions. Being in "a free
zone" generally does **not** by itself exempt a business from VAT
(`policy.yaml: vat.free_zone_exempt: false`) — Designated Zone status and
transaction type must be confirmed before any VAT-free treatment is
assumed. See `market-data/vertical-notes/uae-tax-vat.md`; always flag for
human/legal review regardless.

## New in v2

**Edition (Community / Enterprise)** — which Odoo licensing tier a build
uses. Community is the default (`editions.yaml: default_edition`), zero
per-user licence cost, with real capability exclusions that must be
disclosed in writing (G38). Enterprise is a priced, conditional upgrade,
triggered only when the client brief trips a specific
`editions.yaml: enterprise.trigger_conditions` item.

**Exposure (contractual / cash / economic)** — the three distinct risks a
deal carries, computed separately for every option (G21). Contractual is
the unrecovered build principal (protected by clawback). Cash is the peak
point where SGC has spent more delivering than it has collected
(protected by mobilisation and cadence — the one that actually threatens
runway). Economic is the unrecovered internal delivery cost (protected by
staged delivery). See `07-protection/exposure/exposure-model.md`.

**Concession / Compensator** — a concession is anything that reduces
what SGC collects on a deal (a discount, a waived mobilisation, a free
module); a compensator is what's traded for it, priced to equal or exceed
the concession's value, per `pricing/concession-ladder.yaml`. An
unlogged concession — one without matching compensators recorded in
`manifest.yaml` — is void (G14).

**Walk-away deal card** — a one-page artifact (three prices, total give
available, risk band, top compensators, abort criteria, incumbent
benchmark) produced before any pricing conversation with a client (G22).
See `07-protection/walkaway/deal-card.template.md`.

**Risk band** — one of five bands (`low` / `moderate` / `elevated` /
`high` / `refuse`) a client scores into via
`pricing/risk-security-matrix.yaml`, determining which security
instruments (mobilisation depth, deposit, PDCs) a deal requires before it
can proceed.

**Cadence** — the payment schedule a client is billed on (quarterly in
advance is the current minimum, G33). Each cadence in
`pricing/payment-plans.yaml: cadences` carries its own price adjustment,
which is always a ceiling (G12), never an entitlement — the margin floor
beneath it binds if tighter.

**Absolute floor** — a rule no approver, at any authority level, may
override: the 25% margin floor (G23), unconditional client data export
(G18), mandatory clawback on any deferred structure (G16), and tax/
registration accuracy (G35). See `00-knowledge/PRECEDENCE.md`.
