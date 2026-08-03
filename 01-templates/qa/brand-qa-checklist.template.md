# Brand QA Checklist — copy to 02-clients/{client}/04-review/brand-qa-checklist.md

Per-client working copy of `06-brand/brand-qa-checklist.md` — that file
is the master; complete this copy for each revision before human review.

- [ ] All colour, type, grid, and decor tokens used trace to `06-brand/registry.yaml`
- [ ] Saturation law respected (`06-brand/tokens/color.yaml`)
- [ ] Every entity fact (legal name, licence authority, address, contact)
      pulled from `06-brand/entity/legal-identity.yaml` — **blocked from
      issue if any field is still `RESOLVE`**
- [ ] Co-branding, if any, follows `06-brand/co-brand/rules.md` — cover
      right-panel and transmittal TO block only
- [ ] No Arabic content unless `06-brand/locale/ar-AE.md` status has moved
      past SPEC INCOMPLETE
- [ ] Landscape layout used only for §10 commercial comparison table /
      worksheet appendix, per `06-brand/tokens/grid.yaml`

Reviewer: _______________  Date: _______________
Result: [ ] Approved   [ ] Changes required
