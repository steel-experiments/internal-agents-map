# Jev public-evidence smoke experiment

Run on 2026-09-22 against public catalog commit `9d2be29`, pinned to `jev-1.13.0`.
The maintainer authorized up to $1. No catalog data was changed.

## Results

**140 successful HTTP requests; 126,820 reported input tokens; estimated API charge $0.00532644** at the documented $0.042/million-input-token price. This is usage multiplied by the published rate, not an invoice reconciliation. Output tokens are free under that rate. No failed requests or retries occurred. The conservative request reservations totaled $0.38535168, below the $1 cap.

The initial run covered 14 cases, each with five questions, in four variants:

- `batch`: five questions in one request.
- `singles`: the same five questions sent separately.
- `reverse`: question order and relation-option order both reversed; this is a combined stress condition, not an isolated causal test.
- `paraphrase`: relation-question wording changed; other question text unchanged.

Two additional identical batch repetitions per case tested ordinary variability. They reuse the same cases and are not independent quality observations.

| Initial-run strategy | Requests | Input tokens | Estimated charge | Summed request time | Per-request p50 / descriptive p95 |
| --- | ---: | ---: | ---: | ---: | --- |
| Five questions batched | 14 | 14,964 | $0.000628488 | 4.033 s | 284 / 374 ms |
| One question per request | 70 | 52,140 | $0.002189880 | 21.762 s | 296 / 385 ms |
| Reversed batch | 14 | 14,964 | $0.000628488 | 4.661 s | 299 / 681 ms |
| Paraphrased batch | 14 | 14,824 | $0.000622608 | 4.435 s | 289 / 441 ms |

Batching cost 3.48× less and had 5.40× lower summed request time than the separate-call strategy. Single requests were interleaved in a seeded random order, not sent concurrently. Summing their network durations estimates the sequential work required; it is not a concurrent-single comparison. The entire initial run took 46.43 seconds including the 100 ms client pacing between calls, preparation and local output. Fixture preparation took approximately 3 ms.

Client timers include serialization, HTTP network and server response processing, but not retrieval from live sources or human review. Calls used one persistent HTTPS connection, one in-flight request, a 20-second timeout, and no retry. The first call includes connection setup. The 14 base batches are too few for a reliable tail estimate: the nearest-rank p95 is the maximum. The follow-up's 28 batches had p50 285 ms, descriptive p95 437 ms and maximum 684 ms. No saturated-load throughput or p99 claim is supported.

## Quality observations

The 14 fixtures comprise supported and deliberately altered claims from six organizations, plus one adjacent-product distractor and one source-text prompt injection. Source paths, line ranges and full capture hashes are frozen in [cases.json](cases.json). Claims are judged relative to supplied excerpts, not world truth or current product behavior.

Expected labels were proposed by a coding agent, checked against the passages by the parent agent, and fixed before API calls. They are **not independently adjudicated gold**. The Shopify counterclaim's distinction between contradiction and insufficient support is debatable; report the disagreement rather than declare the model objectively wrong.

- Base batches: **12/14** three-way labels matched the provisional labels.
- Initial variants: **49/56** relation labels matched; all **56/56** preserved the provisional supported-versus-needs-review distinction.
- Follow-up repeats: **25/28** exact labels matched; **28/28** preserved that coarse distinction.
- The fine-grained disagreements were insufficient evidence classified as contradiction. Shopify's unsupported filesystem guarantee was consistently called contradicted at 0.93–0.96 probability. Plaid's required-review counterclaim was close to a tie and switched between insufficient and contradicted.
- Exact repetition also flipped the Plaid label once. Thus the initial variant differences cannot be attributed solely to batching or order.
- The Coinbase positive had only 0.55 support probability in the base batch. The Shopify positive moved from 0.83 to 0.72 after paraphrasing. Even among these selected positives, a 0.9 acceptance threshold would leave substantial review work.
- Across base versus single calls, the largest corresponding probability difference was 0.12. Identical-repeat comparisons also produced differences up to 0.11 on a companion predicate. One sample per configuration does not prove a batching effect.
- The one synthetic injection did not induce a supported verdict. This is one easy test, not a security guarantee.

The companion Noul questions were not independently labeled. They expose potential review signals, but this experiment does not establish their precision or recall. The runner reports an exploratory multiclass Brier score; correlated variants and uncertain labels prevent treating it as a trustworthy calibration estimate.

**Interpretation:** price and low-concurrency response time justify a larger advisory trial. The sample does not establish production accuracy, safe thresholds, reviewer savings, retrieval quality, or autonomous-publication fitness.

## Reproduce safely

Python standard library only. No installation is required. Run from the repository root:

```sh
python3 plans/016-jev-eval/run.py
python3 plans/016-jev-eval/run.py --summarize plans/016-jev-eval/results.jsonl
python3 plans/016-jev-eval/run.py --summarize plans/016-jev-eval/repeats.jsonl
```

The dry-run reads and hashes public capture files, prepares 112 requests and makes **zero API calls**. It should report 14 cases and 280 questions. Labels, review explanations, expected evidence relations and fixture metadata are not sent to Jev. Only claim text, numbered passage text and questions are sent.

To make a new live run, provide a fresh authorized budget and an unused output path. `TYPESAFE_API_KEY` must already be set in the environment. Do not put its value in a command, output, or file:

```sh
python3 plans/016-jev-eval/run.py --live --budget-usd 0.31 --max-requests 112 \
  --output plans/016-jev-eval/new-results.jsonl
```

The script reserves the price of a full 65,536-token request for every attempted request, including any failed or timed-out attempt. That is intentionally much larger than observed usage. It rejects a run whose reservation exceeds the supplied cap, never overwrites an output, and stops on the first error. No automatic retry can silently increase spend. Recheck published model pricing/limits before future runs; the hard-coded reservation is tied to the September 22 terms.

These commands reproduce the smoke test, not the independent held-out evaluation. The [investigation](../016-jev-investigation.md) defines the 120-item next experiment, leakage controls, stronger baselines, reviewer-time measurement and go/no-go gates.

## Files

- [run.py](run.py): request construction, dry-run, bounded live execution and summary.
- [cases.json](cases.json): 14 frozen exploratory fixtures; altered claims are explicitly marked.
- [results.jsonl](results.jsonl): 112 original request results with usage, timing and request hashes.
- [repeats.jsonl](repeats.jsonl): 28 additional identical-batch results.

No raw credentials are recorded. The requests are reproducible from the runner, fixture file and hash-checked captures. There are no production hooks, model-generated catalog changes, or changes to normal verification behavior.
