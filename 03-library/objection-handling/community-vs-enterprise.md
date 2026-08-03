# Objection: "Shouldn't we just get the full Enterprise version?"

## Why it comes up

A client researches Odoo independently, finds Enterprise-edition
marketing material, and asks why the proposal doesn't include it — or
worse, assumes it already does.

## The response

Community, the default we build on, covers everything most 5–15 user
brokerages actually need — CRM, sales, invoicing, basic accounting,
project, and mobile-optimised browser access — at zero per-user licence
cost, which is exactly why the implementation can be absorbed into the
subscription instead of billed as a separate licence line. Enterprise
adds specific things (automated bank reconciliation, a native mobile app,
Studio, multi-currency) that only matter once a client actually needs
one of them — see `editions.yaml: enterprise.trigger_conditions`.

**Never let this conversation end with an implied "yes, obviously
Enterprise" if no trigger condition is actually present** — see
`known-defects.md` #18 for what happens when edition gets fudged under
sales pressure.

## Exact language

> "Community covers what you've described needing. Enterprise adds a
> short list of specific things — automated bank reconciliation and a
> native mobile app are the two that come up most. If any of those turn
> out to matter once we're in discovery, we'll say so explicitly and
> price the upgrade separately — never silently."

## Ties to

`clause-library/edition-and-upgrades.md`, §06 of every proposal (mandatory
written disclosure, G38).
