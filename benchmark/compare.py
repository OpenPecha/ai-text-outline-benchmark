"""Compare benchmark results across ai-text-outline package versions.

Usage:
    # Compare two specific versions
    python -m benchmark.compare 0.8.0 0.9.0

    # Compare all versions found in data/results/
    python -m benchmark.compare --all

    # Write comparison to a file
    python -m benchmark.compare 0.8.0 0.9.0 --output data/comparison.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark.config import RESULTS_DIR, TOLERANCE_VALUES


def load_results(version: str) -> dict | None:
    path = RESULTS_DIR / version / "results.json"
    if not path.exists():
        print(f"  Warning: no results found for {version} at {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_available_versions() -> list[str]:
    """Return all versions that have a results.json, sorted."""
    if not RESULTS_DIR.exists():
        return []
    versions = [
        d.name for d in sorted(RESULTS_DIR.iterdir())
        if d.is_dir() and (d / "results.json").exists()
    ]
    return versions


def _agg_val(agg: dict, key: str) -> str:
    v = agg.get(key)
    if v is None:
        return "—"
    if isinstance(v, dict) and "mean" in v:
        return f"{v['mean']:.4f}"
    return str(v)


def build_comparison(versions: list[str]) -> str:
    all_results = {}
    for ver in versions:
        r = load_results(ver)
        if r:
            all_results[ver] = r

    if not all_results:
        return "No results found for the requested versions."

    lines = [
        "# Version Comparison",
        "",
        "Metrics are means across all documents evaluated in each run.",
        "",
    ]

    # Header row
    header = ["Metric"] + list(all_results.keys())
    sep = ["---"] + ["---:"] * len(all_results)
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(sep) + " |")

    # Rows
    metric_keys = [
        (f"Breakpoint F1 @{tol}", f"breakpoint_f1_at_{tol}")
        for tol in TOLERANCE_VALUES
    ] + [
        ("Segment Count MAE", "segment_count_mae"),
        ("Title F1", "title_f1"),
        ("Pk (↓)", "pk"),
        ("WindowDiff (↓)", "windowdiff"),
        ("Success rate", "success_rate"),
    ]

    for label, key in metric_keys:
        row = [label]
        for ver, r in all_results.items():
            agg = r.get("aggregate", {})
            row.append(_agg_val(agg, key))
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    # Per-run metadata
    lines.append("## Run metadata")
    lines.append("")
    meta_header = ["Version", "Timestamp", "Documents"]
    lines.append("| " + " | ".join(meta_header) + " |")
    lines.append("| --- | --- | ---: |")
    for ver, r in all_results.items():
        m = r.get("run_metadata", {})
        lines.append(f"| {ver} | {m.get('timestamp', '—')} | {m.get('num_documents', '—')} |")

    lines.append("")

    # Delta section (only when exactly 2 versions)
    ver_list = list(all_results.keys())
    if len(ver_list) == 2:
        v1, v2 = ver_list
        lines.append(f"## Delta: {v2} vs {v1} (positive = improvement)")
        lines.append("")
        lines.append("| Metric | Delta |")
        lines.append("| --- | ---: |")
        for label, key in metric_keys:
            a1 = all_results[v1].get("aggregate", {})
            a2 = all_results[v2].get("aggregate", {})

            def _num(agg: dict, k: str) -> float | None:
                v = agg.get(k)
                if v is None:
                    return None
                if isinstance(v, dict):
                    return v.get("mean")
                if isinstance(v, (int, float)):
                    return float(v)
                return None

            n1, n2 = _num(a1, key), _num(a2, key)
            if n1 is not None and n2 is not None:
                delta = n2 - n1
                # For lower-is-better metrics, negate the sign display
                if key in ("pk", "windowdiff", "segment_count_mae"):
                    sign = "+" if delta < 0 else ("-" if delta > 0 else "")
                    display = f"{sign}{abs(delta):.4f}"
                else:
                    sign = "+" if delta > 0 else ""
                    display = f"{sign}{delta:.4f}"
                lines.append(f"| {label} | {display} |")
            else:
                lines.append(f"| {label} | — |")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare benchmark results across versions.")
    parser.add_argument(
        "versions", nargs="*",
        help="Package versions to compare (e.g. 0.8.0 0.9.0). Omit to use --all.",
    )
    parser.add_argument("--all", action="store_true",
                        help="Compare all versions found in data/results/")
    parser.add_argument("--output", type=Path, default=None,
                        help="Write comparison to this file (default: print to stdout)")
    args = parser.parse_args()

    if args.all:
        versions = list_available_versions()
        if not versions:
            print("No results found in data/results/")
            return
        print(f"Found versions: {', '.join(versions)}")
    elif args.versions:
        versions = args.versions
    else:
        versions = list_available_versions()
        if not versions:
            print("No results found. Run benchmark.run_all first.")
            return
        if len(versions) == 1:
            print(f"Only one version available ({versions[0]}). Need at least two to compare.")
            print("Run the benchmark with a newer version first.")
            return

    text = build_comparison(versions)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"Comparison written to {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
