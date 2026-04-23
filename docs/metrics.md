# Evaluation Metrics

The benchmark uses five complementary metrics to measure how well the
`ai-text-outline` pipeline predicts section boundaries in Tibetan texts.

## Breakpoint F1@N

For each tolerance value N (50, 100, 200, 500 characters):

- A predicted breakpoint is a **true positive** if it falls within N characters
  of any ground-truth breakpoint (closest match wins; each GT point is claimed once).
- **Precision** = TP / predicted count
- **Recall** = TP / ground-truth count
- **F1** = harmonic mean of precision and recall

F1@100 is the primary headline metric. A tolerance of 100 characters corresponds
roughly to two to three lines of Tibetan text.

## Segment Count MAE

Mean absolute error between predicted and ground-truth segment counts across
all documents. Lower is better. This metric is scale-independent and easy to
interpret: an MAE of 2 means the pipeline is off by two sections on average.

## Title F1

Fuzzy string similarity (token-level Jaccard) between the set of predicted titles
and ground-truth titles. Titles are matched greedily by highest similarity; each
ground-truth title is claimed at most once.

- **Precision** = sum of best-match similarities / predicted count
- **Recall** = sum of best-match similarities / ground-truth count
- **F1** = harmonic mean

Threshold: pairs with similarity below `TITLE_SIMILARITY_THRESHOLD = 0.7` are
not counted as matches.

## Pk

The standard Beeferman et al. (1999) segmentation penalty. A sliding window of
size k = max(1, total_chars / (2 × num_segments)) is moved across the text.
For each window position, Pk checks whether the window start and end fall in the
same segment under prediction and ground truth. Pk counts the fraction of windows
where prediction and ground truth disagree.

Lower is better; Pk = 0 is perfect; random baseline ≈ 0.5.

## WindowDiff

Pevzner & Hearst (2002) refinement of Pk. Instead of a binary agreement check,
WindowDiff penalises the absolute difference in the number of segment boundaries
inside the sliding window. This makes it more sensitive to near-miss errors and
off-by-one boundary placements than Pk.

Lower is better; WindowDiff = 0 is perfect.
