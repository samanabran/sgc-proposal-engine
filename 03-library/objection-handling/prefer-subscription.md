# Objection: "We'd rather pay a one-time fixed project fee than subscribe"

## Why it comes up

Subscription pricing is unfamiliar to buyers used to thinking of software
implementation as a one-time capital project — pay once, own it, done.
A recurring line item on the P&L reads as an ongoing liability even when
the total cost of ownership is comparable or lower.

## The SGC response

Both models exist for a reason, and the difference is mechanical, not just
a sales preference — walk the client through what each model actually
does to the numbers.

**Fixed project (`PRJ`)**: `assembly` collapses to a single fixed fee =
`build_value_aed`, full stop — no recurring subscription line
(`runbook/subscription-proposal-runbook.md` §5). Payment is typically
staged 40/40/20 once discovery is complete
(`market-data/sources.md` payment-structure patterns, cited in the
runbook). That means **40% of the total build cost is due upfront**, before
go-live, with no financing uplift charged — the client pays the raw
effort-based price and nothing more.

**Subscription (`SUB`)**: the build cost isn't collected as one lump sum.
Instead, mobilisation defaults to 25% of build value at signing
(`policy.yaml: gates.default_mobilisation_pct`), and the remainder is
recovered across the term with a **financing uplift** on top:
`financing_uplift.months_12` = 6%, `months_18` = 9%, `months_24` = 12%
(`policy.yaml: financing_uplift`). If the client wants zero mobilisation
at all, add `zero_mobilisation_surcharge` (3%) — spreading 100% of the
build cost into the monthly rate costs more than spreading 75% of it.

The trade-off in one line: **PRJ has a higher cash outlay sooner and a
lower total cost; SUB has a lower cash outlay sooner and a higher total
cost** — the uplift percentages above are the explicit price of that
cash-flow flexibility, not a hidden markup. There's also a floor
underneath the subscription rate: `platform_floor_aed` = `cts_total_aed` ×
`gates.platform_floor_multiplier` (1.25) — the monthly rate has to cover
SGC's actual cost to keep serving the account (hosting, support labour,
account management) with margin, which is also why SUB bundles ongoing
support and SaaS licensing into one line rather than billing them
separately later.

If the client's real objection is "we don't want an ongoing relationship,"
PRJ is the right answer — say so plainly rather than arguing for
subscription. If the objection is really about a lump-sum cash outlay,
SUB is the better fit and the uplift is the honest cost of that.

## What to say

> "Fixed project means you pay the build cost as one number, staged
> 40/40/20 — about 40% due before we start. Subscription spreads that same
> build cost over the term instead, with a financing uplift on the
> remainder — 12% over 24 months, for example — plus your hosting and
> support are bundled into the same monthly line so you're not fielding a
> separate SaaS bill. Neither is 'better' — it depends whether you'd rather
> pay less in total or less upfront."

> "If you want the lowest total cost and can clear a 40% upfront payment,
> fixed project is genuinely cheaper. If cash flow matters more than total
> cost, subscription is built for that — the uplift is the visible price of
> that trade, not something we're hiding."
