#!/usr/bin/env python3
"""
Renders the three Rev3 markdown artifacts (offer, walk-away, answered
question form) to HTML using the repo's actual registered brand system --
06-brand/registry.yaml -> styles.pdf_portrait -> 06-brand/styles/
proposal.pdf.css -- the same stylesheet used for VGE's real client-facing
Rev3 proposal, not an improvised one-off.

Deliberately applies tokens/color.yaml + proposal.pdf.css's typography
choice (Playfair Display + Inter, the precedent actually in force per
proposal.pdf.css's own header comment -- tokens/type.yaml specifies IBM
Plex Sans/Serif, but that was superseded for proposal work by explicit
user choice on the last real proposal built here). Grid: A4 portrait,
20mm margin, 170mm content width, per tokens/grid.yaml.

Watermarks (decor.yaml / assets/watermarks/) are NOT applied here --
these are shorter, single-topic documents pending human approval, not
the full 13-section formal proposal watermark rotation was designed for,
and pulling in per-section landmark assets would be disproportionate
effort for documents that may still change. Flagged, not silently
skipped. Colour palette, typography, and grid ARE applied, consistently,
across all three documents.

No PDF generation -- Markdown/HTML only, per this pass's constraint.

Usage:
    python render_brand.py
"""
import re
from pathlib import Path

DRAFT_DIR = Path(r"C:\sgc_proposal_engine\02-clients\PRO-prosper-realestate\03-draft")
OUT_DIR = Path(r"C:\sgc_proposal_engine\02-clients\PRO-prosper-realestate\04-draft")

DOCS = [
    ("PRO-2026-SUB-01_Rev3\\PRO-2026-SUB-01_Rev3_Offer.md", "PRO-2026-SUB-01_Rev3_Offer.html",
     "Best and Final — Prosper Intl Real Estate", True),
    ("PRO-2026-SUB-01_Rev3\\PRO-2026-SUB-01_Rev3_WalkAway.md", "PRO-2026-SUB-01_Rev3_WalkAway.html",
     "Where Things Stand — Prosper Intl Real Estate", False),
    ("PRO-Requirements-Answered_2026-08-06.md", "PRO-Requirements-Answered_2026-08-06.html",
     "Answers to Your CRM & ERP Questions", False),
]

# Mirrors 06-brand/tokens/color.yaml exactly -- no colour outside this palette.
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --ivory: #F7F4EE;
  --navy: #0F213D;
  --gold: #B79554;
  --charcoal: #1C2430;
  --slate: #5F6775;
  --champagne: #D9C08A;
  --parchment: #ECE7DF;
}

@page { size: A4 portrait; margin: 20mm; }

* { box-sizing: border-box; }

body {
  font-family: "Inter", sans-serif;
  font-size: 15px;
  line-height: 1.75;
  color: var(--charcoal);
  background: var(--ivory);
  margin: 0;
  padding: 0;
}

.page {
  max-width: 170mm;
  margin: 0 auto;
  padding: 20mm 0;
}

.internal-banner {
  background: var(--charcoal);
  color: var(--ivory);
  font-family: "Inter", sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  text-align: center;
  padding: 10px 16px;
  margin-bottom: 14mm;
}

.masthead { margin-bottom: 10mm; }
.masthead .prepared-for {
  font-family: "Inter", sans-serif;
  font-size: 13px;
  color: var(--slate);
}
.masthead .reference {
  font-family: "Inter", sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gold);
}

h1.cover-title, h1.section {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  color: var(--navy);
  letter-spacing: -0.5px;
  margin-top: 12mm;
  margin-bottom: 4mm;
  border-bottom: 1.5px solid var(--gold);
  padding-bottom: 3mm;
}
h1.section:first-of-type { margin-top: 0; }
h1 { font-size: 28px; }
body > .page > h1:first-of-type { font-size: 34px; }

h2.subsection {
  font-family: "Inter", sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--gold);
  margin-top: 8mm;
}
h3 { font-family: "Inter", sans-serif; font-size: 15px; font-weight: 600; color: var(--navy); }

