# Objection: "Great system, but my team won't actually use it"

## Why it comes up

This objection usually comes from a decision-maker who has been burned
before — a prior software rollout that was configured correctly but died
at the user-adoption stage because nobody changed how the team actually
worked. It's a legitimate concern, not a stalling tactic, and treating it
as one loses the deal.

## The SGC response

Adoption is framed contractually, not just verbally, as a **shared
responsibility** — see `clause-library/adoption.md`, which goes verbatim
into every proposal's §09 Partnership Terms when
`manifest.yaml: adoption_clause_included` is true:

> "SGC TECH AI will deliver the training and documentation described in
> this proposal, and the Client is responsible for internal change
> management, user onboarding cadence, and ongoing process compliance
> following go-live."

That's not SGC disclaiming responsibility for adoption — it's naming both
halves of the work explicitly so neither side assumes the other is
covering it. SGC's half is concrete and already priced in:

- **2 training sessions of 2 hours each** are bundled into every
  implementation by default (`policy.yaml: overlays.training_sessions`,
  `overlays.training_hours_per_session`) — billed once, in the build fee,
  not as a recurring line (Commercial Rule 8, `12-commercial-rules.md`).
  This isn't an optional add-on the client has to negotiate for; it's
  standard scope.
- Documentation is mandatory on every custom feature shipped — G4
  (`subscription-guardrails.md`) requires `documentation_hours` on every
  worksheet, so the team isn't left without reference material after
  go-live.
- If 4 hours of bundled training isn't enough for a larger or
  less-technical team, additional sessions are available and priced
  separately (`support-training.yaml: training` — e.g. `end_user_standard`
  at 5 hours / 1,750 AED) rather than silently included, so the client can
  size the training investment to their actual team, not a one-size-fits-
  all default.

The honest answer to "will my team use it" is: SGC delivers a working,
documented, trained-on system; the client owns the change-management
cadence after that. Naming this upfront, in writing, is what prevents the
adoption failure the client is worried about — it's the same failure mode
as a prior vendor who never said this out loud.

## What to say

> "That's a fair worry, and it's exactly why our partnership terms spell
> out adoption as a two-sided responsibility rather than leaving it
> implicit — we deliver a trained, documented system; you own the internal
> rollout cadence. Two training sessions are bundled into the build by
> default, and if your team needs more than that, we can size additional
> sessions rather than hoping four hours is enough."

> "If a previous rollout stalled on adoption, my guess is nobody wrote down
> who owned what after go-live. We put that in writing in every proposal
> so it's not a surprise six weeks in."
