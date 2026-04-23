# Evaluating Multiple Package Versions

The benchmark stores results per `ai-text-outline` version so runs never
overwrite each other and you can compare any two versions side by side.

## Directory layout

```
data/
  samples/              # shared — never changes between versions
  ground_truth.json     # shared — ground truth breakpoints and titles
  toc_images/           # shared — gitignored, downloaded at run time
  results/
    0.8.0/
      predictions/      # per-document JSON outputs (Git LFS)
      results.json      # aggregate + per-document metrics
      report.md         # human-readable summary
      segment_tiers.md  # documents tiered by segment-count accuracy
    0.9.0/
      predictions/
      results.json
      report.md
      segment_tiers.md
    ...
```

`data/samples/` and `data/ground_truth.json` are the fixed evaluation corpus.
Everything under `data/results/{version}/` belongs to one run and is independent.

## Evaluating a new version

### 1. Install the new version

```bash
pip install "ai-text-outline==0.9.0"
# or from local source:
pip install -e ../ai-text-outline
```

### 2. Run the benchmark

The orchestrator auto-detects the installed version:

```bash
python -m benchmark.run_all --skip-extract --skip-images --skip-hf
```

This writes results to `data/results/0.9.0/` (or whatever version is installed).

To be explicit about the version:

```bash
python -m benchmark.run_all \
  --package-version 0.9.0 \
  --skip-extract --skip-images --skip-hf
```

### 3. Or run individual steps

```bash
# Run pipeline only — writes predictions + results.json
python -m benchmark.run_pipeline  # auto-detects version

# Generate report from results
python -m benchmark.report

# Generate segment-tier report
python -m benchmark.segment_tier_report
```

All three modules default to the installed package version. Pass
`--package-version X.Y.Z` (for CLI modules) or `package_version="X.Y.Z"` (for
the Python API) to override.

## Comparing versions

```bash
# Compare two specific versions
python -m benchmark.compare 0.8.0 0.9.0

# Compare all versions found in data/results/
python -m benchmark.compare --all

# Write the comparison table to a file
python -m benchmark.compare 0.8.0 0.9.0 --output data/comparison.md
```

The comparison table shows mean values for each metric across versions. When
exactly two versions are compared, a delta row is included (positive = improvement
for higher-is-better metrics; the sign is adjusted for lower-is-better metrics
like Pk and segment MAE).

Example output:

```
| Metric              | 0.8.0  | 0.9.0  |
| ---                 | ---:   | ---:   |
| Breakpoint F1 @100  | 0.4300 | 0.4750 |
| Segment Count MAE   | 2.1000 | 1.8000 |
| Title F1            | 0.5100 | 0.5400 |
| Pk (↓)              | 0.3200 | 0.2900 |
| WindowDiff (↓)      | 0.3500 | 0.3100 |
| Success rate        | 0.8548 | 0.8790 |

## Delta: 0.9.0 vs 0.8.0 (positive = improvement)
| Metric              | Delta   |
| ---                 | ---:    |
| Breakpoint F1 @100  | +0.0450 |
| Segment Count MAE   | +0.3000 |  ← lower is better, so improvement shown as +
...
```

## Git LFS and storage

Predictions JSON files are tracked via Git LFS under the pattern
`data/results/*/predictions/*.json`. Each new version adds one LFS object per
document evaluated (~106 files × ~5 KB ≈ ~500 KB per version).

The 252 MB sample set (`data/samples/`) is shared and uploaded only once.

GitHub free LFS quota is 1 GB storage / 1 GB bandwidth per month. With ~500 KB
per new version, you can store roughly 1 500 version evaluations before hitting
the storage cap. Bandwidth is consumed each time someone clones the repo (only
the version they need if they use `GIT_LFS_SKIP_SMUDGE=1` and selectively pull).

## Tips

- Keep `data/samples/` and `data/ground_truth.json` in sync with the HuggingFace
  dataset. Re-run `python -m benchmark.prepare_dataset` if you add documents.
- If you want to re-run an existing version (e.g. after fixing the benchmark
  code, not the package), delete `data/results/{version}/` first so predictions
  are not cached.
- Use `--skip-run` to regenerate only the report/tiers from existing predictions:
  ```bash
  python -m benchmark.run_all --skip-extract --skip-images --skip-hf --skip-run
  ```
