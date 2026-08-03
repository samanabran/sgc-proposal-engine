# DOCX Style Mapping

Maps `tokens/*.yaml` to Word style names for any proposal rendered as
`.docx`. Apply via Word style definitions, not manual per-paragraph
formatting — manual formatting is how brand drift happens.

| Word style | Token source | Notes |
|---|---|---|
| Title | `type.yaml: display` | Cover page only |
| Heading 1 | `type.yaml: section` | §01-§13 headers |
| Heading 2 | `type.yaml: subsection`, color `color.yaml: gold` | |
| Normal | `type.yaml: body` | |
| Caption | `type.yaml: caption`, uppercase | Table headers, footnotes |
| Table Header | `color.yaml: navy` background, `ivory` text | |
| Page margins | `grid.yaml: portrait.margin_mm` (20mm) | Landscape sections use `grid.yaml: landscape.margin_mm` |

Colour palette is applied via Word theme colours mapped 1:1 to
`color.yaml: palette` — do not hand-pick a colour outside the theme swatch.
