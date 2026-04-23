"""End-to-end benchmark orchestrator.

Usage:
    python -m benchmark.run_all [options]

Options:
    --skip-extract    Skip DB extraction (use cached data/)
    --skip-images     Skip ToC image download
    --skip-hf         Skip HuggingFace dataset push
    --skip-run        Skip pipeline run (use cached predictions/)
    --skip-report     Skip report generation
    --num-samples N   Number of samples to extract (default: all)
    --gemini-api-key  Gemini API key (or set GEMINI_API_KEY env var)
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Run ai-text-outline benchmark pipeline"
    )
    parser.add_argument("--skip-extract", action="store_true",
                        help="Skip DB extraction (use cached data)")
    parser.add_argument("--skip-images", action="store_true",
                        help="Skip ToC image download")
    parser.add_argument("--skip-hf", action="store_true",
                        help="Skip HuggingFace dataset push")
    parser.add_argument("--skip-run", action="store_true",
                        help="Skip pipeline run (use cached predictions)")
    parser.add_argument("--skip-report", action="store_true",
                        help="Skip report generation")
    parser.add_argument("--num-samples", type=int, default=None,
                        help="Number of samples to extract (default: all)")
    parser.add_argument("--gemini-api-key", type=str, default=None,
                        help="Gemini API key")
    args = parser.parse_args()

    if not args.skip_extract:
        print("=" * 60)
        print("Step 1: Extracting benchmark data from database")
        print("=" * 60)
        from benchmark.extract_data import extract_benchmark_data
        extract_benchmark_data(num_samples=args.num_samples)
        print()

    if not args.skip_images:
        print("=" * 60)
        print("Step 2: Downloading ToC images")
        print("=" * 60)
        from benchmark.download_toc_images import main as download_images
        download_images()
        print()

    if not args.skip_hf:
        print("=" * 60)
        print("Step 3: Preparing HuggingFace dataset")
        print("=" * 60)
        from benchmark.prepare_dataset import prepare_hf_dataset
        prepare_hf_dataset(push_to_hub=True)
        print()

    if not args.skip_run:
        print("=" * 60)
        print("Step 4: Running pipeline on benchmark samples")
        print("=" * 60)
        from benchmark.run_pipeline import run_benchmark
        run_benchmark(gemini_api_key=args.gemini_api_key)
        print()

    if not args.skip_report:
        print("=" * 60)
        print("Step 5: Generating report")
        print("=" * 60)
        from benchmark.report import generate_report
        generate_report()
        print()

    print("Done!")


if __name__ == "__main__":
    main()
