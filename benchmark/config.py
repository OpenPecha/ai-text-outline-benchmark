"""Configuration for benchmark pipeline."""

import os
from pathlib import Path
from types import SimpleNamespace

# Paths
BENCHMARK_DIR = Path(__file__).parent
ROOT_DIR = BENCHMARK_DIR.parent
DATA_DIR = ROOT_DIR / "data"

# Shared across all versions (never changes between runs)
SAMPLES_DIR = DATA_DIR / "samples"
GROUND_TRUTH_PATH = DATA_DIR / "ground_truth.json"

# Versioned results root: data/results/{version}/
RESULTS_DIR = DATA_DIR / "results"

# Database (from environment variables)
DB_CONFIG = {
    "host": os.environ.get("BENCHMARK_DB_HOST", ""),
    "user": os.environ.get("BENCHMARK_DB_USER", ""),
    "password": os.environ.get("BENCHMARK_DB_PASSWORD", ""),
    "port": int(os.environ.get("BENCHMARK_DB_PORT", "5432")),
    "database": os.environ.get("BENCHMARK_DB_NAME", "postgres"),
}

# Evaluation settings
TOLERANCE_VALUES = [50, 100, 200, 500]
TITLE_SIMILARITY_THRESHOLD = 0.7
WINDOWED_BIN_SIZE = 100  # characters per bin for Pk/WindowDiff

# Pipeline settings
API_CALL_DELAY = 2.0  # seconds between documents
DEFAULT_NUM_SAMPLES = 10

# HuggingFace
HF_DATASET_REPO = "openpecha/ai-text-outline-benchmark"


def current_version() -> str:
    """Return the installed ai_text_outline version string (e.g. '0.8.0')."""
    try:
        import ai_text_outline
        return ai_text_outline.__version__
    except Exception:
        return "unknown"


def version_paths(version: str) -> SimpleNamespace:
    """Return all output paths for a given package version.

    Usage:
        paths = version_paths("0.9.0")
        paths.predictions_dir   # data/results/0.9.0/predictions/
        paths.results_path      # data/results/0.9.0/results.json
        paths.report_path       # data/results/0.9.0/report.md
        paths.segment_tiers_path # data/results/0.9.0/segment_tiers.md
    """
    vdir = RESULTS_DIR / version
    return SimpleNamespace(
        dir=vdir,
        predictions_dir=vdir / "predictions",
        results_path=vdir / "results.json",
        report_path=vdir / "report.md",
        segment_tiers_path=vdir / "segment_tiers.md",
    )
