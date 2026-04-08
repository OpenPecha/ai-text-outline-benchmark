"""Evaluation metrics for text segmentation benchmark."""

from __future__ import annotations

import difflib
import statistics
from benchmark.config import TOLERANCE_VALUES, TITLE_SIMILARITY_THRESHOLD, WINDOWED_BIN_SIZE


# ---------------------------------------------------------------------------
# Metric 1: Breakpoint Matching (tolerance-based precision/recall/F1)
# ---------------------------------------------------------------------------

def match_breakpoints(
    predicted: list[int],
    ground_truth: list[int],
    tolerance: int,
) -> dict:
    """Match predicted breakpoints to ground truth within a tolerance window.

    Uses greedy matching: for each GT breakpoint (sorted), find the closest
    unmatched predicted breakpoint within tolerance.
    """
    pred_sorted = sorted(predicted)
    gt_sorted = sorted(ground_truth)
    used_pred = set()

    matched_pairs = []
    for gt_bp in gt_sorted:
        best_idx = None
        best_dist = tolerance + 1
        for i, pred_bp in enumerate(pred_sorted):
            if i in used_pred:
                continue
            dist = abs(pred_bp - gt_bp)
            if dist <= tolerance and dist < best_dist:
                best_idx = i
                best_dist = dist
        if best_idx is not None:
            used_pred.add(best_idx)
            matched_pairs.append((pred_sorted[best_idx], gt_bp, best_dist))

    tp = len(matched_pairs)
    fp = len(pred_sorted) - tp
    fn = len(gt_sorted) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    mean_offset = (
        statistics.mean(d for _, _, d in matched_pairs)
        if matched_pairs else 0.0
    )

    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "mean_offset": round(mean_offset, 2),
        "matched_pairs": matched_pairs,
    }


def breakpoint_metrics_at_tolerances(
    predicted: list[int],
    ground_truth: list[int],
    tolerances: list[int] | None = None,
) -> dict:
    """Compute breakpoint matching at multiple tolerance levels."""
    tolerances = tolerances or TOLERANCE_VALUES
    results = {}
    for tol in tolerances:
        m = match_breakpoints(predicted, ground_truth, tol)
        # Remove matched_pairs from summary (too verbose for aggregation)
        results[f"tolerance_{tol}"] = {
            k: v for k, v in m.items() if k != "matched_pairs"
        }
    return results


# ---------------------------------------------------------------------------
# Metric 2: Segment Count Accuracy
# ---------------------------------------------------------------------------

def segment_count_metrics(predicted_count: int, gt_count: int) -> dict:
    """Compare predicted vs ground truth segment counts."""
    return {
        "predicted_count": predicted_count,
        "ground_truth_count": gt_count,
        "absolute_error": abs(predicted_count - gt_count),
        "relative_error": round(
            abs(predicted_count - gt_count) / max(gt_count, 1), 4
        ),
        "over_segmented": predicted_count > gt_count,
    }


# ---------------------------------------------------------------------------
# Metric 3: Title Matching (fuzzy Tibetan text similarity)
# ---------------------------------------------------------------------------

