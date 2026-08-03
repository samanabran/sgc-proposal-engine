# Clause: IP and Configuration

**Purpose**: state data/IP ownership correctly (G26) — the Client owns
its data unconditionally; SGC's claim over configuration IP is limited
and time-bound, and must be checked against LGPL obligations on any
Community/OCA module used (`editions.yaml: community.lgpl_note`).

**requires_counsel_review**: true.

> **DRAFT FOR COUNSEL REVIEW.** Do not include in an issued proposal until
> reviewed by UAE counsel, specifically for LGPL compatibility — an SGC
> claim of ownership over configuration built on LGPL-licensed modules may
> not be enforceable as drafted.

**When mandatory**: every proposal.

**When it must NOT be used**: never claim SGC owns the Client's data;
never claim configuration IP ownership without the LGPL caveat when
Community edition or third-party OCA modules are in scope.

---

## Draft text (pending counsel review)

> The Client owns all of its own data unconditionally, at all times (see
> `data-portability.md`). SGC TECH AI retains ownership of the specific
> configuration and customization work built for the Client until the
> implementation value is fully recovered per this agreement's term,
> subject to the licensing terms of any underlying open-source components
> (see `editions.yaml: community.lgpl_note` where applicable).
