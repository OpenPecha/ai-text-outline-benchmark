# Known Failure Modes

This document describes the main categories of errors observed in the v0.8.0
evaluation run over 124 Tibetan documents.

## Over-extraction

Some documents cause the pipeline to predict far more segments than are present
in the ground truth. The two most severe cases are:

- **W2PD19769** — predicted count greatly exceeds ground truth; the text contains
  many short lines that the no-marker path mistakes for section headings.
- **W4PD502** — similar pattern; dense page-number sequences confuse the
  page-match heuristic.

**Mitigation:** Add a post-processing cap on maximum segments relative to text
length, or tune the short-line detection threshold.

## Gemini image errors

18 documents failed the vision-enhanced ToC path with an API error from Gemini
(typically a content-safety refusal on scanned manuscript images or an empty
model response). These fall back to the text-only path, which reduces accuracy
for manuscripts that lack a clear ToC marker.

**Mitigation:** Implement retry logic with exponential back-off; if the vision
path fails after retries, flag the document rather than silently falling back.

## ToC truncation from 5-page cap

The legacy code used a hard cap of 5 IIIF pages for the ToC window. For long
tables of contents (some Tibetan texts have 10–15 page ToCs), the extraction
window closed before reaching all entries, causing a low recall on breakpoints
in the second half of the document.

The `_get_image_bounded_toc_end` function introduced in v0.8.0 dynamically
extends the window based on image content, but only up to the point where the
model reports the ToC has ended. Very long ToCs may still be truncated if the
model mis-identifies the end early.

## Extraction / API failures

A small number of documents (listed in `data/segment_tiers.md` under
"Extraction / API failures") produced no metrics at all. Common causes:

- IIIF image fetch timeout or HTTP 429 (rate limit).
- Gemini context length exceeded for very long documents.
- Unicode decode errors in edge-case OCR output.
