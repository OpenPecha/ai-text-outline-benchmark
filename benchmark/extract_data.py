"""Extract benchmark samples from the outliner database."""

from __future__ import annotations

import json
from pathlib import Path
import psycopg2
from benchmark.config import DB_CONFIG, SAMPLES_DIR, GROUND_TRUTH_PATH, DEFAULT_NUM_SAMPLES


DOCUMENT_SELECTION_SQL = """
SELECT
    d.id,
    d.filename,
    d.content,
    LENGTH(d.content) AS content_length,
    COUNT(s.id) AS text_segment_count
FROM outliner_documents d
JOIN outliner_segments s
    ON s.document_id = d.id
    AND s.label = 'TEXT'
    AND s.is_annotated = true
WHERE d.status = 'approved'
GROUP BY d.id, d.filename, d.content
HAVING COUNT(s.id) >= 5
ORDER BY COUNT(s.id) DESC
LIMIT %s;
"""

SEGMENT_QUERY_SQL = """
SELECT segment_index, span_start, span_end, title
FROM outliner_segments
WHERE document_id = %s
    AND label = 'TEXT'
    AND is_annotated = true
ORDER BY span_start ASC;
"""


def extract_benchmark_data(
    num_samples: int = DEFAULT_NUM_SAMPLES,
    samples_dir: Path | None = None,
    ground_truth_path: Path | None = None,
):
    """Extract benchmark documents and ground truth from the database.

    Args:
        num_samples: Maximum number of documents to extract.
        samples_dir: Directory to save sample text files. Defaults to SAMPLES_DIR.
        ground_truth_path: Path for ground truth JSON. Defaults to GROUND_TRUTH_PATH.
    """
    samples_dir = samples_dir or SAMPLES_DIR
    ground_truth_path = ground_truth_path or GROUND_TRUTH_PATH

    for key in ("host", "user", "password"):
        if not DB_CONFIG[key]:
            raise ValueError(
                f"Missing BENCHMARK_DB_{key.upper()} environment variable. "
                "See .env.example for required variables."
            )

    samples_dir.mkdir(parents=True, exist_ok=True)

    conn = psycopg2.connect(**DB_CONFIG)
    try:
        cur = conn.cursor()

        # Select benchmark documents
        cur.execute(DOCUMENT_SELECTION_SQL, (num_samples,))
        documents = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]

        print(f"Selected {len(documents)} benchmark documents")

        ground_truth = {}

        for row in documents:
            doc = dict(zip(col_names, row))
            doc_id = doc["id"]
            content = doc["content"]
            filename = doc["filename"]
            content_length = doc["content_length"]

            # Save document text
            text_path = samples_dir / f"{doc_id}.txt"
            text_path.write_text(content, encoding="utf-8")

            # Get ground truth segments
            cur.execute(SEGMENT_QUERY_SQL, (doc_id,))
            segments = cur.fetchall()
            seg_cols = [desc[0] for desc in cur.description]

            seg_list = []
            breakpoints = []
            titles = []
            for seg_row in segments:
                seg = dict(zip(seg_cols, seg_row))
                seg_list.append(seg)
                breakpoints.append(seg["span_start"])
                titles.append(seg["title"] or "")

            ground_truth[doc_id] = {
                "filename": filename,
                "content_length": content_length,
                "breakpoints": breakpoints,
                "titles": titles,
                "segments": seg_list,
            }

            print(
                f"  {filename}: {content_length:,} chars, "
                f"{len(segments)} TEXT segments"
            )

        # Save ground truth
        ground_truth_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ground_truth_path, "w", encoding="utf-8") as f:
            json.dump(ground_truth, f, ensure_ascii=False, indent=2)

        print(f"\nSaved {len(ground_truth)} samples to {samples_dir}")
        print(f"Ground truth saved to {ground_truth_path}")

    finally:
        conn.close()


if __name__ == "__main__":
    extract_benchmark_data()
