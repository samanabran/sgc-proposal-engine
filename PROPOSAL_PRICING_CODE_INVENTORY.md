# Proposal / Pricing Code Inventory (new file, 2026-08-15)

This file's name is chosen to record a naming collision found during the
2026-08-15 RVN audit, not to claim continuity with any prior document of
a similar name elsewhere — none was found in this repository's git
history, and this is a new file, not an append to any prior commit.

**The collision**: this repository's git remote is
`github.com/samanabran/sgc-proposal-engine.git` — named for an "engine,"
but its actual content (`00-knowledge/`, `02-clients/`, `05-ops/`,
`06-brand/`) is a flat-file knowledge and document repository: YAML
pricing catalogues, markdown clause libraries and client folders, and a
Python validator (`05-ops/validate.py`) that reads those files directly.
There is no database, no installed application module, and no record-ID
system anywhere in this checkout. Anyone expecting a database-backed
"pricing engine" from the repo name alone will be looking for objects
(tables, gates, confidence bands) that do not exist here — they may exist
in a genuinely separate system (an Odoo module, a VPS deployment) that
this repository's own files sometimes reference for unrelated purposes
(e.g. `10-signature/deploy/README.md` documents a signature-webhook
service on a VPS), but no evidence in this checkout confirms a pricing
engine exists there, and no evidence in this checkout confirms it does
not. Scope every claim about "the engine" to the specific tree it was
checked in.
