# Quarantined — stale against the live worksheet

`KP-2026-SUB-01_Rev1_Internal.html` and `.pdf` were rendered before the
2026-08-05 pricing v3.0 recompute (commit `525940d`, which deleted
`overlays.rollout_hours_per_user` and replaced it with the Class A-D cost
model) and were never re-rendered afterward. They still show Rev1's
original figures — build value AED 121,716, mobilisation AED 48,686,
Subscription Fee AED 7,790/mo — none of which match the current
`02-calc/pricing-worksheet.yaml` (build value AED 56,072, mobilisation AED
22,429, Subscription Fee AED 5,850/mo).

Never issued to the client (`manifest.yaml: issued_date: ""`,
`prior_versions_issued_to_client: false`) — quarantined as a hygiene
measure, not a retraction of anything sent externally. Moved here so a
reviewer opening `04-draft/` finds only current material by default.
Re-render from the current worksheet via `assemble_and_render.py` before
producing a replacement; do not restore these files to `04-draft/` as-is.
