"""Configuration for benchmark pipeline."""

import os
from pathlib import Path

# Paths
BENCHMARK_DIR = Path(__file__).parent
ROOT_DIR = BENCHMARK_DIR.parent
DATA_DIR = ROOT_DIR / "data"
SAMPLES_DIR = DATA_DIR / "samples"
PREDICTIONS_DIR = DATA_DIR / "predictions"
GROUND_TRUTH_PATH = DATA_DIR / "ground_truth.json"
RESULTS_PATH = DATA_DIR / "results.json"
REPORT_PATH = DATA_DIR / "report.md"

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
HF_DATASET_REPO = "OpenPecha/ai-text-outline-benchmark"
