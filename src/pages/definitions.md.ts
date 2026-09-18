// ABOUTME: Serves the Definitions guide as Markdown, including the chart placements.
// ABOUTME: The placements come from the catalog, so the export follows the evidence.
import type { APIRoute } from 'astro';
import { loadCatalog } from '../lib/catalog';
import { placements, placementsByCell, type PlacementView } from '../lib/definitions';
import {
  ASSISTANT_REFERENCES,
  APPROACH_TYPE_DEFINITIONS,
  WORK_DOMAIN_DESCRIPTION,
  WORK_MODES_DESCRIPTION,
  DEFINITIONS_CHART,
  DEFINITIONS_HEADING,
  DEFINITIONS_INTRO,
  DEFINITIONS_JUMP_LINKS,
  DEFINITIONS_LEDE,
  DEFINITIONS_QUESTIONS,
  DEFINITIONS_SCOPE,
  SUPERVISION_DEFINITIONS,
  DEFINITIONS_TERMS,
  DEFINITIONS_WORKFLOW,
  INVOCATION_DEFINITIONS,
  READY_REFERENCES,
  REFERENCE_PLACEMENTS,
  inlineMarkdown,
  type ChartCell,
  type ConceptFigure,
  type LabelledValue,
  type ReferencePlacement,
  type TextBlock,
} from '../lib/guide-content';
import { canonicalUrl, guidePath } from '../lib/routes';

function blocks(items: readonly TextBlock[]): string[] {
  return items.map((item) => inlineMarkdown(item));
}

function marker(placement: PlacementView): string {
  return `- [**${placement.company}** ${placement.agentName}](${canonicalUrl(placement.path)} "${placement.reason}")`;
}

function referenceMarker(reference: ReferencePlacement): string {
  return `- **${reference.name}** ${reference.category}`;
}

function cell(heading: ChartCell, lines: readonly string[]): string[] {
  return [
    `### ${heading.scope} ${heading.title}`,
    lines.length > 0 ? lines.join('\n') : `- ${DEFINITIONS_CHART.emptyCell}`,
  ];
}

function step(item: LabelledValue): string {
  return `${item.label} **${item.value}**`;
}

function figure(item: ConceptFigure): string[] {
  return [item.label, `**${item.term}** ${item.caption}`];
}

function placementNote(placement: PlacementView): string {
  const links = placement.evidence
    .map((item) => `[${item.label}](${canonicalUrl(item.href)})`)
    .join(' · ');
  return [
    `- **${placement.company} · ${placement.agentName}**`,
    `  ${placement.reason}`,
    `  ${links}`,
  ].join('\n\n');
}

function referenceNote(reference: ReferencePlacement): string {
  const links = reference.links.map((link) => `[${link.label} ↗](${link.url})`).join(' · ');
  return [
    `- **Reference · ${reference.name}**`,
    `  ${reference.reason}`,
    `  ${links}`,
  ].join('\n\n');
}

