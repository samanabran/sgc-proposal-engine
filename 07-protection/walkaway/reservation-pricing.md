# Reservation Pricing

The floor below which a deal should not proceed at all, computed before
any negotiation.

```
revenue_floor(margin) = (build_cost + CTS × term) ÷ (1 − margin)
monthly_floor = (revenue_floor − mobilisation) ÷ term_months
```

Run this twice — once at `policy.yaml: gates.target_gross_margin` (0.35)
for the number an SDR should be aiming to land at, and once at
`gates.absolute_margin_floor` (0.25) for the number below which no
approver, at any level, may go (G23).

These two numbers, plus the list price, are the three figures on the
walk-away deal card — nothing else belongs on that card.
