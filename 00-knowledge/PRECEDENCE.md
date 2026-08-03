# Precedence

Layers are cumulative. Later layers extend earlier ones; they do not
replace them. When two rules conflict, resolve in this order:

1. **Absolute floors** — `absolute_margin_floor` (25%, G23), unconditional
   client data export (G18), clawback presence on any deferred structure
   (G16), tax/registration accuracy (G35).
2. **Guardrails G1–G41** (`commercial-rules/`).
3. `policy.yaml` / `payment-plans.yaml` / `risk-security-matrix.yaml` /
   `editions.yaml` / other `pricing/*.yaml`.
4. Runbook method (`runbook/subscription-proposal-runbook.md`).
5. Templates and prose (`01-templates/`).

**The stricter rule always wins. A ceiling is never an entitlement** —
a cadence table's maximum discount is not a promise, it's an upper bound
still subject to the margin floor beneath it (see G12).

Superseded values live in `failure-modes/known-defects.md`, **never** in a
pricing file as a comment. If a number is wrong, delete it and log why it
was wrong — don't leave it dormant where a future read can pick it back up.
