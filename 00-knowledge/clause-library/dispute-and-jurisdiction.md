# Clause: Dispute Resolution and Jurisdiction

**Purpose**: state governing law and dispute forum. Depends directly on
the unresolved entity facts in `06-brand/entity/legal-identity.yaml`
(`licence_authority: RESOLVE` — IFZA and DIFC carry different court/
arbitration regimes and this clause cannot be finalized until that's
known).

**requires_counsel_review**: true.

> **DRAFT FOR COUNSEL REVIEW.** Do not include in an issued proposal until
> reviewed by UAE counsel AND until `legal-identity.yaml: licence_authority`
> is resolved — IFZA registration implies a different jurisdiction/court
> regime than DIFC registration, and this clause must not be finalized
> against a placeholder.

**When mandatory**: every proposal, once the underlying entity fact is
resolved.

**When it must NOT be used**: never issue a proposal with this clause
drafted against an unresolved `licence_authority` — the validate script
must fail loudly on this condition.

---

## Draft text (pending counsel review AND entity resolution)

> This agreement is governed by the laws of the United Arab Emirates
> [and, if applicable, the regulations of RESOLVE — IFZA or DIFC]. Any
> dispute arising under this agreement is subject to the exclusive
> jurisdiction of [RESOLVE — courts or arbitration forum applicable to the
> resolved licence authority].
