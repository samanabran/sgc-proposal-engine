# Pricing Engine Exception — RVN-2026-SUB-01

RVN is priced in this flat-file knowledge repo
(`00-knowledge/pricing/*.yaml` + `05-ops/pricing_engine.py` +
`05-ops/validate.py`), **not** in the Odoo `sgc_proposal_engine` module
referenced as running on a VPS (`sgc.pricing.activity`,
`confidence_band`, banded gates G54-G62, `cost_rate_validated`).

This is a **named, accepted exception**, not an oversight: the agent
session that priced this deal had no network or SSH credentials to reach
that VPS, could not verify its state, and will not fabricate output from
a system it cannot query.

**Consequence**: every AED figure in this deal's worksheet, SOW, and
draft is provisional against that engine's cost basis
(`cost_rate_validated: False` there, per the user's own account) until a
human operator with access to both systems reconciles the two. Do not
treat this deal's numbers as validated against the governed engine's role
costs, bands, or gates — only against this repo's own 41-gate
`gate-report.md` and `validate.py` checks, which are real and have been
run.

**Resolution owner**: whoever has credentials to the VPS/Odoo instance —
not resolvable from this session.
