# Walk-Away Deal Card — KP-2026-SUB-01_Rev1

**Produced before any pricing conversation with the client (G22).**
One page. Nothing beyond what's below.

## ⚠ Read this before the numbers

This deal card reflects the *third* iteration of scope/hours today. The
first pass (34h, AED 4,840/mo) failed `05-ops/validate.py`'s hour-benchmark
gate badly. The second pass (58h, AED 5,290/mo) still failed it. Closing it
required adding a genuine per-user scaling factor to `policy.yaml` itself
(v2.1, `rollout_hours_per_user`) — a real, defensible cost driver (role
setup, individual training, hypercare fanned across more people), not
padding. But the honest result is a **List price ~47% higher than where
this exercise started** (AED 5,290 → 7,790/mo). This works directly against
the disarm-hesitation strategy that motivated building this revised offer
in the first place. Worth deciding, before this goes anywhere near a
client conversation, whether AED 7,790/mo is still the right number to
lead with, or whether the "prioritize early needs" scope should be cut
back further even if that means living with a documented gate override
instead of a clean pass. **Flagging this explicitly rather than letting a
mechanically-clean gate report imply the strategic goal was met.**

## Three numbers (24-month option, preferred)

| | AED/mo |
|---|---|
| List (chosen Subscription Fee) | 7,790 |
| Target floor (30% margin) | 4,486 |
| **Absolute floor (25% margin — no approver may go below this)** | 4,051 |

(List = pricing-worksheet.yaml chosen 24mo Subscription Fee. Floors via
`07-protection/walkaway/reservation-pricing.md` against build_cost 28,800 +
CTS 3,360/mo × 24 months, less mobilisation 48,686.)

Actual computed margin on List: **~53.6%** — well clear of every floor.
The margin is this high specifically *because* the rollout-hours overlay
inflated build value substantially while CTS (which sets platform_portion)
stayed fixed — the healthy margin is a byproduct of the gate-compliance
fix, not a deliberate pricing choice.

## Total give available

AED 3,304/mo to the target floor, AED 3,739/mo to the absolute floor (24mo
term) — a wide band, reflecting the now-generous margin. **Currently zero
given.** Genuinely room to negotiate down significantly if price
sensitivity resurfaces, without breaching any margin floor.

## Risk band and required security

Band: **elevated** (`pricing/risk-security-matrix.yaml`) — **placeholder-driven**,
see `02-calc/risk-assessment.yaml`. Two of eight scoring inputs
(entity_age_years, vat_registered) are unconfirmed conservative
placeholders, not verified facts. Required instruments as currently
scored: **Mobilisation at 40%** (AED 48,686 at Kickoff), **2-month deposit**
(AED 15,580), **PDC set**. If the two unconfirmed inputs resolve favorably,
the band would likely drop to moderate/low and this instrument set would
loosen — **do not treat this as final without re-running the risk
assessment against real answers.**

## Top 3 compensators for this deal

1. Annual-prepay billing cadence (removes Recovery Component in full).
2. Extended Initial Term beyond 24 months — **not offered on this deal**,
   user capped commitment at 24 months maximum.
3. Given the wide give-available band above, a straightforward price
   reduction is realistically the more useful lever here than the
   standard compensator list — see the total-give-available note.

(from `pricing/concession-ladder.yaml: compensators` — pre-selected before
the conversation, not improvised mid-negotiation.)

## Abort criteria

Reference `07-protection/abort/abort-criteria.md`. **None currently
triggered.** Flagged for attention: risk band is placeholder-driven, not
confirmed; underlying CRM "Pipeline Gate Review: incomplete" (BANT Q1-Q4
missing) has not been resolved; **the price now materially exceeds the
figure this exercise set out to land near**, which is itself worth
treating as a soft abort signal for the internal reviewer, not just a
compliance checkbox.

## Incumbent benchmark

Prior unsigned PRJ-model proposal (SGC-KP-2026-07, built outside this
repo's governance) quoted AED 48,450-123,250 one-time (tier-dependent) +
AED 2,800-6,300/mo hosting. This SUB-model revision's Year-1 total
(24mo option) = 48,686 + (7,790 × 12) = **AED 142,166** — this now
lands *above* the prior PRJ proposal's Tier 2 (Growth) one-time-plus-
year-1-hosting equivalent (~79,900 + 4,900×12 = 138,700), the opposite of
the disarm-hesitation strategy's original intent. See the warning at the
top of this card.
