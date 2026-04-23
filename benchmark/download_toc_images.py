"""Download and save ToC page images for every benchmark document.

For each document in ``ground_truth.json`` this script:

1. Loads the sample text from ``data/samples/{doc_id}.txt``.
2. Calls the same region-detection helpers used by ``extract_toc_indices``.
3. Resolves the BDRC page list for the document's ``volume_id``.
4. For ToC-bearing documents, caps the ToC region at the 5-page image window.
5. For no-marker documents, picks the short-line candidate pages instead.
6. Downloads each image and writes it to
   ``data/toc_images/{doc_id}_{volume_id}/page_{pnum:04d}_{pname}``.

This is a debugging / manual-inspection aid; it is not called from the
benchmark pipeline itself.

Usage::

    set IIIF_API_KEY=...    # required
    python -m benchmark.download_toc_images
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from ai_text_outline._extract import (
    _find_short_line_pages,
    _find_toc_region,
    _get_image_bounded_toc_end,
)
from ai_text_outline._pages import (
    fetch_page_image,
    find_pages_for_range,
    get_volume_pages,
)

from benchmark.config import DATA_DIR, GROUND_TRUTH_PATH, SAMPLES_DIR

DEFAULT_TOC_IMAGES_DIR = DATA_DIR / "toc_images"
MAX_NO_MARKER_CANDIDATES = 30
PAGE_WINDOW = 5


def _save_image(out_dir: Path, page: dict, img_bytes: bytes) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    pnum = page.get("pnum")
    pname = page.get("pname", "page.jpg")
    prefix = f"page_{int(pnum):04d}_" if isinstance(pnum, int) else "page_"
    out_path = out_dir / f"{prefix}{pname}"
    out_path.write_bytes(img_bytes)
    return out_path


def _process_document(
    doc_id: str,
    gt: dict,
    iiif_api_key: str,
    *,
    samples_dir: Path,
    toc_images_dir: Path,
) -> None:
    text_path = samples_dir / f"{doc_id}.txt"
    if not text_path.exists():
        print(f"  [skip] missing sample file: {text_path}")
        return

    volume_id = gt.get("filename")
    if not volume_id:
        print(f"  [skip] no volume_id in ground truth for {doc_id}")
        return

    text = text_path.read_text(encoding="utf-8")

    try:
        vol_id, pages = get_volume_pages(volume_id)
    except RuntimeError as e:
        print(f"  [error] get_volume_pages failed: {e}")
        return
    if not vol_id or not pages:
        print(f"  [skip] empty page list for {volume_id}")
        return

    out_dir = toc_images_dir / f"{doc_id}_{volume_id}"

    if out_dir.exists():
        existing = [p for p in out_dir.iterdir() if p.is_file() and p.stat().st_size > 0]
        if len(existing) >= 3:
            print(f"  [skip] already have {len(existing)} image(s) in {out_dir.name}")
            return

    toc_region = _find_toc_region(text)
    selected_pages: list[dict] = []
    mode: str

    if toc_region is not None:
        toc_start, toc_end = toc_region
        bounded_end = _get_image_bounded_toc_end(
            toc_start, pages, n_pages=PAGE_WINDOW,
        )
        if bounded_end is not None:
            toc_end = min(toc_end, bounded_end)
        selected_pages = find_pages_for_range(pages, toc_start, toc_end)
        mode = f"toc-marker ({len(selected_pages)} page(s), window={PAGE_WINDOW})"
    else:
        candidates = _find_short_line_pages(text, pages)
        candidates = candidates[:MAX_NO_MARKER_CANDIDATES]
        pname_to_page = {p["pname"]: p for p in pages if "pname" in p}
        for c in candidates:
            page = pname_to_page.get(c.get("pname"))
            if page is not None:
                selected_pages.append(page)
        mode = f"no-marker candidates ({len(selected_pages)} page(s))"

    if not selected_pages:
        print(f"  [skip] no ToC pages resolved ({mode})")
        return

    print(f"  mode: {mode}")
    print(f"  output: {out_dir}")
    saved = 0
    for page in selected_pages:
        pname = page.get("pname")
        if not pname:
            continue
        try:
            img_bytes = fetch_page_image(vol_id, pname, iiif_api_key)
        except RuntimeError as e:
            print(f"    [warn] fetch {pname}: {e}")
            continue
        out_path = _save_image(out_dir, page, img_bytes)
        saved += 1
        print(f"    -> {out_path.name}")
    print(f"  saved {saved}/{len(selected_pages)} image(s)")


def main(
    *,
    samples_dir: Path | None = None,
    ground_truth_path: Path | None = None,
    toc_images_dir: Path | None = None,
) -> int:
    samples_dir = samples_dir or SAMPLES_DIR
    ground_truth_path = ground_truth_path or GROUND_TRUTH_PATH
    toc_images_dir = toc_images_dir or DEFAULT_TOC_IMAGES_DIR

    iiif_api_key = os.environ.get("IIIF_API_KEY")
    if not iiif_api_key:
        print("ERROR: set IIIF_API_KEY in the environment before running.")
        return 1

    with open(ground_truth_path, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    total = len(ground_truth)
    toc_images_dir.mkdir(parents=True, exist_ok=True)

    for i, (doc_id, gt) in enumerate(ground_truth.items(), start=1):
        filename = gt.get("filename", "<unknown>")
        print(f"[{i}/{total}] {doc_id}  ({filename})", flush=True)
        try:
            _process_document(
                doc_id, gt, iiif_api_key,
                samples_dir=samples_dir,
                toc_images_dir=toc_images_dir,
            )
        except Exception as e:  # noqa: BLE001 — this is a debug tool
            print(f"  [error] {type(e).__name__}: {e}", flush=True)

    print(f"\nAll images under {toc_images_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