function document(): string {
  const catalog = loadCatalog();
  const cells = placementsByCell(catalog);
  const placed = placements(catalog);
  const page = canonicalUrl(guidePath('definitions'));
  const scope = DEFINITIONS_SCOPE;
  const workflow = DEFINITIONS_WORKFLOW;
  const chart = DEFINITIONS_CHART;
  const terms = DEFINITIONS_TERMS;
  const questions = DEFINITIONS_QUESTIONS;
  const supervision = SUPERVISION_DEFINITIONS;
  return [
    `Source: ${page}`,
    `# ${DEFINITIONS_HEADING}`,
    DEFINITIONS_LEDE,
    ...blocks(DEFINITIONS_INTRO),
    'The agent comparisons below exclude shared infrastructure. Explore [platforms and components](https://internal-agents.com/infrastructure) separately.',
    '',
    DEFINITIONS_JUMP_LINKS.map((link) => `[${link.label}](${page}#${link.fragment})`).join(' '),
    scope.eyebrow,
    `## ${scope.heading}`,
    scope.definitionLabel,
    inlineMarkdown(scope.definition),
    scope.diagramLabel,
    ...blocks(scope.body),
    `### ${scope.agentHeading}`,
    ...blocks(scope.agentBody),
    workflow.eyebrow,
    `## ${workflow.heading}`,
    inlineMarkdown(workflow.intro),
    ...workflow.steps.map(step),
    inlineMarkdown(workflow.caption),
    inlineMarkdown(workflow.closing),
    inlineMarkdown([workflow.catalogLink]),
    chart.eyebrow,
    `## ${chart.heading}`,
    inlineMarkdown(chart.intro),
    ...chart.dimensions.flatMap((dimension) => [
      `### ${dimension.heading}`,
      inlineMarkdown(dimension.description),
    ]),
    `${chart.legend.catalog} ${chart.legend.reference}`,
    `${chart.verticalAxis.from} ${chart.verticalAxis.to}`,
    ...cell(chart.cells.specialized, cells.specialized.map(marker)),
    ...cell(chart.cells.shared, cells.shared.map(marker)),
    ...cell(chart.cells.ready, [
      ...cells.ready.map(marker),
      ...READY_REFERENCES.map(referenceMarker),
    ]),
    ...cell(chart.cells.assistants, ASSISTANT_REFERENCES.map(referenceMarker)),
    `${chart.horizontalAxis.from} ${chart.horizontalAxis.to}`,
    inlineMarkdown(chart.caption),
    ...blocks(chart.body),
    chart.notesSummary,
    [...placed.map(placementNote), ...REFERENCE_PLACEMENTS.map(referenceNote)].join('\n'),
    `### ${chart.builtHeading}`,
    ...blocks(chart.builtBody),
    `## ${supervision.heading}`,
    inlineMarkdown(supervision.intro),
    inlineMarkdown(supervision.source),
    '| Boundary | Level | Human attention | Interpretation |',
    '| --- | --- | --- | --- |',
    ...supervision.rows.map((row) => `| ${row.label} | ${row.level} | ${row.attention} | ${row.meaning} |`),
    inlineMarkdown(supervision.limits),
    inlineMarkdown(supervision.scope),
    '### Work domains',
    WORK_DOMAIN_DESCRIPTION,
    '### Approach types',
    'Approach type answers what kind of system the entry describes. It is independent of how work starts.',
    ...APPROACH_TYPE_DEFINITIONS.map((item) => `- **${item.label}:** ${item.meaning}`),
    '### Work modes',
    WORK_MODES_DESCRIPTION,
    ...INVOCATION_DEFINITIONS.map((item) => `- **${item.label}:** ${item.meaning}`),
    terms.eyebrow,
    `## ${terms.heading}`,
    inlineMarkdown(terms.intro),
    `### ${terms.place.heading}`,
    inlineMarkdown(terms.place.definition),
    ...terms.place.figures.flatMap(figure),
    ...blocks(terms.place.body),
    `### ${terms.participation.heading}`,
    inlineMarkdown(terms.participation.definition),
    ...terms.participation.figures.flatMap(figure),
    ...blocks(terms.participation.body),
    terms.combination.label,
    inlineMarkdown(terms.combination.lede),
    ...terms.combination.pairs.map((pair) => `${pair.label}\n:   ${pair.value}`),
    terms.combination.note,
    `### ${terms.autonomy.heading}`,
    ...blocks(terms.autonomy.body),
    `${inlineMarkdown(terms.autonomy.lead)} “${terms.autonomy.quote}” ${inlineMarkdown(terms.autonomy.closing)}`,
    questions.eyebrow,
    `## ${questions.heading}`,
    ...questions.items.flatMap((item) => [item.question, inlineMarkdown(item.answer)]),
  ].join('\n\n');
}

export const GET: APIRoute = () =>
  new Response(`${document()}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
