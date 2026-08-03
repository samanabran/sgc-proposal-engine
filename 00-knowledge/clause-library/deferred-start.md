# Clause: Deferred Start

**Purpose**: document the deferred-start cadence structure
(`payment-plans.yaml: cadences.deferred_start`) — a per-month surcharge
and platform-price increase for delaying kickoff, capped at 3 months and
requiring Commercial Desk approval.

**requires_counsel_review**: false.

**When mandatory**: any deal where kickoff is deliberately delayed at the
Client's request beyond signature.

**When it must NOT be used**: never exceed the 3-month cap
(`payment-plans.yaml: cadences.deferred_start.max_months`); never grant
without Commercial Desk approval logged in `manifest.yaml`.

---

## Approved verbatim text

> At the Client's request, kickoff is deferred by [N] month(s) from
> signature. This proposal's platform fee and financing terms reflect a
> deferred-start adjustment of [platform_adj_pct_per_month × N]% and
> [uplift_surcharge_pp_per_month × N] percentage points, applied because
> SGC TECH AI's cost-to-serve begins accruing before your deferred
> commencement date.
