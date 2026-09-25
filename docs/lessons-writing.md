# Writing lessons

Lessons help builders consider one agent design choice at a time. Keep each article short:
about 200–350 words and a few original sources. Add a diagram or quotation only when it
explains something that the surrounding prose does not. Longer comparisons can remain
in the architecture and adoption documents.

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

Start with a concrete title and observation. Organize the rest around the question the
lesson examines. Report what each source says before adding a catalog interpretation.
Keep the distinction visible in the prose. A lesson can use a comparison, branch, loop,
or sequence when that form explains the mechanism. It does not need a quotation, a
diagram, a caution, and a closing question in the same fixed order.

Check quotes against preserved sources. Preserve qualification, time, and scope.
Do not treat a catalog judgment as independent evidence. An implementation does not
prove effectiveness. A result from one company does not establish a general rule.
State uncertainty next to the claim that it qualifies. Remove a generic caveat when
the lesson already identifies the specific evidence limit. Read the source again when
its evidence or the associated catalog claims change.

## Illustrations

Use the existing Areal type, white background, fine gray rules, and restrained teal
accent. HTML/CSS diagrams keep labels readable and let the layout adapt to small
screens. Show the branch, loop, comparison, or shared state that matters to the lesson.
Omit the diagram when it would only repeat the prose. Mark arrows as decorative when
the text already gives the order.

Choose the form after identifying what a reader must compare or follow. A conditional
retry needs visible exit and retry branches; parallel reviewers need a shared input;
worker recovery needs storage outside the workers. A table can explain differences
between two discovery designs. An article about review cost may need only prose.

Captions identify the illustration as ours and explain any simplification. Do not
invent scores, proportions, or performance improvements. A conceptual quadrant needs
named axes and a clear statement that positions are illustrative.

## Adding a lesson

Add one Markdown file under `src/content/lessons/`. Its front matter declares the title,
description, eyebrow, lede, summary, reading time, reading order, publication date,
`relatedAgentIds`, and the numbered sources. The collection schema in
`src/content.config.ts` stops the build when a field is missing, and the build adds the
lesson to the index, the routes, the sitemap, and the Markdown exports. No route list,
allowlist, or page template needs an edit. Then run `npm run verify`.

Read the lessons together before finishing an editorial pass. Check for repeated
openings, quotations that add no evidence, identical diagrams, and closing questions
that restate the article. Record source checks and editorial decisions separately
from automated validation; tests can check reading and export integrity, not whether
the argument is useful.
