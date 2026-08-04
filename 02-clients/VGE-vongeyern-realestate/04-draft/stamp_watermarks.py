"""Stamp one full-page watermark behind each physical PDF page.

Why a post-process instead of CSS: a background tied to a <section> that
runs across several physical pages lands wherever that section's box
happens to fall when Chromium paginates it — this produced cropped or
misplaced artwork in earlier passes. Doing it after pagination, directly
against the real page objects, gives exact per-page placement with zero
risk of the watermark straddling a page break.

Usage: run after regenerating the clean (unwatermarked) PDF from the HTML.
    python stamp_watermarks.py
"""
import os
import fitz

PDF_PATH = r"C:\sgc_proposal_engine\02-clients\VGE-vongeyern-realestate\04-draft\VGE-2026-SUB-01_Rev3_Proposal.pdf"
ASSET_DIR = r"C:\sgc_proposal_engine\06-brand\assets\watermarks\optimized\fullpage\jpg"

# Section heading -> page it starts on, found via search_for against the
# clean PDF. Recompute if the copy changes enough to shift pagination.
SECTION_HEADING_PAGE = {
    "cover": 1,
    "sec-01": 2,
    "sec-02": 2,
    "sec-03": 3,
    "sec-04": 3,
    "sec-05": 4,
    "sec-06": 5,
    "sec-07": 5,
    "sec-08": 6,
    "sec-09": 6,
    "sec-10": 7,
    "sec-11": 8,
    "sec-12": 9,
    "sec-13": 9,
    "appendix": 10,
}

# One landmark per section, in document order — see rotation intent in
# 06-brand/assets/watermarks/rotation.yaml (no two consecutive pages
# repeat the same landmark).
SECTION_IMAGE = {
    "cover": "qasr-al-watan.jpg",
    "sec-01": "heritage-ghaf-tree-dallah.jpg",
    "sec-02": "emirates-towers.jpg",
    "sec-03": "jumeirah-mosque.jpg",
    "sec-04": "museum-of-the-future.jpg",
    "sec-05": "cayan-tower-marina.jpg",
    "sec-06": "louvre-abu-dhabi.jpg",
    "sec-07": "dubai-frame.jpg",
    "sec-08": "stepped-resort.jpg",
    "sec-09": "heritage-al-fahidi-windtowers.jpg",
    "sec-10": "sheikh-zayed-mosque-wide.jpg",
    "sec-11": "dubai-opera.jpg",
    "sec-12": "ain-dubai.jpg",
    "sec-13": "etihad-towers.jpg",
    "appendix": "heritage-mountain-village.jpg",
}


def build_page_image_map(total_pages: int) -> dict[int, str]:
    """For each physical page, pick the most-recently-started section as
    of that page (the section active by the time you reach its bottom)."""
    ordered = list(SECTION_HEADING_PAGE.items())  # already in doc order
    page_to_section = {}
    for page_num in range(1, total_pages + 1):
        active = None
        for name, start_page in ordered:
            if start_page <= page_num:
                active = name
        page_to_section[page_num] = active
    return {p: SECTION_IMAGE[s] for p, s in page_to_section.items()}


def main():
    doc = fitz.open(PDF_PATH)
    page_image = build_page_image_map(len(doc))
    for i, page in enumerate(doc):
        page_num = i + 1
        image_name = page_image[page_num]
        image_path = f"{ASSET_DIR}\\{image_name}"
        page.insert_image(page.rect, filename=image_path, overlay=False)
        print(f"page {page_num}: {image_name}")
    tmp_path = PDF_PATH + ".tmp"
    doc.save(tmp_path)
    doc.close()
    os.replace(tmp_path, PDF_PATH)
    print("done")


if __name__ == "__main__":
    main()
