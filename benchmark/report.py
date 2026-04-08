"""Generate markdown report from benchmark results."""

import json
from tabulate import tabulate
from benchmark.config import RESULTS_PATH, REPORT_PATH, TOLERANCE_VALUES


def generate_report():
    """Generate a markdown report from results.json."""
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)

    meta = results["run_metadata"]
    agg = results["aggregate"]
    per_doc = results["per_document"]

    lines = []
    lines.append("# Benchmark Evaluation Report")
    lines.append("")
    lines.append(f"**Package version**: {meta['package_version']}")
    lines.append(f"**Timestamp**: {meta['timestamp']}")
    lines.append(f"**Documents evaluated**: {meta['num_documents']}")
    lines.append(f"**Success rate**: {agg.get('success_rate', 'N/A')}")
    lines.append("")

    # --- Aggregate Summary ---
    lines.append("## Aggregate Metrics")
    lines.append("")

    summary_rows = []
    for tol in TOLERANCE_VALUES:
        key = f"breakpoint_f1_at_{tol}"
        if key in agg:
            v = agg[key]
            summary_rows.append([
                f"Breakpoint F1 @{tol}",
                f"{v['mean']:.4f}",
                f"{v['std']:.4f}",
                f"{v['min']:.4f}",
                f"{v['max']:.4f}",
            ])

    for metric_name, key in [
        ("Segment Count MAE", "segment_count_mae"),
        ("Title F1", "title_f1"),
        ("Pk (lower=better)", "pk"),
        ("WindowDiff (lower=better)", "windowdiff"),
    ]:
        if key in agg:
            v = agg[key]
            summary_rows.append([
                metric_name,
                f"{v['mean']:.4f}",
                f"{v['std']:.4f}",
                f"{v['min']:.4f}",
                f"{v['max']:.4f}",
            ])

    lines.append(tabulate(
        summary_rows,
        headers=["Metric", "Mean", "Std", "Min", "Max"],
        tablefmt="github",
    ))
    lines.append("")

    # --- Per-Document Table ---
    lines.append("## Per-Document Results")
    lines.append("")

    doc_rows = []
    for doc_id, doc in per_doc.items():
        if doc["error"]:
            doc_rows.append([
                doc["filename"][:40],
                "ERROR",
                "-", "-", "-", "-", "-",
            ])
            continue

        m = doc["metrics"]
        sc = m["segment_count"]
        f1_100 = m["breakpoint_matching"].get("tolerance_100", {}).get("f1", "-")
        f1_200 = m["breakpoint_matching"].get("tolerance_200", {}).get("f1", "-")
        title_f1 = m["title_matching"]["f1"]
        pk = m["windowed"]["pk"]

        doc_rows.append([
            doc["filename"][:40],
            f"{sc['predicted_count']}/{sc['ground_truth_count']}",
            f"{f1_100}",
            f"{f1_200}",
            f"{title_f1}",
            f"{pk}",
            doc["error"] or "OK",
        ])

    lines.append(tabulate(
        doc_rows,
        headers=["Document", "Pred/GT Segs", "F1@100", "F1@200", "Title F1", "Pk", "Status"],
        tablefmt="github",
    ))
    lines.append("")

    # --- Failure Analysis ---
    failures = [
        (doc_id, doc) for doc_id, doc in per_doc.items() if doc["error"]
    ]
    if failures:
        lines.append("## Failure Analysis")
        lines.append("")
        for doc_id, doc in failures:
            lines.append(f"- **{doc['filename']}**: {doc['error']}")
        lines.append("")

    report_text = "\n".join(lines)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Report saved to {REPORT_PATH}")
    print("\n" + report_text)


if __name__ == "__main__":
    generate_report()