p { margin: 0 0 1em 0; }

strong { color: var(--navy); }

table {
  border-collapse: collapse;
  width: 100%;
  margin: 6mm 0;
  font-size: 13.5px;
}
th {
  background: var(--navy);
  color: var(--ivory);
  font-family: "Inter", sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  text-align: left;
  padding: 6px 10px;
}
td {
  border: 1px solid var(--champagne);
  padding: 6px 10px;
}

blockquote {
  font-family: "Inter", sans-serif;
  font-style: italic;
  border-left: 3px solid var(--gold);
  background: var(--parchment);
  margin: 5mm 0;
  padding: 4mm 6mm;
  color: var(--navy);
}

code {
  background: var(--parchment);
  padding: 1px 5px;
  border-radius: 2px;
  font-size: 0.9em;
}

hr { border: none; border-top: 1px solid var(--champagne); margin: 8mm 0; }

.caption, .footnote {
  font-family: "Inter", sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--slate);
}

ul, ol { padding-left: 1.4em; }
li { margin-bottom: 0.4em; }
"""


def _inline(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_to_html(text: str) -> str:
    # Strip HTML comments first, as whole blocks -- a per-line startswith
    # check only catches the comment's opening line, leaving continuation
    # lines (and the closing "-->") to leak through as stray paragraphs.
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = text.split("\n")
    out: list[str] = []
    in_table = False
    in_list = False
    list_tag = ""
    first_h1_done = False
    para_buf: list[str] = []

    def flush_para():
        if para_buf:
            out.append(f"<p>{_inline(' '.join(para_buf))}</p>")
            para_buf.clear()

    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1:
            flush_para()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                out.append("<table>")
                out.append("<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells) + "</tr>")
                in_table = True
                continue
            if set(stripped.replace("|", "").replace("-", "").replace(" ", "")) == set():
                continue
            out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
            continue
        elif in_table:
            out.append("</table>")
            in_table = False

        if stripped == "---":
            flush_para()
            out.append("<hr>")
        elif stripped.startswith("# "):
            flush_para()
            cls = "cover-title" if not first_h1_done else "section"
            first_h1_done = True
            out.append(f'<h1 class="{cls}">{_inline(stripped[2:])}</h1>')
        elif stripped.startswith("## "):
            flush_para()
            out.append(f'<h2 class="subsection">{_inline(stripped[3:])}</h2>')
        elif stripped.startswith("### "):
            flush_para()
            out.append(f"<h3>{_inline(stripped[4:])}</h3>")
        elif stripped.startswith("> "):
            flush_para()
            out.append(f"<blockquote>{_inline(stripped[2:])}</blockquote>")
        elif stripped.startswith("- "):
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True; list_tag = "ul"
            out.append(f"<li>{_inline(stripped[2:])}</li>")
        elif stripped.startswith(tuple(f"{i}. " for i in range(1, 10))):
            flush_para()
            if not in_list:
                out.append("<ol>"); in_list = True; list_tag = "ol"
            out.append(f"<li>{_inline(stripped[stripped.index('.')+2:])}</li>")
        elif stripped == "":
            flush_para()
            if in_list:
                out.append(f"</{list_tag}>"); in_list = False
        else:
            if in_list:
                out.append(f"</{list_tag}>"); in_list = False
            para_buf.append(stripped)

    flush_para()
    if in_table:
        out.append("</table>")
    if in_list:
        out.append(f"</{list_tag}>")
    return "\n".join(out)


def main():
    for src_rel, out_name, title, is_internal_draft in DOCS:
        src = DRAFT_DIR / src_rel
        text = src.read_text(encoding="utf-8")
        banner = ('<div class="internal-banner">INTERNAL DRAFT — PENDING HUMAN DECISION — '
                  'NOT YET SENT</div>')
        body_html = md_to_html(text)
        full_html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>{title}</title>
<style>{CSS}</style>
</head><body>
<div class="page">
{banner}
{body_html}
</div>
</body></html>"""
        out_path = OUT_DIR / out_name
        out_path.write_text(full_html, encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
