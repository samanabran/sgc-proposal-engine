# Clause: Edition and Upgrades

**Purpose**: state the Odoo edition being sold, its upgrade policy, and —
in client-facing language — its capability exclusions, before signature
(G36–G38). This is the highest-stakes clause in the library after VAT:
`failure-modes/known-defects.md` #18 documents "Odoo Enterprise licences"
being promised while Community was actually sold.

**requires_counsel_review**: false.

**When mandatory**: in the MSA/Order Form (§A.9), every deal, Community or
Enterprise, no exceptions — that is the binding "before signature, in
writing" disclosure G38 actually requires, and it is never omitted.

**In the sales proposal specifically** (per user decision 2026-08-04):
this clause is omitted by default — do not name "Community"/"Enterprise"
or list capability exclusions in the proposal unless the client or SDR
explicitly raises edition or upgrade questions. When asked, use this
clause verbatim and record the origin (`sdr` / `client-words`) per
`09-agent/fabrication-rules.md`. Proposal silence never substitutes for
the MSA's binding disclosure, and never justifies skipping it there.

**When it must NOT be used**: never substitute Enterprise language for a
Community deal, even in the "why us" framing.

---

## Approved verbatim text (positioning, edition-neutral)

> Your platform is built on Odoo, the world's most widely deployed
> open-source business platform, running on infrastructure managed
> entirely by SGC TECH AI. There are no per-user licence fees — which is
> precisely why we can absorb the implementation into your subscription
> rather than invoicing it upfront.

## Community-specific additions (mandatory when edition = community)

State explicitly, in the client-facing solution section (§06), not an
appendix:

> This proposal is built on Odoo Community edition. Community includes
> [editions.yaml: community.included list], with mobile-optimised browser
> access rather than a dedicated iOS/Android app. It does not include
> automated bank reconciliation, Studio (no-code customization), advanced
> tax configuration, multi-currency, or Odoo's own vendor upgrade service
> and official support — SGC TECH AI provides implementation and support
> directly instead. Upgrade policy: [editions.yaml:
> community.upgrade_policy], estimated at [upgrade_cost_estimate_hours]
> hours per major version.

**Mobile-access honesty line**: always write "mobile-optimised browser
access," never "iOS / Android app," when edition = community.

## Enterprise-specific additions (mandatory when edition = enterprise)

State the annual licence cost, that it is billed annually in advance, and
that mobilisation must cover the first year's licence fee in full (G40).
