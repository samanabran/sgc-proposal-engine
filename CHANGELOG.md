# Changelog — Knowledge Layer

Every change to `00-knowledge/` or `01-templates/` is logged here, in semver.
Client worksheets pin the version active when they were built
(`manifest.yaml: knowledge_version_used`); a later bump never silently
revalues an existing proposal.

## pricing v1.0 — 2026-08-03

Initial seed of the knowledge layer from `commercial-pricing-revised-v2.xlsx`
(v1→v2 revision, 22 Jul 2026) and the SGCTECH.AI Odoo Implementation Pricing
Strategy playbook (v1.0, 18 Jul 2026).

- Added `pricing/rate-card.yaml` — 13 roles, revised UAE specialist-boutique
  band (280–800 AED/hr).
- Added `pricing/saas-modules.yaml` — 18 Odoo modules + 4 Microsoft SKUs.
- Added `pricing/hosting.yaml` — 3 managed-hosting tiers (Contabo/Hetzner) +
  AWS pass-through reference rates.
- Added `pricing/support-training.yaml` — 3 support SLA tiers, 3 training
  formats, 3 cybersecurity services.
- Added `pricing/hour-lookup.yaml` — work-package → hour range, sourced from
  the pricing playbook's Excel-ready service catalog (Part 6).
- Added `pricing/phase2-catalogue.yaml` — deferred-scope items not costed in
  Phase 1 (AI Solutions catalog, advanced integrations).
- Added `pricing/policy.yaml` — segments, overlays, cost-to-serve
  coefficients, financing uplift, and the G-series commercial gates.
- Added `commercial-rules/12-commercial-rules.md` — verbatim from the xlsx
  Commercial Rules sheet (unchanged since v1).
- Added `commercial-rules/subscription-guardrails.md` — G1–G10, derived from
  `policy.yaml` gates plus the playbook's payment-structure guidance (Part 10).
- Added `market-data/benchmarks.yaml` + `sources.md` — UAE/GCC partner
  density, regional rate comparison, and industry pricing bands from the
  pricing playbook (Parts 2, 6, 7, 9).
- Added `market-data/vertical-notes/uae-real-estate.md` and
  `uae-tax-vat.md`.
- Added `failure-modes/known-defects.md` — seeded with the defect classes the
  gate structure exists to prevent (see file for the full list).
- Ported **VGE-vongeyern-realestate** in as the live worked example, Rev1 and
  Rev2 in `05-issued/`, Rev3 in `03-draft/`.

All figures in this release are sourced from the two documents above, now
archived in `_source-documents/`. Where the source used a range, `policy.yaml`
records the specific operating value SGCTECH commits to — see inline comments
for the rationale.
