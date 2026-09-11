Source: https://internal-agents.com/#uber-ureview

Uber Background agent

# uReview

An event-driven AI code reviewer for Uber's internal review platform that generates, grades, filters, deduplicates, and posts findings while leaving engineers in control of the reviewed change.

Code review

pull request → filtered AI review findings: Work product review

Operating model, claims & sources

#### Scoped operating models

**pull request → filtered AI review findings** Work product review · Level 3

#### Summary and context

Summary

An event-driven AI code reviewer for Uber's internal review platform that generates, grades, filters, deduplicates, and posts findings while leaving engineers in control of the reviewed change.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Introduction; How It Works

#### Reported metrics

Headline claim

Uber's introduction reports reviews of over 90% of approximately 65,000 weekly diffs, with over 75% usefulness and over 65% addressed comments; a later paragraph says 65,000 diffs per month

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The opening paragraph reports approximately 65,000 weekly diffs, but the cost discussion says 65,000 per month. These conflicting periods remain unresolved; neither is independently verified.

Reported by
:   Uber

Scope
:   Introduction's reported weekly diff coverage, plus comment usefulness/addressed rates; later paragraph's monthly period conflicts and remains unresolved

Denominator
:   Introduction reports approximately 65,000 weekly diffs; cost paragraph says monthly. Usefulness covers rated comments; addressed rate covers posted comments

Method
:   Production coverage, developer ratings, and automatic addressed-comment detection

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 34, 98
- Contradicts [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 120 (65,000 per month, versus weekly in line 34)

Key observation

Introduction reports reviews of over 90% of approximately 65,000 weekly diffs; cost discussion instead says 65,000 diffs per month

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The opening paragraph reports approximately 65,000 weekly diffs, but the cost discussion says 65,000 per month. These conflicting periods remain unresolved; neither is independently verified.

Reported by
:   Uber

Scope
:   Introduction's reported weekly diffs analyzed; monthly period in the cost paragraph conflicts and remains unresolved

Denominator
:   Approximately 65,000 weekly diffs according to the introduction; same volume described as monthly in the cost paragraph

Method
:   Unknown

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 34
- Contradicts [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 120 (65,000 per month, versus weekly in line 34)

Key observation

Over 75% of comments rated useful by engineers who interact with the tool

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Uber

Scope
:   Comments rated useful by engineers who provide feedback

Denominator
:   Comments with engineer interaction

Method
:   Useful / Not Useful rating links

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 76, 98

Key observation

Over 65% of posted comments addressed in the same changeset

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Uber

Scope
:   Posted comments considered addressed in the same changeset

Denominator
:   Posted comments

Method
:   Five reruns on the final commit and semantic-similarity matching

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 82, 98

Key observation

Median review latency of 4 minutes across all six Uber monorepos

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

Reported by
:   Uber

Scope
:   Reviews across all six Uber monorepos

Denominator
:   Unknown

Method
:   Production latency telemetry

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 94

Key observation

Approximately 1,500 developer hours reportedly saved per week, based on an assumed 10-minute second review per processed commit

Metric · Reported · Low confidence

Evidence and qualifications

Confidence reason
:   The source estimates about 1,500 hours using over 10,000 commits and a 10-minute assumption; the rounded figures do not arithmetically reconcile exactly and are not observed time savings.

Reported by
:   Uber

Scope
:   Processed commits excluding configuration files; modeled second-review time savings

Denominator
:   Over 10,000 commits per week

Method
:   Processed commits multiplied by an assumed 10 minutes for a second human review

Observation date
:   2025-08

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Preserved content.md, lines 104

#### Architecture and primitives

Harness

A prompt-chained pipeline separates comment generation, confidence grading, validation, semantic deduplication, and category filtering; three specialized assistants were in operation when published

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) How It Works; Comment Generation; Post-Processing

Model

Periodic benchmark evaluation; Claude 4 Sonnet as generator with o4-mini-high as grader was the highest-F1 reported pairing

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Empirical Model Evaluation

Interfaces

internal-ui, ci

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Comment Delivery and Feedback Collection; Impact and Evaluation

Tool access

Reviews eligible code in Uber's six monorepos across Go, Java, Android, iOS, TypeScript, and Python; richer internal artifacts were not yet connected when published

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Impact and Evaluation; Better at Catching Bugs than Assessing System Design

Knowledge

Surrounding source context plus a shared registry of Uber-specific coding and style rules

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Ingestion and Preprocessing; Comment Generation by Specialized Assistants

Context management

Comments and metadata are streamed through Kafka to Hive for feedback analysis, experiments, and operational dashboards

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Comment Delivery and Feedback Collection

Supporting component

Standard, best-practices, and AppSec reviewers generate findings for different issue classes

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Comment Generation by Specialized Assistants

Supporting component

Confidence grading, semantic deduplication, and historically low-value category suppression reduce noise

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Post-Processing and Quality Filtering

Supporting component

Developer ratings, addressed-comment detection, and a curated benchmark tune prompts, thresholds, and models

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Evaluation and Continuous Improvement

#### Lessons and interpretation

Lesson

Prefer fewer high-confidence findings over high comment volume

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The article states this lesson directly and documents the associated mechanisms.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Precision Is More Valuable than Volume

Lesson

Combine prompts with deterministic filtering, deduplication, evaluation, and feedback instrumentation

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The article states this lesson directly and documents the pipeline.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Guardrails Are Just as Important as Prompts

Lesson

Roll out gradually by team and assistant while tracking precision, recall, usefulness, and false positives

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The article states this lesson directly and describes the rollout telemetry.

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party) Trust Grows with Gradual Rollout

#### Operating model evidence

Operating model assessment

Level 3 for pull request → filtered AI review findings; human attention boundary: work-product-review.

Inference · Catalog judgment · High confidence

Evidence and qualifications

Confidence reason
:   The source describes AI-generated review findings while engineers remain in control of the change.

Observation date
:   2025-08-12

- Supports [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md) (first-party)

#### Sources

1. [uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://www.uber.com/us/en/blog/ureview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/uber-ureview-source-1/content.md)  <https://www.uber.com/us/en/blog/ureview/> engineering-blog · first-party · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#uber-ureview)
