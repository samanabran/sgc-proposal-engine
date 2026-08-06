"""Render the Rev2 priority-draft markdown into internal-review HTML/PDF.

Single-file trimmed revision (not the full 13-section structure) — see
03-draft/PRO-2026-SUB-01_Rev2/PRO-2026-SUB-01_Rev2_Priority-Draft.md for
the scope-cut rationale. Same internal-only styling convention as Rev1's
assemble_and_render.py.

Usage:
    python render_rev2.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SRC = Path(
    r"C:\sgc_proposal_engine\02-clients\PRO-prosper-realestate\03-draft"
    r"\PRO-2026-SUB-01_Rev2\PRO-2026-SUB-01_Rev2_Priority-Draft.md"
)
OUT_HTML = Path(
    r"C:\sgc_proposal_engine\02-clients\PRO-prosper-realestate\04-draft"
    r"\PRO-2026-SUB-01_Rev2_Priority-Draft.html"
)
OUT_PDF = OUT_HTML.with_suffix(".pdf")

CSS = """
@page { size: A4; margin: 20mm 18mm; }
body { font-family: 'IBM Plex Sans', Arial, sans-serif; color: #1C2430; line-height: 1.5; font-size: 10.5pt; }
h1 { font-size: 20pt; color: #1C2430; border-bottom: 2px solid #B79554; padding-bottom: 6px; margin-top: 0; }
h2 { font-size: 13pt; color: #1C2430; margin-top: 20px; border-top: 1px solid #D9C08A; padding-top: 10px; }
h3 { font-size: 11.5pt; color: #5F6775; margin-top: 14px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt; }
th, td { border: 1px solid #D9C08A; padding: 5px 8px; text-align: left; }
th { background: #ECE7DF; font-weight: 600; }
blockquote { border-left: 3px solid #B79554; margin: 10px 0; padding: 6px 14px; background: #F7F4EE; font-style: italic; }
.internal-banner { background: #1C2430; color: #F7F4EE; padding: 10px 16px; font-weight: 600; text-align: center; margin-bottom: 14px; }
.scope-note { background: #F7F4EE; border: 1px solid #D9C08A; padding: 10px 14px; margin-bottom: 18px; font-size: 9.5pt; }
.cover { text-align: center; padding-top: 20mm; margin-bottom: 20mm; }
.cover h1 { border: none; font-size: 24pt; }
code { background: #ECE7DF; padding: 1px 4px; border-radius: 2px; font-size: 9pt; }
hr { border: none; border-top: 1px solid #D9C08A; margin: 18px 0; }
"""


def md_to_html(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_table = False
    in_list = False
    list_tag = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                out.append("<table>")
                out.append("<tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr>")
                in_table = True
                continue
            if set(stripped.replace("|", "").replace("-", "").replace(" ", "")) == set():
                continue
            out.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
            continue
        elif in_table:
            out.append("</table>")
            in_table = False

        if stripped == "---":
            out.append("<hr>")
        elif stripped.startswith("# "):
            out.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("## "):
            out.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("### "):
            out.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("> "):
            out.append(f"<blockquote>{stripped[2:]}</blockquote>")
        elif stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
                list_tag = "ul"
            out.append(f"<li>{stripped[2:]}</li>")
            continue
        elif stripped.startswith(tuple(f"{i}. " for i in range(1, 10))):
            if not in_list:
                out.append("<ol>")
                in_list = True
                list_tag = "ol"
            out.append(f"<li>{stripped[stripped.index('.')+2:]}</li>")
            continue
        elif stripped == "":
            if in_list:
                out.append(f"</{list_tag}>")
                in_list = False
            out.append("")
        else:
            if in_list:
                out.append(f"</{list_tag}>")
                in_list = False
            out.append(f"<p>{stripped}</p>")

    if in_table:
        out.append("</table>")
    if in_list:
        out.append(f"</{list_tag}>")
    html = "\n".join(out)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", html)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    return html


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    # First H1 becomes the cover; rest flows as the body.
    body_html = md_to_html(text)

    full_html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>PRO-2026-SUB-01_Rev2 — Priority Draft</title>
<style>{CSS}</style>
</head><body>
<div class="internal-banner">INTERNAL DRAFT — NOT FOR CLIENT TRANSMISSION — SDR REVIEW/SIGNATURE ONLY</div>
{body_html}
</body></html>"""

    OUT_HTML.write_text(full_html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(OUT_HTML.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        browser.close()

    import os
    size_kb = os.path.getsize(OUT_PDF) / 1024
    print(f"wrote {OUT_HTML}")
    print(f"wrote {OUT_PDF} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
