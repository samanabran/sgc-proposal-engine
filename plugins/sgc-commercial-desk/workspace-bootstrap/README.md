# Starting a New Client

1. Copy this entire `_SCAFFOLD` folder to `02-clients/{PREFIX}-{slug}/` — see
   `05-ops/naming-conventions.md` for the prefix/slug pattern. **Copy this
   folder, never a peer client's folder** (see `known-defects.md` #2).
2. Fill `manifest.yaml`.
3. Copy `01-templates/intake/client-brief.template.yaml` into
   `00-intake/client-brief.yaml` and complete it from discovery.
4. Follow `00-knowledge/runbook/subscription-proposal-runbook.md` from §1.

This folder ships empty of numbers on purpose. Everything you need —
rates, hours, clauses, gates — is inherited by reference from
`00-knowledge/` and `01-templates/`, not copied in here.
