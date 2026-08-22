---
name: add-agent-from-url
description: Research a URL and decide whether it belongs in the Internal Agents Map catalog, then add it when it passes the inclusion rubric. Use this skill whenever the user shares a link (engineering blog, talk, podcast, paper, HN thread, newsletter) about a company's internal AI agent, harness, platform, or dogfooding story and asks to add it, check it, evaluate it, or "see if this qualifies" — even if they do not name the catalog or the rubric.
---

# Add an approach from a URL

You are the intake pipeline for the Internal Agents Map catalog. A URL arrives. You research it,
score it against the inclusion rubric, and then act on the score: add a record, log a border case,
or record an exclusion. The catalog's value is that every entry is a real internal build with
linked evidence, so the discipline below is the product. A wrongly added promotional story costs
more than a missed entry, because the backlog keeps missed entries findable.

## Workflow overview

1. Fetch the URL and extract the claims.
2. Check the catalog for an existing record.
3. Score the source against the rubric.
4. Branch on the score: add, border case, or exclude.
5. Verify the repo state and report.

## Step 1: Fetch and extract

Fetch the URL. If the fetch fails, say so and stop; do not score from memory.

Extract these facts from the page itself, not from your prior knowledge of the company:

- The organization that runs the system.
- The system's name (or the absence of one).
- What the system does, described as a workflow from input to output.
- Who built it: the org itself, a vendor tool adopted as-is, or something in between.
- Whether the system is internal, a shipping product, or both.
- Architecture details: harness, sandbox, model, tools, interfaces, knowledge, credentials.
- Metrics with their dates, scopes, and denominators.
- The publication date and the author's relationship to the system.

If the URL is a secondary source (newsletter, news report) that references a primary source,
fetch the primary source too and score that. Record both as sources when you write a record.
The catalog prefers the primary source for claims, with the secondary as context.

If the URL is a Hacker News thread or forum discussion, treat the thread and each material
comment as separate candidate sources with the `community` provenance class.

## Step 2: Check for an existing record

Run `ls data/agents/` and grep the file contents for the company name and the system name,
including likely aliases. The catalog stores aliases in an `aliases` field, so search file
contents, not just file names.

- If the system is already cataloged, do not add a second record. Instead, offer to add the new
  URL as a source to the existing record, with evidence links for any claims it supports.
- If the company is cataloged but this system is new, proceed. One company can have several
  records (see Atlassian and Plaid).

## Step 3: Score against the rubric

Score each dimension 0, 1, or 2. Base every score on what the fetched sources document, not on
what the company is known for. The rubric rewards demonstrated builds and punishes promotion.

| # | Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- | --- |
| 1 | Identified build | No named system; the org "uses AI" | Named system, thin description | Named system with its workflow described |
| 2 | Internal ownership | Vendor tool adopted as-is (a Cursor or Claude Code usage story) | Adaptation claimed but not demonstrated | Distinct internal build, or material adaptation shown (wrapper, internal MCP servers, gateway, own framework) |
| 3 | Source provenance | Unattributed, rumor, anonymous | Community thread or independent secondary only | First-party engineering source, repository, paper, or direct-participant talk or podcast |
| 4 | Operational specificity | Announcement or vision, no usage evidence | Some usage signals | Concrete architecture, scale, or workflow detail with dates |
| 5 | Product independence | The story is the org using its own shipping consumer product internally | Straddles: an internal adaptation layer sits on a shipping product | Internal-only system, or a distinct build that predates or informed a product |

### Hard gates

Fail the intake outright, whatever the total, when any of these hold:

- No named organization.
- The system is not agent-shaped: pure model-serving or inference infrastructure (see the
  Netflix exclusion in `docs/coverage-backlog.md`) is out of scope.
- Dimension 3 scores 0: rumor or unattributed claim.
- Dimension 5 scores 0: the company's own shipping consumer product used internally with no
  distinct internal build. This is promotional dogfooding. The v0 and GitLab Duo exclusions in
  the backlog are the precedents. The rule exists because such stories market the product; they
  do not document an internal build.
- The system is already cataloged (Step 2).

### Decision

- **Add** when dimensions 1 and 2 both score 2, dimension 5 scores 2, and the total is 8 or more.
- **Border case** when the hard gates pass but the add conditions do not. Typical causes: a
  shipping product with a real internal adaptation layer (dimension 5 at 1), or secondary-only
  provenance with thin detail. Log it in the backlog with the specific question a human must
  answer.
