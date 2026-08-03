# Clause: Service Credit Guarantee

**Purpose**: give clients a bounded, honest guarantee structure —
service credits only, never cash refunds, aggregate-capped, with explicit
exclusions (G17, G28, G31).

**requires_counsel_review**: false.

**When mandatory**: every proposal states this table; individual rows are
optional per deal (e.g. no uptime guarantee if hosting isn't SGC-managed).

**When it must NOT be used**: never present any guarantee as a cash
refund; never state a credit without its cap; never omit the mandatory
exclusions.

---

## Approved verbatim text (guarantee table)

| Guarantee | Credit | Cap |
|---|---|---|
| Go-live timeliness | 5% of one month's subscription per week late | 2 months' subscription |
| Adoption | One free remediation/retraining session | 1 per term (see `adoption.md`) |
| UAT re-performance | Re-performed at no charge | Never a refund |
| Price lock | Rate fixed for the term (see `price-lock.md`) | — |
| Uptime (SGC-managed hosting only) | 1 month's subscription credit below 99.5% uptime | 1 month per year |
| Data portability | Unconditional export | — (see `data-portability.md`) |
| Exit | No exit fee; unrecovered clawback balance only | — |

> **Aggregate credit cap: 10% of annual contract value across all
> guarantees combined, per term.**

## Mandatory exclusions

> These guarantees are void where the triggering delay or shortfall is
> caused by the Client — including late provision of data files, delayed
> portal feed access, or unavailability of the Client's nominated system
> owner — and are void during any period of non-payment.
