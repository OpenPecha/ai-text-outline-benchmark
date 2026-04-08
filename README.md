# ai-text-outline-benchmark

Benchmark evaluation pipeline for the [ai-text-outline](https://github.com/OpenPecha/ai-text-outline) package.

Extracts annotated Tibetan text samples from the outliner tool database, runs the ToC extraction pipeline, and evaluates accuracy using multiple metrics.

## Setup

```bash
pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required environment variables:
- `BENCHMARK_DB_HOST`, `BENCHMARK_DB_USER`, `BENCHMARK_DB_PASSWORD` — PostgreSQL database
- `GEMINI_API_KEY` — for running the extraction pipeline
- `HF_TOKEN` — for pushing dataset to HuggingFace Hub

## Usage

### Full pipeline

```bash
python -m benchmark.run_all
```

### Step by step

```bash
# 1. Extract samples from database
python -m benchmark.extract_data

# 2. Push HuggingFace dataset
python -m benchmark.prepare_dataset

# 3. Run pipeline and evaluate
python -m benchmark.run_pipeline

# 4. Generate report
python -m benchmark.report
```

### Skip steps (use cached data)

```bash
# Skip extraction, use cached samples
python -m benchmark.run_all --skip-extract

# Skip everything except report
python -m benchmark.run_all --skip-extract --skip-hf --skip-run
```

## Evaluation Metrics

| Metric | Description | Range |
|--------|-------------|-------|
| Breakpoint F1 @N | Precision/recall of breakpoints within N chars tolerance | 0-1 (higher=better) |
| Segment Count MAE | Absolute error in number of detected segments | 0+ (lower=better) |
| Title F1 | Fuzzy match of extracted titles vs ground truth | 0-1 (higher=better) |
| Pk | Standard text segmentation metric | 0-1 (lower=better) |
| WindowDiff | Stricter segmentation quality metric | 0-1 (lower=better) |

## Output

- `data/samples/` — extracted text files
- `data/ground_truth.json` — annotated breakpoints and titles
- `data/predictions/` — cached pipeline outputs
- `data/results.json` — full evaluation results
- `data/report.md` — human-readable report
