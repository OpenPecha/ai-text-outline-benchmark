"""Classify benchmark runs by predicted vs ground-truth segment count.

Tiers (using relative segment-count error vs ground truth):
  - success: relative error <= 5%
  - average: relative error > 5% and <= 20%
  - big_failure: relative error > 20%

Extraction/API failures (no metrics) are listed separately.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _rel_error(metrics: dict | None) -> float | None:
    if not metrics:
        return None
    sc = metrics.get("segment_count")
    if not sc:
        return None
    if "relative_error" in sc:
        return float(sc["relative_error"])
    p = int(sc.get("predicted_count", 0))
    g = int(sc.get("ground_truth_count", 0))
    if g <= 0:
        return None
    return abs(p - g) / g


def _f1_100(metrics: dict | None) -> float:
    if not metrics:
        return -1.0
    return float(
        metrics.get("breakpoint_matching", {})
        .get("tolerance_100", {})
        .get("f1", -1.0)
    )


def build_tiers(results_path: Path) -> dict:
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    extraction_failures: list[dict] = []
    success: list[dict] = []
    average: list[dict] = []
    big_failure: list[dict] = []

    for doc_id, doc in data["per_document"].items():
        if doc.get("error"):
            extraction_failures.append(
                {
                    "doc_id": doc_id,
                    "filename": doc["filename"],
                    "error": doc["error"],
                }
            )
            continue

        m = doc.get("metrics")
        sc = (m or {}).get("segment_count") or {}
        p = int(sc.get("predicted_count", 0))
        g = int(sc.get("ground_truth_count", 0))

        rel = _rel_error(m)
        if rel is None:
            if g > 0:
                rel = abs(p - g) / g
            elif p == 0:
                rel = 0.0
            else:
                rel = 1.0  # pred > 0 but gt == 0: treat as 100% mismatch

        row = {
            "doc_id": doc_id,
            "filename": doc["filename"],
            "predicted_count": p,
            "ground_truth_count": g,
            "relative_error": rel,
            "rel_pct": f"{100.0 * rel:.2f}%",
            "f1_at_100": _f1_100(m),
            "title_f1": float((m or {}).get("title_matching", {}).get("f1", -1.0)),
        }

        if rel <= 0.05:
            row["tier"] = "success"
            success.append(row)
        elif rel <= 0.20:
            row["tier"] = "average"
            average.append(row)
        else:
            row["tier"] = "big_failure"
            big_failure.append(row)

    success.sort(key=lambda r: (-r["f1_at_100"], -r["title_f1"], r["relative_error"]))
    average.sort(key=lambda r: (r["relative_error"], -r["f1_at_100"]))
    big_failure.sort(key=lambda r: (-r["relative_error"], r["f1_at_100"]))

    return {
        "meta": data.get("run_metadata", {}),
        "success": success,
        "average": average,
        "big_failure": big_failure,
        "extraction_failures": extraction_failures,
    }


def _md_table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
    if not rows:
        return "_None._\n"
    headers = [c[0] for c in cols]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for r in rows:
        cells = []
        for _, key in cols:
            v = r.get(key, "")
            if isinstance(v, float):
                cells.append(f"{v:.4f}" if v == v else "")  # nan check
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def render_markdown(tiers: dict) -> str:
    meta = tiers["meta"]
    n = meta.get("num_documents", "?")
    lines = [
        "# Segment-count tiering (pred vs ground-truth segments)",
        "",
        "Rules (relative error = |pred - gt| / gt):",
        "",
        "- **Success**: relative error ≤ 5% (over- or under-segmented within 5%).",
        "- **Average**: relative error > 5% and ≤ 20%.",
        "- **Big failure**: relative error > 20%.",
        "- **Extraction failure**: run errored (no metrics), e.g. API/image errors.",
        "",
        f"**Source run**: {meta.get('timestamp', '')} — **documents**: {n}",
        "",
        "## Counts",
        "",
        "| Tier | Count |",
        "| --- | ---: |",
        f"| Success (≤5%) | {len(tiers['success'])} |",
        f"| Average (5%–20%) | {len(tiers['average'])} |",
        f"| Big failure (>20%) | {len(tiers['big_failure'])} |",
        f"| Extraction failure | {len(tiers['extraction_failures'])} |",
        "",
        "## Best performers — success tier (sorted by F1@100, then title F1)",
        "",
        "Documents where segment count matched ground truth within **5%**.",
        "",
    ]

    cols = [
        ("Rank", "_rank"),
        ("Document", "filename"),
        ("Pred/GT", "_pg"),
        ("Rel % vs GT", "rel_pct"),
        ("F1@100", "f1_at_100"),
        ("Title F1", "title_f1"),
    ]
    succ = tiers["success"]
    for i, r in enumerate(succ, 1):
        r["_rank"] = i
        r["_pg"] = f"{r['predicted_count']}/{r['ground_truth_count']}"
    lines.append(_md_table(succ, cols))
    lines.append("## Average tier (5% < relative error ≤ 20%)")
    lines.append("")
    for r in tiers["average"]:
        r["_pg"] = f"{r['predicted_count']}/{r['ground_truth_count']}"
        r["_rank"] = ""
    lines.append(_md_table(tiers["average"], cols[1:]))

    lines.append("## Big failure tier (relative error > 20%)")
    lines.append("")
    for r in tiers["big_failure"]:
        r["_pg"] = f"{r['predicted_count']}/{r['ground_truth_count']}"
        r["_rank"] = ""
    lines.append(_md_table(tiers["big_failure"], cols[1:]))

    lines.append("## Extraction / API failures (no successful metrics)")
    lines.append("")
    ef = tiers["extraction_failures"]
    if not ef:
        lines.append("_None._\n")
    else:
        lines.append("| Document | Error (truncated) |")
        lines.append("| --- | --- |")
        for r in ef:
            err = (r["error"] or "")[:120]
            if len(r["error"] or "") > 120:
                err += "..."
            fn = r["filename"]
            lines.append(f"| {fn} | {err} |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="Tier docs by segment-count error vs GT.")
    p.add_argument(
        "--results",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "results.json",
        help="Path to results.json",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Markdown output path (default: <results_dir>/segment_tiers.md)",
    )
    args = p.parse_args()
    out = args.output or (args.results.parent / "segment_tiers.md")

    tiers = build_tiers(args.results)
    text = render_markdown(tiers)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    print(
        f"Success: {len(tiers['success'])}, "
        f"Average: {len(tiers['average'])}, "
        f"Big failure: {len(tiers['big_failure'])}, "
        f"Extraction failure: {len(tiers['extraction_failures'])}"
    )


if __name__ == "__main__":
    main()