def _string_similarity(a: str, b: str) -> float:
    """Compute similarity ratio between two strings using SequenceMatcher."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def match_titles(
    predicted_titles: list[str],
    gt_titles: list[str],
    threshold: float = TITLE_SIMILARITY_THRESHOLD,
) -> dict:
    """Match predicted titles to ground truth using fuzzy string matching.

    For each GT title, finds the best matching predicted title above threshold.
    """
    used_pred = set()
    matched = []

    for gt_title in gt_titles:
        best_idx = None
        best_sim = threshold  # minimum required
        for i, pred_title in enumerate(predicted_titles):
            if i in used_pred:
                continue
            sim = _string_similarity(pred_title, gt_title)
            if sim >= best_sim:
                best_idx = i
                best_sim = sim
        if best_idx is not None:
            used_pred.add(best_idx)
            matched.append((predicted_titles[best_idx], gt_title, best_sim))

    tp = len(matched)
    fp = len(predicted_titles) - tp
    fn = len(gt_titles) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    avg_sim = (
        statistics.mean(s for _, _, s in matched)
        if matched else 0.0
    )

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "avg_similarity": round(avg_sim, 4),
        "matched_count": tp,
        "unmatched_predicted": len(predicted_titles) - tp,
        "unmatched_ground_truth": len(gt_titles) - tp,
    }


# ---------------------------------------------------------------------------
# Metric 4: WindowDiff and Pk (standard text segmentation metrics)
# ---------------------------------------------------------------------------

def _breakpoints_to_bins(breakpoints: list[int], text_length: int, bin_size: int) -> list[int]:
    """Convert character-index breakpoints to a binary boundary array over bins.

    Returns a list of 0s and 1s, where 1 indicates a segment boundary in that bin.
    """
    num_bins = max(1, text_length // bin_size)
    bins = [0] * num_bins
    for bp in breakpoints:
        bin_idx = bp // bin_size
        if 0 <= bin_idx < num_bins:
            bins[bin_idx] = 1
    return bins


def _count_boundaries(bins: list[int], start: int, end: int) -> int:
    """Count boundaries in bin range [start, end)."""
    return sum(bins[start:end])


def compute_pk(
    predicted_bins: list[int],
    gt_bins: list[int],
    k: int | None = None,
) -> float:
    """Compute Pk metric (Beeferman et al. 1999).

    Probability that two points k apart are incorrectly classified as
    same/different segment. Lower is better (0-1).
    """
    n = len(gt_bins)
    if n < 2:
        return 0.0

    if k is None:
        # Default: half the average segment length
        num_boundaries = sum(gt_bins)
        avg_seg_len = n / max(num_boundaries + 1, 2)
        k = max(1, int(avg_seg_len / 2))

    errors = 0
    comparisons = 0
    for i in range(n - k):
        gt_same = _count_boundaries(gt_bins, i, i + k) == 0
        pred_same = _count_boundaries(predicted_bins, i, i + k) == 0
        if gt_same != pred_same:
            errors += 1
        comparisons += 1

    return errors / max(comparisons, 1)


def compute_windowdiff(
    predicted_bins: list[int],
    gt_bins: list[int],
    k: int | None = None,
) -> float:
    """Compute WindowDiff metric (Pevzner & Hearst 2002).

    Stricter than Pk — counts exact boundary count mismatches in window.
    Lower is better (0-1).
    """
    n = len(gt_bins)
    if n < 2:
        return 0.0

    if k is None:
        num_boundaries = sum(gt_bins)
        avg_seg_len = n / max(num_boundaries + 1, 2)
        k = max(1, int(avg_seg_len / 2))

    errors = 0
    comparisons = 0
    for i in range(n - k):
        gt_count = _count_boundaries(gt_bins, i, i + k)
        pred_count = _count_boundaries(predicted_bins, i, i + k)
        if gt_count != pred_count:
            errors += 1
        comparisons += 1

    return errors / max(comparisons, 1)


def windowed_metrics(
    predicted_breakpoints: list[int],
    gt_breakpoints: list[int],
    text_length: int,
    bin_size: int = WINDOWED_BIN_SIZE,
) -> dict:
    """Compute Pk and WindowDiff metrics."""
    pred_bins = _breakpoints_to_bins(predicted_breakpoints, text_length, bin_size)
    gt_bins = _breakpoints_to_bins(gt_breakpoints, text_length, bin_size)

    pk = compute_pk(pred_bins, gt_bins)
    wd = compute_windowdiff(pred_bins, gt_bins)

    return {
        "pk": round(pk, 4),
        "windowdiff": round(wd, 4),
        "num_bins": len(gt_bins),
        "bin_size": bin_size,
    }


# ---------------------------------------------------------------------------
# Combined: All metrics for one document
# ---------------------------------------------------------------------------

def compute_all_metrics(
    predicted: dict,
    ground_truth: dict,
    text_length: int,
) -> dict:
    """Compute all metrics for a single document.

    Args:
        predicted: {"breakpoints": [...], "toc": {"title": page, ...}}
        ground_truth: {"breakpoints": [...], "titles": [...]}
        text_length: Length of the document text in characters.
    """
    pred_bp = predicted.get("breakpoints", [])
    gt_bp = ground_truth.get("breakpoints", [])
    pred_titles = list(predicted.get("toc", {}).keys())
    gt_titles = ground_truth.get("titles", [])

    return {
        "breakpoint_matching": breakpoint_metrics_at_tolerances(pred_bp, gt_bp),
        "segment_count": segment_count_metrics(len(pred_bp), len(gt_bp)),
        "title_matching": match_titles(pred_titles, gt_titles),
        "windowed": windowed_metrics(pred_bp, gt_bp, text_length),
    }
