# Segment Tiering

After each benchmark run, `benchmark.segment_tier_report` classifies every document
into one of four tiers based on how accurately the pipeline predicted the number of
sections (segments).

## Tier definitions

**Relative error** = |predicted\_count − ground\_truth\_count| / ground\_truth\_count

| Tier | Condition | Meaning |
|---|---|---|
| **Success** | relative error ≤ 5% | Segment count is essentially correct |
| **Average** | 5% < relative error ≤ 20% | Moderate over- or under-segmentation |
| **Big failure** | relative error > 20% | Severe mis-segmentation |
| **Extraction failure** | pipeline raised an error | No metrics available |

## Why segment count?

Segment-count error is a fast, interpretable diagnostic. A document with the
right number of segments but slightly shifted breakpoints will score well here and
poorly on F1@N — that split tells you where to look (boundary precision vs. section
detection). Conversely, a document with the wrong count always has a low F1@N, so
the tiers help separate structural failures from fine-grained positioning errors.

## Reading the report

`data/segment_tiers.md` is generated automatically. It contains:

1. **Counts** — how many documents fall in each tier.
2. **Success tier table** — sorted by F1@100 descending, then title F1.
3. **Average tier table** — sorted by relative error ascending.
4. **Big failure tier table** — sorted by relative error descending.
5. **Extraction failure list** — documents where the pipeline errored.

## Regenerating

```bash
python -m benchmark.segment_tier_report
# or specify a different results file:
python -m benchmark.segment_tier_report --results path/to/results.json
```
