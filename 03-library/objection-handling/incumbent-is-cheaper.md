# Objection: "Our current provider/system is cheaper than this"

## Why it comes up

The client is comparing SGC's proposal against the sunk cost of staying
put, or against a low-ball renewal quote from an incumbent vendor who
knows switching has friction. "Cheaper" often means "cheaper to keep
doing nothing," not "cheaper for equivalent scope."

## The SGC response

Two separate things are usually being conflated here, and untangling them
is the actual sales move:

**1. Positioning, not "cheapest."** SGC's own stated position is
explicit: **"Specialist boutique band. 15–20% below mid-tier, well below
Big-4"** (`market-data/benchmarks.yaml: strategic_position`) — not "the
cheapest option in the market." An incumbent charging less is entirely
plausible if they're a smaller freelancer, an unsupported legacy system,
or a vendor who's stopped investing in the relationship because the
contract is expiring anyway. Cheaper isn't automatically comparable —
ask what's actually in the incumbent's number (ongoing support? a named
account manager? documented configuration? an Odoo-certified team?)
before treating it as apples-to-apples.

**2. What switching actually commits to.** If the deal proceeds, SGC's
scope and pricing assume the incumbent is being genuinely replaced, not
run in parallel indefinitely — this is written into every proposal
verbatim via `clause-library/exclusivity-replacement.md` (used in §08
whenever the client brief names an incumbent):

> "SGC TECH AI's scope and pricing are based on this replacement being
> exclusive... the incumbent system is decommissioned or restricted to
> read-only/archive access following a mutually agreed cutover date."

That clause matters for the objection: it's the reason SGC's pricing
doesn't need to compete with the sunk cost of *keeping* the incumbent
around — the deal is priced as a full replacement, not as a second system
layered on top of the first. If the client wants to run both in parallel
past the cutover window, that's explicitly a change request against the
pricing (per the clause), which is worth surfacing early rather than
letting it surface as scope creep later.

## What to say

> "We're not positioned to be the cheapest option in the market — we're
> priced 15–20% under mid-tier agencies, which is a different claim. If
> your incumbent's quote is genuinely lower, it's worth checking what's
> actually included — ongoing support, documented configuration, a
> certified implementation team — before comparing it directly to ours."

> "Our pricing assumes this is a real replacement, not running two systems
> in parallel — that's actually part of why we can hold this number. If you
> want to keep the incumbent running alongside us past go-live, that
> changes the scope, and I'd rather flag that now than have it show up as
> a surprise later."
