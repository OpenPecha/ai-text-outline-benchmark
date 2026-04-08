# Benchmark Guide

Complete guide for evaluating the `ai-text-outline` package and comparing different versions.

---

## Table of Contents

1. [Overview](#overview)
2. [Testing with a New Package Version](#testing-with-a-new-package-version)
3. [Testing with a Different Package](#testing-with-a-different-package)
4. [Evaluation Metrics Explained](#evaluation-metrics-explained)
5. [Interpreting Results](#interpreting-results)
6. [Baseline Results (v0.5.0)](#baseline-results-v050)

---

## Overview

This benchmark evaluates how accurately a ToC extraction package can detect **section boundaries** (breakpoints) and **section titles** in Tibetan texts.

### What is being measured?

Given a Tibetan text document, the package produces:
```python
{
    "breakpoints": [5035, 6583, 7702, ...],   # character indices where sections start
    "toc": {"Title A": 5, "Title B": 10, ...}  # extracted section titles with page numbers
}
```

The benchmark compares this output against **human-annotated ground truth** from the outliner tool database, which provides the correct section boundaries and titles.

### Pipeline flow

```
Database (ground truth)     Package (predictions)
        |                           |
        v                           v
  ground_truth.json          predictions/*.json
        |                           |
        +----------+----------------+
                   |
                   v
            metrics.py (compare)
                   |
                   v
             results.json
                   |
                   v
              report.md
```

---

## Testing with a New Package Version

When you release a new version of `ai-text-outline` (e.g., v0.6.0), you can re-run the benchmark to compare performance against previous versions.

### Step 1: Install the new version

```bash
# From PyPI
pip install ai-text-outline==0.6.0

# Or from local source (editable)
pip install -e /path/to/ai-text-outline
```

### Step 2: Clear cached predictions

The benchmark caches API predictions in `data/predictions/`. You must clear these to force re-running with the new version:

```bash
# Delete all cached predictions
rm -rf data/predictions/*.json
```

If you skip this step, the benchmark will use the old cached results and you won't see any difference.

### Step 3: Re-run the pipeline

```bash
# Set your API key
export GEMINI_API_KEY="your-key"

# Run only the pipeline + report (skip data extraction and HF push)
python -m benchmark.run_all --skip-extract --skip-hf
```

This will:
1. Re-run `extract_toc_indices()` on all 10 benchmark samples using the new package version
2. Compute all evaluation metrics
3. Generate a new `data/report.md`

### Step 4: Compare results

The report includes the package version in the header. Compare `data/results.json` from different runs to track improvements:

```python
import json

# Load results from different versions
with open("data/results_v050.json") as f:
    v050 = json.load(f)
with open("data/results.json") as f:
    v060 = json.load(f)

# Compare aggregate F1@200
old_f1 = v050["aggregate"]["breakpoint_f1_at_200"]["mean"]
new_f1 = v060["aggregate"]["breakpoint_f1_at_200"]["mean"]
print(f"F1@200: {old_f1:.4f} -> {new_f1:.4f} ({new_f1 - old_f1:+.4f})")
```

**Tip**: Before clearing predictions, rename `data/results.json` to `data/results_v050.json` to preserve the old results for comparison.

### Quick reference: Re-run commands

```bash
# Save old results
cp data/results.json data/results_v050.json

# Install new version
pip install ai-text-outline==0.6.0

# Clear predictions cache and re-run
rm -rf data/predictions/*.json
export GEMINI_API_KEY="your-key"
python -m benchmark.run_all --skip-extract --skip-hf

# View report
cat data/report.md
```

---

## Testing with a Different Package

If you want to benchmark a completely different extraction package (not `ai-text-outline`), you need to write an adapter that produces output in the expected format.

### Expected output format

The benchmark expects predictions as a JSON dict with two keys:

```python
{
    "breakpoints": [5035, 6583, 7702, ...],  # sorted list of character indices (int)
    "toc": {                                  # dict mapping title string to page number
        "Section Title 1": 5,
        "Section Title 2": 10,
    }
}
```

### Option A: Write a custom runner

Create a script that generates predictions in the correct format:

```python
# custom_runner.py
import json
from pathlib import Path
from your_package import your_extraction_function

SAMPLES_DIR = Path("data/samples")
PREDICTIONS_DIR = Path("data/predictions")
GROUND_TRUTH_PATH = Path("data/ground_truth.json")

with open(GROUND_TRUTH_PATH) as f:
    ground_truth = json.load(f)

PREDICTIONS_DIR.mkdir(exist_ok=True)

for doc_id in ground_truth:
    text = (SAMPLES_DIR / f"{doc_id}.txt").read_text(encoding="utf-8")

    # Call your package — adapt this to your API
    result = your_extraction_function(text)

    # Convert to expected format
    prediction = {
        "breakpoints": result["breakpoints"],  # must be list[int]
        "toc": result["toc"],                   # must be dict[str, int]
    }

    with open(PREDICTIONS_DIR / f"{doc_id}.json", "w", encoding="utf-8") as f:
        json.dump(prediction, f, ensure_ascii=False, indent=2)

    print(f"Processed {doc_id}")
```

Then run evaluation + report only:

```bash
python custom_runner.py
python -m benchmark.run_all --skip-extract --skip-hf --skip-run
```

The `--skip-run` flag tells the orchestrator not to call `extract_toc_indices`, and it will use your cached predictions from `data/predictions/` instead.

### Option B: Modify run_pipeline.py

If you want to integrate directly, edit `benchmark/run_pipeline.py` and replace the import and function call:

```python
# Change this:
from ai_text_outline import extract_toc_indices

# To this:
from your_package import your_function as extract_toc_indices
```

Make sure your function returns the same dict format: `{"breakpoints": list[int], "toc": dict[str, int]}`.

---

## Evaluation Metrics Explained

The benchmark uses four metric groups, each measuring a different aspect of extraction quality.

---

### Metric 1: Breakpoint Matching (Tolerance-based Precision/Recall/F1)

**What it measures**: How accurately the package identifies where sections start in the text.

**The problem**: Predicted breakpoints will rarely be *exactly* at the same character index as ground truth. The package might find a section starts at character 5042 while the annotator marked it at 5035. A strict exact-match comparison would count this as wrong, even though it's essentially correct.

**Solution — tolerance window**: We allow a configurable tolerance. If a predicted breakpoint is within N characters of a ground truth breakpoint, it counts as a match.

**How it works**:

```
Ground truth breakpoints:  [5035,     6583,     7702    ]
Predicted breakpoints:     [5042,     6600,     9000    ]
                            |          |          |
Tolerance = 50:            match(7)   match(17)  no match
Tolerance = 200:           match(7)   match(17)  no match
```

1. Sort both predicted and ground truth breakpoints
2. For each ground truth breakpoint, find the nearest unmatched predicted breakpoint within the tolerance window
3. Each predicted breakpoint can only match one ground truth breakpoint (greedy 1-to-1 matching)
4. Count True Positives (matched), False Positives (predicted but unmatched), False Negatives (ground truth but unmatched)

**Formulas**:
```
Precision = TP / (TP + FP)    "Of all predicted breakpoints, how many were correct?"
Recall    = TP / (TP + FN)    "Of all real breakpoints, how many did we find?"
F1        = 2 * P * R / (P + R)   "Harmonic mean of precision and recall"
```

**Tolerance levels tested**: 50, 100, 200, 500 characters

| Tolerance | Meaning |
|-----------|---------|
| 50 chars | Very strict — prediction must be within ~1 line of ground truth |
| 100 chars | Strict — within ~2-3 lines |
| 200 chars | Moderate — within a small paragraph |
| 500 chars | Lenient — within half a page |

**Also reports**:
- `mean_offset`: Average distance (in characters) between matched pairs. Lower = more precise positioning.

**Ideal scores**: F1 = 1.0 means every predicted breakpoint matched a ground truth breakpoint (and vice versa) within the tolerance.

---

### Metric 2: Segment Count Accuracy

**What it measures**: Whether the package finds the right *number* of sections, regardless of position.

**Why it matters**: Even if breakpoint positions are slightly off, finding the correct number of segments indicates the package understands the document structure.

**Outputs**:
| Field | Meaning |
|-------|---------|
| `predicted_count` | Number of breakpoints the package found |
| `ground_truth_count` | Number of breakpoints in human annotation |
| `absolute_error` | `|predicted - ground_truth|` |
| `relative_error` | `absolute_error / ground_truth_count` |
| `over_segmented` | `true` if predicted more segments than exist |

**Example**:
```
Predicted: 27 segments, Ground truth: 28 segments
  -> absolute_error = 1
  -> relative_error = 0.036 (3.6% off)
  -> over_segmented = false
```

**Ideal scores**: absolute_error = 0, relative_error = 0.

---

### Metric 3: Title Matching (Fuzzy Tibetan Text Similarity)

**What it measures**: Whether the AI-extracted section titles match the human-annotated titles.

**The problem**: The package extracts titles from the ToC section using Gemini AI. The human annotator independently labels each segment with a title. These may differ due to:
- Slight OCR errors in the text
- Different spelling conventions
- Truncation or abbreviation
- AI extracting a slightly different portion of the title

**Solution — fuzzy matching**: Uses Python's `difflib.SequenceMatcher` to compute character-level similarity between strings. This works well for Tibetan Unicode text.

**How it works**:
1. For each ground truth title, find the most similar predicted title
2. If similarity >= 0.7 (70%), count as a match
3. Each predicted title can only match one ground truth title
4. Compute precision, recall, F1 same as breakpoint matching

**Similarity calculation**:
```python
# SequenceMatcher finds the longest common subsequences
similarity("Section Alpha", "Section Alpah") = 0.923  # typo tolerance
similarity("Chapter 1", "Something Else")    = 0.111  # very different
```

**The 0.7 threshold**: A similarity of 70% means roughly 70% of the characters match in sequence. This is lenient enough to handle minor OCR/transcription differences but strict enough to reject unrelated titles.

**Outputs**:
| Field | Meaning |
|-------|---------|
| `precision` | Of all predicted titles, how many matched a ground truth title? |
| `recall` | Of all ground truth titles, how many were found by the package? |
| `f1` | Harmonic mean of precision and recall |
| `avg_similarity` | Mean similarity score of matched pairs (0-1) |

**Ideal scores**: F1 = 1.0, avg_similarity = 1.0.

---

### Metric 4: Pk and WindowDiff (Standard Text Segmentation Metrics)

These are established metrics from the NLP text segmentation literature, designed specifically for evaluating boundary detection.

#### How they work (shared concept)

Both metrics slide a window of size `k` across the text and compare predicted vs ground truth boundaries within each window position:

```
Text:   [  segment 1  |  segment 2  |    segment 3    |  seg 4  ]
         ▼ window ▼
         [____k____]  -> count boundaries in this window
              [____k____]  -> slide right by 1 bin
                   [____k____]  -> slide again
                        ...
```

**Binning**: Since the text can be hundreds of thousands of characters, we first bin it into 100-character chunks. Each bin is marked as 1 (boundary here) or 0 (no boundary). This makes computation efficient without losing meaningful resolution.

**Window size k**: By default, half the average segment length. This adapts to the document structure.

#### Pk (Beeferman et al. 1999)

For each window position, Pk asks: **"Do predicted and ground truth agree on whether these two points are in the same segment?"**

```
Window at position i:
  GT says: 0 boundaries in window  -> "same segment"
  Pred says: 1 boundary in window  -> "different segments"
  -> DISAGREE = error

Pk = (number of disagreements) / (total window positions)
```

**Range**: 0 to 1 (lower is better). Pk = 0 means perfect agreement. Pk = 0.5 means the prediction is essentially random.

**Known limitation**: Pk penalizes false negatives (missed boundaries) more than false positives (extra boundaries) when segments are of unequal length.

#### WindowDiff (Pevzner & Hearst 2002)

WindowDiff is stricter than Pk. Instead of asking "same or different segment?", it asks: **"Is the exact number of boundaries in this window correct?"**

```
Window at position i:
  GT boundary count in window:   1
  Pred boundary count in window: 2
  -> DIFFERENT = error (even though both say "not same segment")

WindowDiff = (number of mismatches) / (total window positions)
```

**Range**: 0 to 1 (lower is better).

**Key difference from Pk**: If the ground truth has 1 boundary in a window and prediction has 2, Pk might say "both agree it's different segments" (no error), but WindowDiff says "wrong count" (error). This catches over-segmentation that Pk misses.

#### When to use which?

| Situation | Pk | WindowDiff |
|-----------|------|------|
| Quick sanity check | Good | - |
| Comparing two versions | Good | Better |
| Detecting over-segmentation | Misses it | Catches it |
| Published benchmarks | Often reported | Preferred |

**Ideal scores**: Both = 0.0 (perfect segmentation).

---

## Interpreting Results

### Reading the report

The report (`data/report.md`) contains:

1. **Aggregate Metrics**: Mean/std/min/max across all documents
2. **Per-Document Table**: Individual document results

### What to look for

**Good performance indicators**:
- F1@200 > 0.7 — most breakpoints are within 200 chars of ground truth
- Title F1 > 0.6 — most titles are correctly extracted
- Pk < 0.15 — segmentation is mostly correct
- Segment Count MAE < 5 — within 5 segments of ground truth

**Warning signs**:
- F1@200 = 0 for a document — the package found no breakpoints at all (likely no ToC detected)
- High variance (std) — inconsistent performance across document types
- Pred/GT ratio far from 1.0 — systematic over- or under-segmentation

### Common failure modes

| Symptom | Likely cause |
|---------|--------------|
| 0 breakpoints predicted | No recognizable ToC in the first 1/5 of text |
| Many more predicted than GT | Over-segmentation: package splitting at minor headings |
| Good F1@500 but poor F1@50 | Correct sections found, but boundary positions are imprecise |
| Good breakpoint F1 but poor title F1 | Positions correct, but AI extracted wrong title text |

---

## Baseline Results (v0.5.0)

These are the results from the initial benchmark run with `ai-text-outline` v0.5.0 on 10 approved documents:

| Metric                    |    Mean |     Std |    Min |    Max |
|---------------------------|---------|---------|--------|--------|
| Breakpoint F1 @50         |  0.121  |  0.222  | 0      |  0.6   |
| Breakpoint F1 @100        |  0.315  |  0.323  | 0      |  0.95  |
| Breakpoint F1 @200        |  0.494  |  0.406  | 0      |  1.0   |
| Breakpoint F1 @500        |  0.501  |  0.404  | 0      |  1.0   |
| Segment Count MAE         | 10.3    | 13.4    | 0      | 40     |
| Title F1                  |  0.420  |  0.398  | 0      |  1.0   |
| Pk (lower=better)         |  0.212  |  0.154  | 0.002  |  0.404 |
| WindowDiff (lower=better) |  0.233  |  0.140  | 0.004  |  0.404 |

**Key takeaways**:
- 3/10 documents returned empty (no ToC detected) — dragging down averages
- Best case (W3KG239): near-perfect F1@200 = 1.0, Pk = 0.002
- When the package does find a ToC, it performs well (F1@200 > 0.6 for 6/7 non-empty results)
- High variance indicates strong dependence on text formatting and ToC structure
