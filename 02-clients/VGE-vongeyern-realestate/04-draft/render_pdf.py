"""Render the final-draft HTML to PDF using headless Chromium (Playwright).

Run from anywhere; paths are absolute.

Why a script: the proposal HTML has print-only styles (nav hidden,
sections paginated with `@page :size A4`). Headless Chromium's
`page.pdf()` honours those, and `document.fonts.ready` lets us wait for
the Google Fonts (Playfair Display, Inter) to actually resolve before
emitting the PDF — otherwise the early frames fall back to Georgia.

Usage:
    python render_pdf.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HTML_PATH = Path(
    r"C:\sgc_proposal_engine\02-clients\VGE-vongeyern-realestate\04-draft"
    r"\VGE-2026-SUB-01_Rev3_Proposal.html"
)
PDF_PATH = HTML_PATH.with_suffix(".pdf")


def main() -> int:
    if not HTML_PATH.is_file():
        print(f"error: {HTML_PATH} not found", file=sys.stderr)
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(HTML_PATH.as_uri(), wait_until="networkidle")
        # Force webfonts (Playfair Display, Inter) to fully resolve before
        # emitting the PDF — without this the first ~200ms of rendering can
        # miss the @font-face and lock in fallback faces.
        page.evaluate("document.fonts.ready")
        page.emulate_media(media="print")
        page.pdf(
            path=str(PDF_PATH),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        browser.close()

    size_kb = os.path.getsize(PDF_PATH) / 1024
    print(f"wrote {PDF_PATH} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
