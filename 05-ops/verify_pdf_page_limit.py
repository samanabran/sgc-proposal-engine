#!/usr/bin/env python3
"""
Mechanical 10-page-limit enforcement, Part 5.3. The HTML generator
(render_proposal_v4.py) forces one page-break per section by design,
which means "exactly 10 pages" for the real fixtures is partly a product
of that construction, not solely proof the enforcement mechanism would
catch a genuine overflow. This script is the actual enforcement point:
it reads a real rendered PDF's page count (pypdf, no wkhtmltopdf needed
locally) and exits non-zero if it exceeds the limit.

CANONICAL RENDER PATH (known-defects.md #29): page counts must be
verified against a real `wkhtmltopdf 0.12.6.1` render before they are
quoted anywhere -- run it inside the `demo_presentation` Docker container
on the ops VPS (a non-production Odoo 19 container; distinct from
`odoo-prod`/`sgc_staging`, no DB touched, no -u/-i, a stateless
HTML-to-PDF convert only: `docker exec -u root demo_presentation
wkhtmltopdf --disable-smart-shrinking in.html out.pdf`). Chrome headless
(`chrome --headless --print-to-pdf`) is a local convenience for quick
iteration ONLY -- it is a different, modern WebKit engine with materially
different flow/pagination behaviour, confirmed to disagree with
wkhtmltopdf by a full page on a near-boundary fixture (F2:
ZZZFIXTURE-2026-V4-02, 5 pages under Chrome vs. 4 under wkhtmltopdf).
Any page count produced by Chrome is provisional until re-confirmed
against the container above; only a wkhtmltopdf-derived count may be
cited as final in a client-facing decision.

Usage:
    python verify_pdf_page_limit.py <pdf_path> [max_pages]
"""
import sys

import pypdf


def check(pdf_path, max_pages=10):
    reader = pypdf.PdfReader(pdf_path)
    n = len(reader.pages)
    if n > max_pages:
        print(f"FAIL: {pdf_path} has {n} pages, exceeds the {max_pages}-page limit")
        return False
    print(f"PASS: {pdf_path} has {n} pages (limit {max_pages})")
    return True


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    ok = check(pdf_path, max_pages)
    sys.exit(0 if ok else 1)
