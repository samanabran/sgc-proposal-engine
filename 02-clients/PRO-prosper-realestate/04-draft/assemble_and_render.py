"""Assemble the 13 markdown sections into a single internal-review HTML/PDF.

Internal-only document (Docuseal, SDR signature) — deliberately simpler
styling than the full client-facing brand/watermark system used for
external proposals like VGE's. Proportionate effort for an internal
artifact, not a client deliverable.

Usage:
    python assemble_and_render.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DRAFT_DIR = Path(
    r"C:\sgc_proposal_engine\02-clients\PRO-prosper-realestate\03-draft"
    r"\PRO-2026-SUB-01_Rev1"
)
OUT_HTML = Path(
    r"C:\sgc_proposal_engine\02-clients\PRO-prosper-realestate\04-draft"
    r"\PRO-2026-SUB-01_Rev1_Internal.html"
)
OUT_PDF = OUT_HTML.with_suffix(".pdf")

SECTIONS = [
    "01-executive-summary.md",
    "02-about.md",
    "03-understanding-business.md",
    "04-as-is.md",
    "05-to-be.md",
    "06-solution-phase1.md",
    "07-options-inclusions.md",
    "08-implementation-recovery.md",
    "09-partnership-terms.md",
    "10-commercial-terms.md",
    "11-support-sla.md",
    "12-why-sgc.md",
    "13-next-steps.md",
]

CSS = """
@page { size: A4; margin: 20mm 18mm; }
body { font-family: 'IBM Plex Sans', Arial, sans-serif; color: #1C2430; line-height: 1.5; font-size: 10.5pt; }
h1 { font-size: 20pt; color: #1C2430; border-bottom: 2px solid #B79554; padding-bottom: 6px; margin-top: 0; page-break-before: always; }
section:first-of-type h1 { page-break-before: avoid; }
h2 { font-size: 13pt; color: #1C2430; margin-top: 18px; }
h3 { font-size: 11.5pt; color: #5F6775; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt; }
th, td { border: 1px solid #D9C08A; padding: 5px 8px; text-align: left; }
th { background: #ECE7DF; font-weight: 600; }
blockquote { border-left: 3px solid #B79554; margin: 10px 0; padding: 6px 14px; background: #F7F4EE; font-style: italic; }
.internal-banner { background: #1C2430; color: #F7F4EE; padding: 10px 16px; font-weight: 600; text-align: center; margin-bottom: 14px; }
.cover { text-align: center; padding-top: 30mm; }
.cover h1 { border: none; font-size: 26pt; page-break-before: avoid; }
section { page-break-after: always; }
section:last-of-type { page-break-after: avoid; }
code { background: #ECE7DF; padding: 1px 4px; border-radius: 2px; font-size: 9pt; }
"""


def md_to_html(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_table = False
    in_list = False
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

        if stripped.startswith("# "):
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
            out.append(f"<li>{stripped[2:]}</li>")
            continue
        elif stripped.startswith(tuple(f"{i}. " for i in range(1, 10))):
            if not in_list:
                out.append("<ol>")
                in_list = True
            out.append(f"<li>{stripped[stripped.index('.')+2:]}</li>")
            continue
        elif stripped == "":
            if in_list:
                out.append("</ul>" if out[-1].startswith("<li") or "</li>" in out[-1] else "</ol>")
                in_list = False
            out.append("")
        else:
            out.append(f"<p>{stripped}</p>")

        if in_list and stripped == "":
            in_list = False
    if in_table:
        out.append("</table>")
    html = "\n".join(out)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", html)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    return html


def main() -> int:
    body_parts = []
    for i, fname in enumerate(SECTIONS):
        path = DRAFT_DIR / fname
        if not path.is_file():
            print(f"error: {path} not found", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        section_html = md_to_html(text)
        body_parts.append(f"<section>{section_html}</section>")

    full_html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>PRO-2026-SUB-01_Rev1 — Internal Draft</title>
<style>{CSS}</style>
</head><body>
<div class="cover">
<div class="internal-banner">INTERNAL DRAFT — NOT FOR CLIENT TRANSMISSION — SDR REVIEW/SIGNATURE ONLY</div>
<h1>PRO-2026-SUB-01</h1>
<p>Revision 1 &middot; Subscription Recovery Model &middot; Prosper Intl Real Estate</p>
<p>Prepared by SGC TECH AI &middot; 2026-08-05</p>
</div>
{''.join(body_parts)}
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
