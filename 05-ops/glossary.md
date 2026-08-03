# Glossary

The repo's own vocabulary, plus the Odoo/UAE-specific terms used
throughout `00-knowledge/`. Plain-language definitions — for the
mechanical detail behind any of these, follow the cited source file.

## Repo vocabulary

**Gate (G1–G10)** — one of ten mechanical pass/fail checks a subscription
worksheet must clear before drafting can begin. Each gate enforces one or
more of the `12-commercial-rules.md`. Defined in `commercial-rules/
subscription-guardrails.md`; run per the procedure in `05-ops/validate.md`.

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

**Platform floor** — the minimum combined value (build value + cost-to-
serve) a deal must clear: `cts_total_aed × gates.platform_floor_multiplier
(1.25)`. Enforced by G1. Exists to make sure a deal covers what it
actually costs SGC to serve the client before any margin is even
discussed.

**Cost-to-serve (CTS)** — SGC's internal, ongoing cost to keep a
subscription client served: hosting node cost, tooling, support labour,
and account management, from `policy.yaml: cost_to_serve`. This is a cost
figure (COGS), not a client-facing price — the client-facing hosting and
support prices live in `hosting.yaml` / `support-training.yaml` and are
typically higher, since they include margin.

**Mobilisation** — the upfront payment collected at signing on a
subscription deal, before recurring billing starts. Defaults to 25% of
`build_value_aed` (`policy.yaml: gates.default_mobilisation_pct`) unless
the client brief specifies otherwise or the client opts for zero
mobilisation (which carries a surcharge instead — `financing_uplift.
zero_mobilisation_surcharge`).

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
authority, responsible for e-invoicing and VAT compliance rules in KSA.
Referenced in `pricing/hour-lookup.yaml: work_packages.ksa_zatca_advisory`
for any GCC deal touching Saudi operations — distinct from UAE VAT
handling, which uses the UAE's own FTA rules.

**VAT (Value Added Tax)** — the UAE's standard consumption tax, 5%
(`policy.yaml: vat.standard_rate`), applicable UAE-wide, mainland and
free zone alike, unless a supply is specifically zero-rated or exempt.
Always quoted as a separate line, never folded into the headline price —
see `clause-library/vat-uae.md`.

**VAT Designated Zone** — a specific free-zone classification under UAE
VAT law where qualifying goods transactions (not services, generally) can
receive VAT-free treatment under narrow conditions. Being in "a free
zone" generally does **not** by itself exempt a business from VAT
(`policy.yaml: vat.free_zone_exempt: false`) — Designated Zone status and
transaction type must be confirmed before any VAT-free treatment is
assumed. See `market-data/vertical-notes/uae-tax-vat.md`; always flag for
human/legal review regardless.
