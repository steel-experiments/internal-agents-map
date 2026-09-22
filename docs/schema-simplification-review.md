# Schema simplification review

Reviewed: 2026-09-22. Advisory note; no schema or implementation changes made.

The authoring format has accumulated too much bookkeeping. The evidence model is useful, but editing one fact often requires coordinating several parallel structures.

This review covered `data/schema.md`, a structural scan of all 66 YAML records and `data/agents.json`, and the relevant generation and rendering code. It did not re-verify the underlying source claims.

## Scale

- 66 YAML records, totaling 18,536 lines; median 280 lines per record.
- `page_content` occupies 4,923 lines, or 27% of the YAML.
- Evidence and claim metadata occupy another 42%.
- The generated JSON is about 1.5 MB, containing 66 approaches, 1,172 claims, 138 source records, and 43 companies.

Line count alone is not a problem, but there is substantial repetition.

## Priorities

| Priority | Simplification | Why | Effort / migration risk |
| --- | --- | --- | --- |
| 1 | Make `page_content` mostly generated, with explicit review exceptions | Repeated mappings such as `harness → architecture.harness` add little information | Medium / medium |
| 2 | Store each observation once; select one as the headline | There are 33 duplicate-observation aliases maintaining multiple representations | Medium / medium |
| 3 | Put evidence and metadata beside each claim, using stable IDs | Positional references spread one item across several distant blocks | Large / high |
| 4 | Make `canonical_url` an optional override | All 138 source records currently repeat `url` verbatim | Small / low |

These are high-confidence structural observations. The exact replacement format needs a migration design.

## Page-review metadata

`page_content` is the clearest excess. In [Datako's record](../data/agents/airbnb-datako.yaml), its 70 lines mostly classify and point back to a handful of facts already above.

Keep the distinction between *unreported*, *not reviewed*, and *not applicable*. Require authors to record the review and meaningful exceptions, while generating obvious field mappings. Missing content alone must not imply that sources were reviewed and found silent.

There is a legitimate historical reason: [the pilot plan](../plans/009-agent-page-content-pilot.md) deliberately added this layer to preserve existing claim identities. It was a reasonable migration bridge. Now all 66 records have it, while the schema still calls it an optional pilot.

## Claim identity and authoring

Positional claim references are the deeper design problem. A metric's text lives in `key_metrics.0`, its citations in `evidence`, its qualifications in `claim_metadata`, and its presentation classification in `page_content`.

The [generator](../scripts/build.py) also derives public claim IDs from those positions. Reordering a list can therefore change which statement an existing ID identifies.

Give list items stable IDs and colocate their evidence and qualifications. Preserve old public IDs through an explicit compatibility mapping. This is the largest migration and should be designed before broad restructuring.

## Duplicate observations

[Airchat](../data/agents/airbnb-airchat.yaml) contains an identical headline and key metric, followed by metadata explaining that they are identical. One observation plus a headline reference would remove the need to author that reconciliation.

The catalog has 33 observation aliases. Preserve distinct periods, scopes, and qualifications when consolidating; similar numbers do not necessarily represent the same observation. Existing public claim references also need compatibility handling.

## Generated JSON

`agents.json` is less concerning than the authoring format. It is generated, and the separate approaches, claims, sources, and companies collections support traceability.

The inconvenience is that consumers must join claims just to retrieve a summary. Simplify YAML authoring first and preserve the export contract during that work.

## Overlapping classifications

Reconsider requiring both entry-wide `autonomy` and scoped `operating_models`. They overlap, but are not interchangeable; do not derive one blindly from the other. Scoped assessments are the stronger foundation.

## Complexity worth keeping

Keep source provenance, exact citations, metric qualifications, preserved captures, and the distinction between facts and catalog judgments. Those earn their complexity.

Start with `page_content` and duplicate metrics, then tackle stable claim IDs before broader restructuring.

## Validation

Both checks passed at review time:

```sh
.venv/bin/python scripts/build.py --check
.venv/bin/python scripts/content_coverage.py --check
```

Generated files were current, and coverage was valid for all 66 entries. This was a structural review, not a full application audit or a source-fact verification.
