# Reviewer Notes — MRD-2026-SUB-01_Rev3

**Status: awaiting human review, and blocked on one open item below.**

## Commercial review

All 41 gates pass, plus market_test and budget_test. This is a clean,
low-risk, zero-cash-exposure deal — no notes on the numbers.

## Content review

The comparison to Rev1/Rev2 in §12 is a deliberate choice — flag for the
client-relationship owner whether that level of transparency about our
own prior mistakes is the right call for this specific client
relationship, or whether it should be softened before issue. This is a
judgment call, not a compliance requirement.

## Blocker — not a QA failure, a known open item

This revision **cannot be issued** until `06-brand/entity/legal-identity.yaml`
resolves `licence_authority`, `registered_address`, and `contact`. Two
things depend on this directly:

1. §09's dispute-and-jurisdiction clause is explicitly blocked pending
   this fact — IFZA and DIFC carry different jurisdiction regimes.
2. §13's signature block cannot show SGC's own signatory details.

This is by design, not an oversight — see `AGENTS.md` and the entity
file's own header. Route to Commercial Desk + Founder for resolution;
once resolved, re-run `05-ops/validate.py` (check #14) before issue.

---

Reviewer: _______________
Date: _______________
Result: [ ] Approved — proceed to issue   [x] Blocked pending entity resolution
