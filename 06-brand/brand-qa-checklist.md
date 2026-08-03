# Brand QA Checklist

Run before any draft moves to human review (step 7 of the runbook). Mirrors
`01-templates/qa/brand-qa-checklist.template.md` — this file is the
master; the template is the per-client working copy.

- [ ] Every colour used traces to `tokens/color.yaml: palette` — no
      off-registry hex value anywhere in the document
- [ ] Saturation law respected — XL surfaces ≤ 0.08, M elements ≤ 0.30,
      accents unrestricted but XS-scale only
- [ ] Typography matches `tokens/type.yaml` — no font or size introduced
      outside the five defined roles (display/section/subsection/body/caption)
- [ ] Grid matches `tokens/grid.yaml` — landscape used only for §10
      commercial comparison tables and worksheet appendices
- [ ] Watermark opacity within `tokens/decor.yaml` range; no consecutive
      landmark repeats across adjacent sections
- [ ] Every entity fact (name, licence authority, address, contact) pulled
      from `entity/legal-identity.yaml` — **document blocked from issue if
      any field is still `RESOLVE`**
- [ ] Co-branding, if any, follows `co-brand/rules.md` exactly — cover
      right-panel and transmittal TO block only, never listing pages
- [ ] No Arabic content included unless `locale/ar-AE.md` status has moved
      past SPEC INCOMPLETE
