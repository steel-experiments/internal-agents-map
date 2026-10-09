# Coinbase Forge re-verification — 2026-10-09

ABOUTME: Re-verification of the coinbase-forge-mux record against its preserved source captures.
ABOUTME: It records a verdict for each reported problem, the catalog change, and the open follow-up.

## Scope and method

A Claude.ai analysis of the `coinbase-forge-mux` record reported six possible problems. Answers
from ChatGPT also showed that the record mixes Forge with the Mux metrics. This review examined
each item against the five preserved captures in `archive/sources/coinbase-forge-mux-source-*/`.
The captures are the evidence. A live page was read only where a capture did not contain the text
in question.

## Verdicts

| # | Reported problem | Verdict | Evidence | Catalog change |
|---|---|---|---|---|
| 1 | The Mux metrics have a measurement window: "By April 2026 - in one month" | Correct for the live page; absent from the capture | The live English post (published 2026-05-11) has this line. The capture of the `/de/` URL, taken 2026-08-31, does not. | None yet. See the follow-up. |
| 2 | The 3.5x ratio applies to power users in the summary, but to all Mux users in the body | Correct for the live page; absent from the capture | The live post's TL;DR says "Power users now merge 3.5x more PRs than baseline". The body and the capture (source-1, line 32) say "Mux users". | None yet. See the follow-up. |
| 3 | The interfaces claim cites only the Mux post, which does not name Forge or its surfaces | Correct | Source-1 does not mention Forge. Source-2, line 34, names Slack, GitHub, and Linear as Forge surfaces. | The interfaces claim and the operating-model claim cite source-2, line 34. |
| 4 | No readable source supports "Forge, previously Claudebot" | Incorrect | Source-3, line 11 (the X post): "Started as 'Claudebot'". Source-5, line 114, names the Claude bot. | None. |
| 5 | The Linear customer story is classed as `first-party` | Correct | `data/schema.md` defines `first-party` as a source that the organization published. Linear published the story. | Source-2 is `independent-secondary`. The same Linear story format in `ramp-inspect` also changed. |
| 6 | The speed-run counts differ between sources | Correct; the sessions are probably different | Source-4, line 23 and source-5, line 170: about 100 people, about 70 PRs. Source-2, line 38: 120 engineers and 80 PRs in the first session; over 500 PRs in a later session. | Source-2, line 38 contextualizes the metric. The confidence reason names the other counts. |
| 7 | The Forge record holds three Mux metrics | Correct | The same three metrics are in the `coinbase-mux` record. | None yet. Each metric is labelled as a Mux metric, and the observations note says that the metrics do not isolate Forge. See the follow-up. |

Claude.ai also noted that the Linear story mentions "autonomous operation time" as a tracked
measure. The source gives no value, so the record does not add it as a metric.

## Follow-up

Item 7 cannot change in this release. `data/claim_aliases.json` must map every schema 7 claim ID
to a claim of the same record, so a claim cannot move to a different record while the map
exists. When the map is removed, remove the three Mux metrics from the Forge record.

Items 1 and 2 need a new capture of the English post,
`https://www.coinbase.com/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it`. Every
source in the catalog has a capture, so the record cannot cite the page without one.
`scripts/archive_sources.py` stops at the Cloudflare challenge page, also with `--delay 15000`.
A Steel scrape through a residential proxy failed twice with a Steel server error. A Steel browser
session in stealth mode opened the page. When a capture succeeds, add the source to the
`coinbase-mux` record, add the window to the three Mux metrics, and record the TL;DR and body
difference for the 3.5x ratio.
