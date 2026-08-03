# Objection: "Your price is too high"

## Why it comes up

Almost every prospect has a cheaper number in hand — a freelancer's quote, a
generic CRM subscription, or a competitor's low-ball to win the logo. The
objection is rarely "I can't afford this"; it's usually "convince me this
isn't the AED 15,000 CRM licence I could buy instead," or, less often,
"prove you're not a Big-4 markup."

## The SGC response

SGC sits deliberately in the middle of the market, not at either end, and
that position is a pricing policy, not a marketing line:

- **Senior consultant rate**: SGC 280–525 AED/hr vs. mid-tier agencies
  350–550 AED/hr vs. Big-4 600–900 AED/hr
  (`market-data/benchmarks.yaml: market_positioning.
  senior_consultant_hr_aed`).
- **10–30 user implementation**: SGC 22,000–55,000 AED vs. mid-tier
  45,000–75,000 AED vs. Big-4 80,000–150,000 AED
  (`market_positioning.implementation_10_30_users_aed`).
- **Full ERP rollout + Year 1**: SGC 70,000–150,000 AED vs. mid-tier
  180,000–350,000 AED vs. Big-4 500,000+ AED
  (`market_positioning.erp_rollout_bundle_c_plus_y1_aed`).

The stated position: **"Specialist boutique band. 15–20% below mid-tier,
well below Big-4"** (`benchmarks.yaml: strategic_position`). That's the
answer to "why isn't this cheaper" (a mid-tier agency would cost more for
the same senior-consultant-led delivery) and to "why isn't this free"
(a generic CRM licence doesn't come with an Odoo-certified implementation
team, UAE VAT localization, or a blended rate structure that's audited
against a rate card).

**Why SGC won't discount below the number quoted**: two mechanical gates
sit behind every quote, not sales discretion.

- **G8 (gross margin floor)** — the deal must clear 30% gross margin,
  target 35% (`policy.yaml: gates.min_gross_margin`,
  `gates.target_gross_margin`). Discounting further doesn't lower SGC's
  cost to deliver; it just moves the deal below the floor where it becomes
  a loss-making implementation regardless of how badly the team wants the
  logo.
- **G9 (market test)** — the quoted year-1 cost is capped at 1.30× the
  client's stated incumbent/comparable cost
  (`policy.yaml: gates.max_multiple_of_incumbent`). SGC is already
  mechanically prevented from quoting Big-4-adjacent prices; there's no
  hidden margin above the quote to discount away.

Reducing scope is a legitimate way to hit a tighter budget (fewer modules,
a lower support tier, a smaller user count). Reducing price below the floor
is not — see `known-defects.md #3` for what that looks like when an SDR
does it under deal pressure, and `AGENTS.md: On uncertainty`.

## What to say

> "We're priced deliberately in the specialist-boutique band — about
> 15–20% under what a mid-tier agency would charge for the same senior-led
> delivery, and well under half of what a Big-4 firm bills for this scope.
> If budget's the real constraint, I'd rather cut a module or a support
> tier with you than shave the number in a way that puts the delivery team
> at risk — let's look at what's actually load-bearing for you first."

> "Every quote we send is checked against a margin floor and a market-rate
> cap before it goes out — so what you're seeing isn't a number with
> padding I can just remove. If it's genuinely out of range, tell me your
> number and I'll show you what scope fits it."
