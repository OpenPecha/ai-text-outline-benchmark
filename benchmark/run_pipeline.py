"""Run the ai-text-outline package on benchmark samples and evaluate."""

from __future__ import annotations

import json
import time
import statistics
from datetime import datetime, timezone
from pathlib import Path

from ai_text_outline import extract_toc_indices

from benchmark.config import (
    SAMPLES_DIR,
    GROUND_TRUTH_PATH,
    API_CALL_DELAY,
    TOLERANCE_VALUES,
    current_version,
    version_paths,
)
from benchmark.metrics import compute_all_metrics


def run_benchmark(
    gemini_api_key: str | None = None,
    *,
    package_version: str | None = None,
    samples_dir: Path | None = None,
    predictions_dir: Path | None = None,
    ground_truth_path: Path | None = None,
    results_path: Path | None = None,
    api_call_delay: float | None = None,
):
    """Run extract_toc_indices on all samples and compute metrics.

    Results are written to data/results/{package_version}/ by default.
    Pass ``package_version`` to evaluate a specific version; omit it to
    auto-detect from the installed package.  Individual path overrides
    (predictions_dir, results_path) take precedence over the version dir.
    """
    pkg_ver = package_version or current_version()
    paths = version_paths(pkg_ver)

    samples_dir = samples_dir or SAMPLES_DIR
    predictions_dir = predictions_dir or paths.predictions_dir
    ground_truth_path = ground_truth_path or GROUND_TRUTH_PATH
    results_path = results_path or paths.results_path
    delay = API_CALL_DELAY if api_call_delay is None else api_call_delay

    print(f"Evaluating package version: {pkg_ver}")

    with open(ground_truth_path, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    predictions_dir.mkdir(parents=True, exist_ok=True)

    per_document = {}
    total = len(ground_truth)

    for i, (doc_id, gt) in enumerate(ground_truth.items(), 1):
        text_path = samples_dir / f"{doc_id}.txt"
        pred_path = predictions_dir / f"{doc_id}.json"

        print(f"[{i}/{total}] Processing {gt['filename']}...")

        # Use cached prediction if available
        if pred_path.exists():
            with open(pred_path, "r", encoding="utf-8") as f:
                prediction = json.load(f)
            print(f"  Using cached prediction")
        else:
            try:
                text = text_path.read_text(encoding="utf-8")
                kwargs = {"text": text}
                if gemini_api_key:
                    kwargs["gemini_api_key"] = gemini_api_key
                # Pass volume_id for vision-enhanced extraction
                kwargs["volume_id"] = gt["filename"]
                prediction = extract_toc_indices(**kwargs)

                # Cache prediction
                with open(pred_path, "w", encoding="utf-8") as f:
                    json.dump(prediction, f, ensure_ascii=False, indent=2)

                print(
                    f"  Predicted {len(prediction['breakpoints'])} breakpoints, "
                    f"{len(prediction['toc'])} TOC entries"
                )

                # Rate limit
                if i < total:
                    time.sleep(delay)

            except Exception as e:
                print(f"  ERROR: {e}")
                prediction = {"breakpoints": [], "toc": {}}
                per_document[doc_id] = {
                    "filename": gt["filename"],
                    "content_length": gt["content_length"],
                    "prediction": prediction,
                    "metrics": None,
                    "error": str(e),
                }
                continue

        # Compute metrics
        metrics = compute_all_metrics(
            predicted=prediction,
            ground_truth=gt,
            text_length=gt["content_length"],
        )

        per_document[doc_id] = {
            "filename": gt["filename"],
            "content_length": gt["content_length"],
            "prediction": {
                "num_breakpoints": len(prediction["breakpoints"]),
                "num_toc_entries": len(prediction["toc"]),
            },
            "metrics": metrics,
            "error": None,
        }

    # Compute aggregate statistics
    aggregate = _compute_aggregate(per_document)

    results = {
        "run_metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "package_version": pkg_ver,
            "num_documents": total,
            "tolerance_values": TOLERANCE_VALUES,
        },
        "per_document": per_document,
        "aggregate": aggregate,
    }

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {results_path}")
    _print_summary(aggregate)


def _compute_aggregate(per_document: dict) -> dict:
    """Compute aggregate statistics across all documents."""
    agg = {}

    # Collect values for each metric
    docs_with_metrics = [
        d for d in per_document.values() if d["metrics"] is not None
    ]

    if not docs_with_metrics:
        return {"error": "No documents produced metrics"}

    # Breakpoint F1 at each tolerance
    for tol in TOLERANCE_VALUES:
        key = f"tolerance_{tol}"
        values = [
            d["metrics"]["breakpoint_matching"][key]["f1"]
            for d in docs_with_metrics
            if key in d["metrics"]["breakpoint_matching"]
        ]
        if values:
            agg[f"breakpoint_f1_at_{tol}"] = _stats(values)

    # Segment count MAE
    count_errors = [
        d["metrics"]["segment_count"]["absolute_error"]
        for d in docs_with_metrics
    ]
    agg["segment_count_mae"] = _stats(count_errors)

    # Title matching F1
    title_f1s = [
        d["metrics"]["title_matching"]["f1"]
        for d in docs_with_metrics
    ]
    agg["title_f1"] = _stats(title_f1s)

    # Pk and WindowDiff
    pks = [d["metrics"]["windowed"]["pk"] for d in docs_with_metrics]
    wds = [d["metrics"]["windowed"]["windowdiff"] for d in docs_with_metrics]
    agg["pk"] = _stats(pks)
    agg["windowdiff"] = _stats(wds)

    # Success rate
    success_count = sum(1 for d in per_document.values() if d["error"] is None)
    agg["success_rate"] = round(success_count / len(per_document), 4)

    return agg


def _stats(values: list[float]) -> dict:
    """Compute summary statistics."""
    if not values:
        return {"mean": 0, "std": 0, "min": 0, "max": 0, "count": 0}
    return {
        "mean": round(statistics.mean(values), 4),
        "std": round(statistics.stdev(values), 4) if len(values) > 1 else 0,
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "count": len(values),
    }


def _print_summary(aggregate: dict):
    """Print a quick summary to console."""
    print("\n=== Aggregate Results ===")
    for key, val in aggregate.items():
        if isinstance(val, dict) and "mean" in val:
            print(f"  {key}: mean={val['mean']:.4f} std={val['std']:.4f} [{val['min']:.4f}, {val['max']:.4f}]")
        else:
            print(f"  {key}: {val}")


if __name__ == "__main__":
    run_benchmark()
