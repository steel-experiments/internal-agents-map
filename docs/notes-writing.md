# Writing notes

Notes help builders consider one agent design choice at a time. Keep each article short:
about 200–350 words, one useful diagram, and a few original sources. Longer comparisons
can remain in the architecture and adoption documents.

## Language

Use [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf)
as the language reference. Apply its descriptive-writing rules: short sentences, one
topic per paragraph, and information in a logical sequence. Use no more than 25 words
per descriptive sentence or six sentences per paragraph. Use active constructions,
consistent terms, and the approved dictionary meanings. Avoid contractions in authored
prose. Explain abbreviations on first use.

Agent, model, prompt, context, tool, code review, pull request, branch, continuous
integration (CI), run, retry, timeout, log, and judge agent are subject-specific terms.
Keep product and company names intact. Introduce further technical terms only when
needed, and explain their meaning. Short sentences alone do not establish full STE
conformance; vocabulary and grammar also need review.

Do not rewrite direct quotations to make them follow STE. Keep them short and exact,
with a nearby attribution and a link to the original source. Treat quotation text as
source language, separate from the authored prose.

## Evidence and interpretation

Use this structure:

1. A concrete title and a one-sentence observation.
2. What the team reports, with a quote and source references.
3. One original diagram that explains the process or comparison.
4. Our observation, its limits, and one question for the reader.
5. Original source links and related catalog entries.

Check quotes against preserved sources. Preserve qualification, time, and scope.
Do not treat a catalog judgment as independent evidence. An implementation does not
prove effectiveness. A result from one company does not establish a general rule.
Read the source again when its evidence or the associated catalog claims change.

## Illustrations

Use the existing Geist type, white background, fine gray rules, and restrained teal
accent. HTML/CSS diagrams keep labels readable and let the layout adapt to small
screens. Mark arrows as decorative when the text already gives the order.

Captions identify the illustration as ours and explain any simplification. Do not
invent scores, proportions, or performance improvements. A conceptual quadrant needs
named axes and a clear statement that positions are illustrative.

## Adding a note

Add its template under `templates/notes/`, link it from `templates/notes.html`, and add
the output path to `rendered_outputs` in `scripts/build.py` and the explicit allowlist
in `scripts/check_site.py`. Then rebuild and run the documented site checks. Commit
the authored templates and generated output together.
