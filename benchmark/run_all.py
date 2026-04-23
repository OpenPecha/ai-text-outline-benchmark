"""End-to-end benchmark orchestrator.

Usage:
    python -m benchmark.run_all [options]

Options:
    --package-version V   Version to evaluate (default: auto-detect from installed package)
    --skip-extract        Skip DB extraction (use cached data/)
    --skip-images         Skip ToC image download
    --skip-hf             Skip HuggingFace dataset push
    --skip-run            Skip pipeline run (use cached predictions/)
    --skip-report         Skip report generation
    --skip-tiers          Skip segment-tier report
    --num-samples N       Number of samples to extract (default: all)
    --gemini-api-key KEY  Gemini API key (or set GEMINI_API_KEY env var)

Results are written to data/results/<version>/ so runs for different versions
never overwrite each other. Use benchmark.compare to diff two versions.
"""

import argparse


def main():
    from benchmark.config import current_version, version_paths

    parser = argparse.ArgumentParser(
        description="Run ai-text-outline benchmark pipeline"
    )
    parser.add_argument(
        "--package-version", type=str, default=None,
        help="Package version to evaluate (default: auto-detect from installed package)",
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
    parser.add_argument("--skip-tiers", action="store_true",
                        help="Skip segment-tier report")
    parser.add_argument("--num-samples", type=int, default=None,
                        help="Number of samples to extract (default: all)")
    parser.add_argument("--gemini-api-key", type=str, default=None,
                        help="Gemini API key")
    args = parser.parse_args()

    pkg_ver = args.package_version or current_version()
    paths = version_paths(pkg_ver)
    print(f"Package version: {pkg_ver}")
    print(f"Results dir:     {paths.dir}")
    print()

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
        run_benchmark(
            gemini_api_key=args.gemini_api_key,
            package_version=pkg_ver,
        )
        print()

    if not args.skip_report:
        print("=" * 60)
        print("Step 5: Generating report")
        print("=" * 60)
        from benchmark.report import generate_report
        generate_report(package_version=pkg_ver)
        print()

    if not args.skip_tiers:
        print("=" * 60)
        print("Step 6: Generating segment-tier report")
        print("=" * 60)
        from benchmark.segment_tier_report import build_tiers, render_markdown
        tiers = build_tiers(paths.results_path)
        text = render_markdown(tiers)
        paths.segment_tiers_path.parent.mkdir(parents=True, exist_ok=True)
        paths.segment_tiers_path.write_text(text, encoding="utf-8")
        print(f"Wrote {paths.segment_tiers_path}")
        print()

    print("Done!")
    print(f"Results at: {paths.dir}")


if __name__ == "__main__":
    main()
