"""Review extracted staging samples for benchmark quality."""

from __future__ import annotations

import json
import re
from pathlib import Path

from benchmark.config import DATA_DIR, SAMPLES_DIR, GROUND_TRUTH_PATH


def _detect_toc_markers(text: str) -> list[int]:
    """Find all དཀར་ཆག marker positions in text."""
    return [m.start() for m in re.finditer(r"དཀར་ཆག", text)]


def _get_ocr_source(filename: str) -> str:
    """Extract OCR source from filename."""
    if filename.endswith("google_vision"):
        return "google_vision"
    elif filename.endswith("google_books"):
        return "google_books"
    return "unknown"


def _toc_quality_flag(markers: list[int], text_length: int) -> str:
    """Classify ToC quality based on marker positions."""
    if not markers:
        return "NO_MARKER"
    # Check if first marker is in first 20% of text
    if markers[0] > text_length * 0.2:
        return "MARKER_LATE"
    if len(markers) >= 2:
        return "MULTI_PAGE_TOC"
    return "SINGLE_TOC"


def _snippet(text: str, start: int, length: int = 300) -> str:
    """Get a text snippet, replacing newlines for display."""
    end = min(len(text), start + length)
    return text[start:end].replace("\n", " | ")


def review_staging_samples(output_path: Path | None = None):
    """Generate a review report for all benchmark samples."""
    output_path = output_path or DATA_DIR / "review_report.md"

    if not GROUND_TRUTH_PATH.exists():
        raise FileNotFoundError(
            f"No ground truth at {GROUND_TRUTH_PATH}. Run extraction first."
        )

    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    # Sort by segment count descending
    sorted_docs = sorted(
        ground_truth.items(),
        key=lambda x: len(x[1]["breakpoints"]),
        reverse=True,
    )

    lines = []
    lines.append("# Benchmark Sample Review Report\n")
    lines.append(f"Total candidates: {len(sorted_docs)}\n")

    # Summary table
    stats = {"NO_MARKER": 0, "MARKER_LATE": 0, "SINGLE_TOC": 0, "MULTI_PAGE_TOC": 0}

    lines.append("## Summary Table\n")
    lines.append("| # | Filename | OCR | Length | Segs | ToC Flag | Markers |")
    lines.append("|---|----------|-----|--------|------|----------|---------|")

    doc_details = []
    for i, (doc_id, gt) in enumerate(sorted_docs, 1):
        filename = gt["filename"]
        content_length = gt["content_length"]
        num_segments = len(gt["breakpoints"])
        ocr_source = _get_ocr_source(filename)

        # Read text to check for ToC markers
        text_path = SAMPLES_DIR / f"{doc_id}.txt"
        if text_path.exists():
            text = text_path.read_text(encoding="utf-8")
            markers = _detect_toc_markers(text)
            flag = _toc_quality_flag(markers, content_length)
        else:
            text = ""
            markers = []
            flag = "NO_FILE"

        stats[flag] = stats.get(flag, 0) + 1

        lines.append(
            f"| {i} | {filename} | {ocr_source} | {content_length:,} | "
            f"{num_segments} | {flag} | {len(markers)} |"
        )

        doc_details.append((i, doc_id, gt, text, markers, flag, ocr_source))

    lines.append("")
    lines.append("## Quality Distribution\n")
    for flag, count in sorted(stats.items()):
        lines.append(f"- **{flag}**: {count} documents")
    lines.append("")

    # Detailed per-document section
    lines.append("---\n")
    lines.append("## Document Details\n")

    for i, doc_id, gt, text, markers, flag, ocr_source in doc_details:
        filename = gt["filename"]
        content_length = gt["content_length"]
        num_segments = len(gt["breakpoints"])
        titles = gt["titles"]

        lines.append(f"### {i}. {filename}\n")
        lines.append(f"- **ID**: `{doc_id}`")
        lines.append(f"- **OCR**: {ocr_source}")
        lines.append(f"- **Length**: {content_length:,} chars")
        lines.append(f"- **Segments**: {num_segments}")
        lines.append(f"- **ToC flag**: {flag}")
        lines.append(f"- **དཀར་ཆག markers**: {len(markers)} at positions {markers[:5]}{'...' if len(markers) > 5 else ''}")

        if text:
            lines.append(f"\n**First 300 chars of text:**")
            lines.append(f"```\n{_snippet(text, 0, 300)}\n```")

            if markers:
                lines.append(f"\n**ToC region (from first marker):**")
                lines.append(f"```\n{_snippet(text, markers[0], 500)}\n```")

        lines.append(f"\n**Segment titles:**")
        for j, title in enumerate(titles):
            bp = gt["breakpoints"][j]
            lines.append(f"  {j+1}. [{bp:>8}] {title}")

        lines.append("\n---\n")

    report = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Review report saved to {output_path}")
    print(f"  Total: {len(sorted_docs)} documents")
    for flag, count in sorted(stats.items()):
        print(f"  {flag}: {count}")


if __name__ == "__main__":
    review_staging_samples()
