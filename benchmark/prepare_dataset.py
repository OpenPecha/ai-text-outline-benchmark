"""Prepare and push HuggingFace dataset from extracted benchmark data."""

import json
import os
from datasets import Dataset, Features, Value, Sequence
from benchmark.config import SAMPLES_DIR, GROUND_TRUTH_PATH, HF_DATASET_REPO


def prepare_hf_dataset(push_to_hub: bool = True):
    """Build HuggingFace dataset from extracted samples and ground truth."""
    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    rows = []
    for doc_id, gt in ground_truth.items():
        text_path = SAMPLES_DIR / f"{doc_id}.txt"
        content = text_path.read_text(encoding="utf-8")

        rows.append({
            "id": doc_id,
            "filename": gt["filename"],
            "content": content,
            "content_length": gt["content_length"],
            "num_segments": len(gt["breakpoints"]),
            "breakpoints": gt["breakpoints"],
            "titles": gt["titles"],
        })

    features = Features({
        "id": Value("string"),
        "filename": Value("string"),
        "content": Value("string"),
        "content_length": Value("int64"),
        "num_segments": Value("int32"),
        "breakpoints": Sequence(Value("int64")),
        "titles": Sequence(Value("string")),
    })

    dataset = Dataset.from_list(rows, features=features)
    print(f"Created dataset with {len(dataset)} rows")
    print(dataset)

    if push_to_hub:
        token = os.environ.get("HF_TOKEN")
        if not token:
            print("Warning: HF_TOKEN not set. Saving locally instead.")
            local_path = GROUND_TRUTH_PATH.parent / "hf_dataset"
            dataset.save_to_disk(str(local_path))
            print(f"Saved locally to {local_path}")
            return dataset

        dataset.push_to_hub(HF_DATASET_REPO, token=token)
        print(f"Pushed to https://huggingface.co/datasets/{HF_DATASET_REPO}")

    return dataset


if __name__ == "__main__":
    prepare_hf_dataset()