- **Exclude** when a hard gate fails or the total is 4 or less. Log it in the backlog under
  "Refuted or excluded" with the reason and the source.

Report the scores and the branch you took. Show your work in one short table; the user should be
able to audit the call without rereading the source.

## Step 4a: Add path — write the record

1. Copy `templates/agent.yaml` to `data/agents/<id>.yaml`. The kebab-case id must match the file
   name.
2. Fill the record from the extracted facts. Follow the schema rules below; they exist because
   each one closed a real defect.
3. Run the bundled counts script:

   ```bash
   python3 .claude/skills/add-agent-from-url/scripts/update_pattern_counts.py
   ```

   It rewrites the approach-type table in `docs/patterns.md` and prints the other distribution
   counts. Update the prose counts in `docs/patterns.md` (total approaches, autonomy tally,
   state tally, Slack count, execution-environment count) to match the printed values. A test
   enforces the table; stale prose misleads readers.
4. Run the full verification block:

   ```bash
   python3 scripts/build.py
   python3 scripts/build.py --check
   python3 -m unittest discover -s tests
   python3 scripts/check_links.py --local
   git diff --check
   ```

5. If anything fails, fix the record or the counts. Do not weaken a check to pass it.
6. Commit everything in one commit (YAML, regenerated README, landscape, agents.json, patterns.md,
   backlog edits) and push to main. The user chose full automation for the pass path. Follow the
   repo commit style: imperative subject line within 50 characters, body wrapped at 72
   characters, and the Co-Authored-By trailer.
7. If verification cannot pass after honest fixes, stop, leave the working tree clean
   (`git restore` the generated files, keep the YAML), and report. A blocked add is a border
   case; log it rather than forcing it.

### Schema rules that catch contributors

- `operating_models` is required and must be a non-empty list of items with exactly `scope` and
  `attention_boundary`. Each item needs an evidence link and claim metadata with
  `kind: inference`, `provenance: catalog-judgment`, `confidence`, `confidence_reason`, and
  `valid_at`. The level is derived by the build; never author it as a company fact.
- Boundary values: `continuous-steering`, `work-product-review`, `outcome-review`,
  `exception-only`, `unknown`. Derive the boundary from the documented workflow, never from the
  `autonomy` field. When the system spans several workflows, or the source is a tool-access
  layer with no single human-attention point, use `unknown`. Do not average.
- A colon inside an unquoted YAML scalar breaks parsing. Quote every `scope` string.
- Every entry in `sources` must be linked from at least one claim in `evidence`, or the build
  fails with "not linked to a claim". Conversely, every evidence link must reference a source id
  that exists in the record.
- `first_public_evidence` must point at a source with the `evidence` role.
- Use `unknown` for any field the sources do not document. Do not invent architecture fields.
  Missing evidence is recorded as `unknown`, never as absence of a feature.
- Mark company metrics as self-reported. Confidence `medium` for first-party self-reported
  figures; `low` when the figure reaches you through a third party (the Airbnb 64% precedent).
- Record `locator` values when the source has stable anchors (section, timestamp, comment id).

## Step 4b: Border-case and exclude paths — log the backlog

Edit `docs/coverage-backlog.md`. Do not create catalog records on these paths.

- Border case: add an entry under the matching tier with status "Border case", the scores, the
  open question a human must resolve, and the source list. Mirror the Snowflake Cortex and
  Datadog Bits entries for tone.
- Exclude: add a bullet under "Refuted or excluded" naming the system, the failing gate, and the
  reason, so nobody re-researches it. One or two sentences is enough.
- Keep the editorial rule section and the audit trail intact; you are appending, not rewriting.

Commit and push the backlog edit with a message that names what was excluded or parked and why.

## Step 5: Report

Close with a short report: the scores, the branch, the record id or backlog change, the
verification results, and the commit hash. If you logged a border case, restate the open
question so the user can answer it later.

## What this skill does not do

- It does not spawn verification subagents. The single-pass rubric is the agreed depth. When a
  caller wants adversarial verification for a high-stakes entry, they can run the three-vote
  pass separately.
- It does not edit the hand-written analysis pages beyond the counts in `docs/patterns.md`.
- It does not push when verification fails.
