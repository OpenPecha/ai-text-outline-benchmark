# ai-text-outline-benchmark

Evaluation pipeline for [ai-text-outline](https://github.com/OpenPecha/ai-text-outline) —
a package that extracts Table of Contents indices from Tibetan texts.

**Current results (v0.8.0, 124 documents):**
- Mean F1@100: **0.43**
- Success rate (≤5% segment-count error): **85.5%**
- Dataset: [openpecha/ai-text-outline-benchmark](https://huggingface.co/datasets/openpecha/ai-text-outline-benchmark)

## Quickstart

```bash
git clone https://github.com/OpenPecha/ai-text-outline-benchmark.git
cd ai-text-outline-benchmark
pip install -e .
```

Set environment variables:

```bash
export GEMINI_API_KEY=...
export IIIF_API_KEY=...
export HF_TOKEN=...
# Database (only needed to re-extract samples)
export BENCHMARK_DB_HOST=...
export BENCHMARK_DB_USER=...
export BENCHMARK_DB_PASSWORD=...
export BENCHMARK_DB_NAME=...
```

### Reproduce from the HuggingFace dataset

```bash
# Skip DB extraction — use the published 124-doc dataset
python -m benchmark.run_all --skip-extract
```

This downloads ToC images, runs the pipeline on all 124 documents, and generates
`data/report.md` and `data/segment_tiers.md`.

### Full pipeline from scratch

```bash
# Extract samples from DB, download images, run pipeline, push to HF, generate reports
python -m benchmark.run_all
```

### Step by step

```bash
# 1. Extract samples from database (or skip if you have data/)
python -m benchmark.extract_data

# 2. Download BDRC IIIF ToC images
python -m benchmark.download_toc_images

# 3. Push to HuggingFace
python -m benchmark.prepare_dataset

# 4. Run pipeline and evaluate
python -m benchmark.run_pipeline

# 5. Generate human-readable report
python -m benchmark.report

# 6. Tier documents by segment-count error
python -m benchmark.segment_tier_report
```

## Data layout

```
data/
  samples/          # 124 Tibetan text files (.txt) — Git LFS
  predictions/      # 124 pipeline outputs (.json) — Git LFS
  ground_truth.json # Annotated breakpoints and titles for 124 documents
  results.json      # Full evaluation metrics
  report.md         # Human-readable results summary
  segment_tiers.md  # Documents tiered by segment-count accuracy
  review_report.md  # Per-document QA review
  toc_images/       # BDRC page images (gitignored, ~81 MB — downloaded at run time)
```

## Dataset schema

Each row in the HuggingFace dataset (`openpecha/ai-text-outline-benchmark`) contains:

| Field | Type | Description |
|---|---|---|
| `doc_id` | string | UUID document identifier |
| `filename` | string | Source BDRC filename |
| `text` | string | Full Tibetan text content |
| `breakpoints` | list[int] | Ground-truth section start character indices |
| `titles` | list[str] | Ground-truth section titles |
| `content_length` | int | Text length in characters |
| `version` | string | `ai-text-outline` version used for evaluation |

## Evaluation metrics

See [docs/metrics.md](docs/metrics.md) for full definitions.

| Metric | Description | Range |
|---|---|---|
| Breakpoint F1@N | Precision/recall of breakpoints within N chars tolerance | 0–1 (higher = better) |
| Segment count MAE | Absolute error in number of detected segments | 0+ (lower = better) |
| Title F1 | Fuzzy match of extracted titles vs ground truth | 0–1 (higher = better) |
| Pk | Standard text segmentation penalty | 0–1 (lower = better) |
| WindowDiff | Stricter segmentation quality metric | 0–1 (lower = better) |

## Segment tiering

Documents are classified by the relative error between predicted and ground-truth segment count:

| Tier | Condition |
|---|---|
| Success | relative error ≤ 5% |
| Average | 5% < relative error ≤ 20% |
| Big failure | relative error > 20% |
| Extraction failure | pipeline error (no metrics) |

See [docs/segment_tiering.md](docs/segment_tiering.md) for details.

## Known failure modes

See [docs/failure_modes.md](docs/failure_modes.md) for documented failure patterns,
including over-extraction cases, Gemini image errors, and ToC truncation.

## Links

- Package: [ai-text-outline on PyPI](https://pypi.org/project/ai-text-outline/)
- Package source: [OpenPecha/ai-text-outline](https://github.com/OpenPecha/ai-text-outline)
- HuggingFace dataset: [openpecha/ai-text-outline-benchmark](https://huggingface.co/datasets/openpecha/ai-text-outline-benchmark)
