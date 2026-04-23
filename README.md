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

### Evaluate the currently installed version

```bash
# Images already downloaded; skip extract, images, and HF push
python -m benchmark.run_all --skip-extract --skip-images --skip-hf
```

Results are written to `data/results/<version>/` automatically.

### Evaluate a specific version

```bash
pip install "ai-text-outline==0.9.0"
python -m benchmark.run_all --skip-extract --skip-images --skip-hf
# writes to data/results/0.9.0/
```

Or name the version explicitly:

```bash
python -m benchmark.run_all --package-version 0.9.0 --skip-extract --skip-images --skip-hf
```

### Compare two versions

```bash
python -m benchmark.compare 0.8.0 0.9.0

# or compare everything in data/results/
python -m benchmark.compare --all

# write to a file
python -m benchmark.compare 0.8.0 0.9.0 --output data/comparison.md
```

See [docs/versioning.md](docs/versioning.md) for full details.

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

# 4. Run pipeline and evaluate (auto-detects installed version)
python -m benchmark.run_pipeline

# 5. Generate human-readable report
python -m benchmark.report

# 6. Tier documents by segment-count error
python -m benchmark.segment_tier_report

# 7. Compare versions
python -m benchmark.compare --all
```

## Data layout

```
data/
  samples/              # 124 Tibetan text files (.txt) — Git LFS, shared
  ground_truth.json     # Annotated breakpoints and titles — shared
  toc_images/           # BDRC page images — gitignored, ~81 MB
  results/
    0.8.0/              # One subdirectory per evaluated package version
      predictions/      # Per-document JSON outputs — Git LFS
      results.json      # Aggregate + per-document metrics
      report.md         # Human-readable summary
      segment_tiers.md  # Documents tiered by segment-count accuracy
    0.9.0/
      ...               # Same structure for each new version
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

## Multi-version evaluation

Each run writes to an isolated `data/results/{version}/` directory. Results for
different versions never overwrite each other. Use `benchmark.compare` to diff
any two versions. See [docs/versioning.md](docs/versioning.md) for the full workflow.

## Known failure modes

See [docs/failure_modes.md](docs/failure_modes.md) for documented failure patterns,
including over-extraction cases, Gemini image errors, and ToC truncation.

## Links

- Package: [ai-text-outline on PyPI](https://pypi.org/project/ai-text-outline/)
- Package source: [OpenPecha/ai-text-outline](https://github.com/OpenPecha/ai-text-outline)
- HuggingFace dataset: [openpecha/ai-text-outline-benchmark](https://huggingface.co/datasets/openpecha/ai-text-outline-benchmark)
