# Graduated Response

What happens when an early-warning indicator fires
(`monitoring/early-warning-indicators.yaml`).

| Tier | Response |
|---|---|
| **Low** | Logged in the monthly Commercial Desk + Finance review. No immediate action required. |
| **Medium** | Commercial Desk reviews before the next deal is priced. New deals may proceed but risk band is re-checked for every deal in flight. |
| **High** | No new deferred-payment structures approved until the indicator clears. Existing deals continue but are reviewed individually against `exposure/portfolio-limits.yaml`. |
| **Critical** | New deal pricing pauses entirely except `full_prepay_term` or `annual_in_advance` cadences (zero financing exposure). Escalate to Founder-level review. |

Two or more concurrent medium-or-above indicators escalate one tier above
the highest individual tier present, not a simple sum — e.g. two medium
indicators together trigger a high-tier response.

This is a monitoring and response protocol, not a gate — it governs
*portfolio*-level behavior between deals, while G1–G41 govern each deal
individually.
