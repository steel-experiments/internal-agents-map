// ABOUTME: Renders the Markdown representations of one entry and of the whole catalog.
// ABOUTME: Every claim, qualification, original citation, and preserved copy stays in the text.

import { claimsById, requireApproach, sortedApproaches, sourcesById, type Catalog } from './catalog';
import { requireCompany } from './companies';
import {
  entryView,
  showQuestion,
  type ClaimView,
  type CoverageAnswerView,
  type EntryView,
  type SourceView,
  type TermView,
} from './entry-view';
import { SITE_DESCRIPTION, SITE_NAME } from './metadata';
import {
  organizationPath,
  ORIGIN,
  canonicalUrl,
  entryJsonPath,
  entryPath,
  homePath,
  markdownPath,
} from './routes';

/** The schema version of the compact index. It is separate from the catalog version. */
export const COMPACT_INDEX_SCHEMA_VERSION = 3;

/** Serialize an export the way the published JSON files are written. */
export function jsonDocument(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

/**
 * The record of one implementation in the catalog schema.
 * It carries the approach with the claims, the sources, and the company that it lists,
 * so the record validates as a complete catalog on its own.
 */
export function recordJson(catalog: Catalog, id: string): string {
  const approach = requireApproach(catalog, id);
  const claims = claimsById(catalog);
  const sources = sourcesById(catalog);
  return jsonDocument({
    schema_version: catalog.schema_version,
    approaches: [approach],
    claims: approach.claim_ids.map((claimId) => claims.get(claimId)),
    sources: approach.source_ids.map((sourceId) => sources.get(sourceId)),
    companies: [requireCompany(catalog, approach.company_id)],
  });
}

/** The compact index that a reader fetches before the individual records. */
export function compactIndexJson(catalog: Catalog): string {
  return jsonDocument({
    schema_version: COMPACT_INDEX_SCHEMA_VERSION,
    approaches: catalog.approaches.map((approach) => ({
      id: approach.id,
      company: approach.company,
      agent_name: approach.agent_name,
      approach_type: approach.approach_type,
      catalog_section: approach.catalog_section,
      domains: approach.domains,
      last_reviewed_at: approach.last_reviewed_at,
      url: canonicalUrl(entryPath(approach.id)),
      json_url: `${ORIGIN}${entryJsonPath(approach.id)}`,
      markdown_url: `${ORIGIN}${markdownPath(entryPath(approach.id))}`,
    })),
  });
}

/** A heading of the given depth, so one renderer serves both export files. */
function heading(level: number, text: string): string {
  return `${'#'.repeat(level)} ${text}`;
}

/** Keep link text readable when catalog prose holds bracket characters. */
function escapeLinkText(text: string): string {
  return text.replace(/([\[\]])/g, '\\$1');
}

/** A Markdown link. A URL with spaces or parentheses needs angle brackets. */
export function markdownLink(text: string, url: string): string {
  const target = /[()\s]/.test(url) ? `<${url}>` : url;
  return `[${escapeLinkText(text)}](${target})`;
}

/** Join the parts of one metadata line and drop the parts that have no value. */
function joinParts(parts: ReadonlyArray<string | null>, separator = ' · '): string {
  return parts.filter((part): part is string => Boolean(part)).join(separator);
}

function termList(terms: readonly TermView[]): string | null {
  return terms.length > 0 ? terms.map((term) => term.label).join(', ') : null;
}

/** The sources of one entry, indexed by identifier. */
type SourceIndex = ReadonlyMap<string, SourceView>;

/** One citation line: the relation, the number, the publisher link, and the copy. */
function citationLines(claim: ClaimView, sources: SourceIndex): string[] {
  return claim.citations.map((citation) => {
    // The reading model already rejects a citation of a source the entry omits.
    const source = sources.get(citation.sourceId)!;
    const parts = [
      `${citation.relationLabel} · [${citation.number}] ` +
        markdownLink(citation.title, source.url),
    ];
    if (source.preservedUrl) parts.push(markdownLink('Preserved copy', source.preservedUrl));
    if (citation.locator) parts.push(citation.locator);
    return `- ${joinParts(parts)}`;
  });
}

/** Render one claim with its qualifications and every source that it cites. */
function claimBlock(claim: ClaimView, sources: SourceIndex, level: number): string[] {
  const lines = [heading(level, claim.label), '', claim.text.trim(), ''];
  lines.push(
    joinParts([
      claim.kindLabel,
      claim.provenanceLabel,
      `${claim.confidenceLabel} confidence`,
      `\`${claim.id}\``,
    ]),
    '',
  );
  if (claim.confidenceReason) {
    lines.push(`Confidence reason: ${claim.confidenceReason}`, '');
  }
  if (claim.qualification || claim.caveats.length > 0) {
    lines.push('Qualifications:', '');
    // The line about a figure the sources do not qualify opens the list.
    if (claim.qualification) lines.push(`- ${claim.qualification}`);
    for (const caveat of claim.caveats) lines.push(`- ${caveat.label}: ${caveat.value}`);
    lines.push('');
  }
  if (claim.citations.length > 0) {
    lines.push('Evidence:', '', ...citationLines(claim, sources), '');
  }
  return lines;
}

/** Render a group of claims under one section heading. */
/** State an answered question in one line. A state that says it all stands alone. */
function answerLine(answer: CoverageAnswerView): string {
  return `**${answer.stateLabel}${answer.note ? ':' : ''}**${answer.note ? ` ${answer.note}` : ''}`;
}

function claimSection(
  title: string,
  claims: readonly ClaimView[],
  sources: SourceIndex,
  level: number,
): string[] {
  if (claims.length === 0) return [];
  return [
    heading(level, title),
    '',
    ...claims.flatMap((claim) => claimBlock(claim, sources, level + 1)),
  ];
}

/** Render one source with its original URL, its dates, and its preserved copies. */
function sourceBlock(source: SourceView): string[] {
  const lines = [
    `${source.number}. ${markdownLink(source.title, source.url)}`,
    `   - ${joinParts([source.kindLabel, source.provenanceClassLabel, source.roleLabel])}`,
    `   - Original URL: <${source.url}>`,
  ];
  const dates = joinParts([
    source.publisher ? `Publisher: ${source.publisher}` : null,
    source.publishedAt ? `Published: ${source.publishedAt}` : null,
    source.accessedAt ? `Accessed: ${source.accessedAt}` : null,
    source.lastVerifiedAt ? `Last verified: ${source.lastVerifiedAt}` : null,
  ]);
  if (dates) lines.push(`   - ${dates}`);
  if (source.preservedUrl) {
    lines.push(`   - Preserved copy in the repository: <${source.preservedUrl}>`);
  }
  if (source.archivedUrl) lines.push(`   - Archived copy: <${source.archivedUrl}>`);
  return lines;
}

/** The identification lines that open an entry. */
function factLines(entry: EntryView): string[] {
  const facts: ReadonlyArray<readonly [string, string | null]> = [
    ['Company', markdownLink(entry.company, canonicalUrl(organizationPath(entry.companyView.id)))],
    ['Collection', entry.profile.label],
    ['Approach type', entry.approachTypeLabel],
    ['Deployment stage', entry.deploymentStageLabel],
    ['Autonomy', entry.isSupportingSystem ? null : entry.autonomyLabel],
    ['Evidence strength', entry.evidenceStrengthLabel],
    ['Status', entry.statusLabel],
    ['First reported year', entry.year === null ? 'Unknown' : String(entry.year)],
    ['Work', termList(entry.domains)],
    ['Interfaces', termList(entry.interfaces)],
    ['Invocation', entry.isSupportingSystem ? null : termList(entry.invocation)],
    ['Entry reviewed', entry.reviewedAt],
  ];
  return facts
    .filter((fact): fact is readonly [string, string] => fact[1] !== null)
    .map(([label, value]) => `- ${label}: ${value}`);
}

/**
 * Render one entry as Markdown.
 * `level` is the depth of the entry title, so the catalog file can nest entries.
 */
export function entryMarkdown(entry: EntryView, level = 1): string[] {
  const sources: SourceIndex = new Map(entry.sources.map((source) => [source.id, source]));
  const lines = [heading(level, entry.title), ''];
  if (entry.summaryText) lines.push(entry.summaryText.trim(), '');
  lines.push(...factLines(entry), '');
  // The catalog file needs the address of each entry; the record file states it above.
  if (level > 1) lines.push(`Page: ${canonicalUrl(entry.path)}`, '');

  if (entry.isSupportingSystem) {
    lines.push(...claimSection('Purpose', entry.summary ? [entry.summary] : [], sources, level + 1));
    for (const section of entry.profile.sectionOrder) {
      if (section === 'implementation') {
        lines.push(heading(level + 1, entry.profile.implementation), '');
        lines.push(...[...entry.architectureClaims, ...entry.mechanismClaims].flatMap((claim) => claimBlock(claim, sources, level + 2)));
        for (const row of entry.architectureRows.filter((row) => !row.claim)) lines.push(`- **${row.label}:** ${row.state ?? 'Unreported'}${row.note ? ` — ${row.note}` : ''}`);
        lines.push('');
      } else if (section === 'workflow' && showQuestion(entry, 'workflow')) {
        lines.push(heading(level + 1, entry.profile.workflow), '');
        if (entry.workflowScope) lines.push(`Documented use example: ${entry.workflowScope}.`, '');
        lines.push(...entry.workflowClaims.flatMap((claim) => claimBlock(claim, sources, level + 2)));
        if (!entry.workflowClaims.length) lines.push(entry.coverageQuestions.workflow?.note ?? 'No documented use example is reported.', '');
      } else if (section === 'people') {
        lines.push(heading(level + 1, entry.profile.people), '');
        const credentials = entry.architectureClaims.find((claim) => claim.field === 'architecture.credentials');
        lines.push(credentials ? `See the credential and access boundaries in architecture (\`${credentials.id}\`). Scoped human-review assessments for individual uses remain in research details.` : 'No separate access-control assessment is recorded.', '');
      }
    }
    if (showQuestion(entry, 'validation')) {
      lines.push(heading(level + 1, entry.profile.validation), '');
      lines.push(...entry.validationClaims.flatMap((claim) => claimBlock(claim, sources, level + 2)));
      if (!entry.validationClaims.length) lines.push(entry.coverageQuestions.validation?.note ?? 'Not reported.', '');
    }
    if (showQuestion(entry, 'observations')) {
      lines.push(heading(level + 1, entry.profile.observations), '');
      for (const item of entry.observationItems) {
        lines.push(`Observation: ${item.categoryLabel} · ${item.basisLabel} · ${item.subject}`, '');
        lines.push(...claimBlock(item.claim, sources, level + 2));
      }
      if (!entry.observationItems.length) lines.push(entry.coverageQuestions.observations?.note ?? 'Not reported.', '');
    }
    if (showQuestion(entry, 'lessons')) {
      lines.push(...claimSection('Lessons', entry.lessonClaims, sources, level + 1));
      if (!entry.lessonClaims.length) lines.push(entry.coverageQuestions.lessons?.note ?? 'Not reported.', '');
    }
    if (entry.aliasObservationRelations.length) {
      lines.push(heading(level + 1, 'Duplicate observation representations'), '');
      for (const relation of entry.aliasObservationRelations) {
        lines.push(`Duplicate of \`${relation.target.id}\`: ${relation.reason}`, '');
        lines.push(...claimBlock(relation.claim, sources, level + 2));
      }
    }
    const aliases = new Set(entry.aliasObservationClaims.map((claim) => claim.id));
    lines.push(...claimSection('Research details and scoped use assessments', entry.researchOnlyClaims.filter((claim) => !aliases.has(claim.id)), sources, level + 1));
  } else {
    if (entry.isPilot) {
      lines.push(...claimSection('Purpose', entry.summary ? [entry.summary] : [], sources, level + 1));
      if (entry.workflowScope) lines.push(`Representative workflow: ${entry.workflowScope}.`, '');
      lines.push(...claimSection(entry.profile.workflow, entry.workflowClaims, sources, level + 1));
      if (entry.workflowClaims.length === 0 && showQuestion(entry, 'workflow') && entry.coverageQuestions.workflow) {
        const workflow = entry.coverageQuestions.workflow;
        lines.push(heading(level + 1, entry.profile.workflow), '', answerLine(workflow), '');
      }
      lines.push(heading(level + 1, entry.profile.people), '');
      for (const model of entry.isSupportingSystem ? [] : entry.operatingModels) {
        lines.push(`- **${model.scope}** — ${model.boundaryLabel} · ${model.levelLabel}`);
      }
      const people = entry.coverageQuestions.human_involvement;
      if (people?.note) lines.push('', `**${people.stateLabel}:** ${people.note}`);
      lines.push('');
      lines.push(...claimSection('Supervision evidence', entry.supervisionClaims, sources, level + 2));
      lines.push(...claimSection(entry.profile.implementation, [...entry.architectureClaims, ...entry.mechanismClaims], sources, level + 1));
      lines.push(heading(level + 2, 'Implementation coverage'), '');
      for (const row of entry.architectureRows) {
        lines.push(`- **${row.label}:** ${row.state ?? 'Unassessed'}${row.note ? ` — ${row.note}` : ''}`);
      }
      lines.push('');
      lines.push(...claimSection(entry.profile.validation, entry.validationClaims, sources, level + 1));
      if (entry.validationClaims.length === 0 && entry.coverageQuestions.validation) {
        lines.push(heading(level + 1, entry.profile.validation), '', answerLine(entry.coverageQuestions.validation), '');
      }
      if (entry.observationItems.length > 0) {
        lines.push(heading(level + 1, entry.profile.observations), '');
        for (const item of entry.observationItems) {
          lines.push(`Observation: ${item.categoryLabel} · ${item.basisLabel} · ${item.subject}`, '');
          lines.push(...claimBlock(item.claim, sources, level + 2));
        }
      }
      if (entry.canonicalObservationClaims.length === 0 && entry.coverageQuestions.observations) {
        lines.push(heading(level + 1, entry.profile.observations), '', answerLine(entry.coverageQuestions.observations), '');
      }
      lines.push(...claimSection('Lessons', entry.lessonClaims, sources, level + 1));
      if (entry.lessonClaims.length === 0 && entry.coverageQuestions.lessons) {
        lines.push(heading(level + 1, 'Lessons'), '', answerLine(entry.coverageQuestions.lessons), '');
      }
      if (entry.aliasObservationRelations.length > 0) {
        lines.push(heading(level + 1, 'Duplicate observation representations'), '');
        for (const relation of entry.aliasObservationRelations) {
          lines.push(`Duplicate of \`${relation.target.id}\`: ${relation.reason}`, '');
          lines.push(...claimBlock(relation.claim, sources, level + 2));
        }
      }
      const aliasIds = new Set(entry.aliasObservationClaims.map((claim) => claim.id));
      lines.push(...claimSection('Reviewed legacy details', entry.researchOnlyClaims.filter((claim) => !aliasIds.has(claim.id)), sources, level + 1));
    } else if (entry.operatingModels.length > 0) {
      lines.push(heading(level + 1, entry.profile.people), '');
      lines.push(
        `Each scope pairs its normal attention boundary with supporting evidence. See the [supervision definitions](${canonicalUrl('/definitions#supervision')}) for the level mapping and limits.`,
        '',
      );
      for (const model of entry.isSupportingSystem ? [] : entry.operatingModels) {
        lines.push(`- **${model.scope}** — ${model.boundaryLabel} · ${model.levelLabel}`);
      }
      lines.push('');
    }

    const sections: ReadonlyArray<readonly [string, readonly ClaimView[]]> = entry.isPilot ? [] : [
      ['Overview', entry.summary ? [entry.summary] : []],
      ['How it works', entry.workflowClaims],
      ['Supervision evidence', entry.supervisionClaims],
      ['Implementation details', entry.architectureClaims],
      ['Reported metrics', entry.metricClaims],
      ['Reported outcomes and statements', entry.resultStatementClaims],
      ['Lessons and interpretation', entry.lessonClaims],
      ['Other reported details', entry.otherClaims],
    ];
    for (const [title, claims] of sections) {
      lines.push(...claimSection(title, claims, sources, level + 1));
    }
  }
  lines.push(heading(level + 1, 'Question coverage and scope'), '');
  for (const [key, answer] of Object.entries(entry.coverageQuestions)) lines.push(`- **${key.replaceAll('_', ' ')}:** ${answer.stateLabel}${answer.note ? ` — ${answer.note}` : ''}`);
  lines.push('');

  if (entry.relatedEntries.length > 0) {
    lines.push(heading(level + 1, 'Related reading'), '');
    for (const related of entry.relatedEntries) {
      const name = `${related.company} — ${related.agentName}`;
      lines.push(`- ${related.relationLabel}: ${markdownLink(name, canonicalUrl(related.path))}`);
    }
    lines.push('');
  }

  if (entry.sources.length > 0) {
    lines.push(heading(level + 1, 'Sources'), '');
    for (const source of entry.sources) lines.push(...sourceBlock(source));
    lines.push('');
  }
  return lines;
}

/** Join rendered lines into a file that starts with the page it represents. */
function document(url: string, lines: readonly string[]): string {
  const body = lines.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  return `Source: ${url}\n\n${body}\n`;
}

/** The complete Markdown record of one implementation. */
export function recordMarkdown(catalog: Catalog, id: string): string {
  const entry = entryView(catalog, id);
  return document(canonicalUrl(entry.path), entryMarkdown(entry, 1));
}

/**
 * The complete Markdown catalog.
 * It holds every entry in full, not the short text of the directory cards.
 */
export function catalogMarkdown(catalog: Catalog, section: 'agents' | 'infrastructure' = 'agents'): string {
  const approaches = sortedApproaches(catalog).filter((item) => item.catalog_section === section);
  const organizations = new Set(approaches.map((approach) => approach.company)).size;
  const reviewed = approaches
    .map((approach) => approach.last_reviewed_at)
    .sort()
    .at(-1);
  const lines = [
    heading(1, `${SITE_NAME} — ${section === 'agents' ? 'Agents' : 'Infrastructure'}`),
    '',
    SITE_DESCRIPTION,
    '',
    `- ${section === 'agents' ? 'Agents' : 'Infrastructure records'}: ${approaches.length}`,
    `- Organizations: ${organizations}`,
    `- Sources: ${new Set(approaches.flatMap((item) => item.source_ids).map((id) => { const source = catalog.sources.find((item) => item.id === id); return source?.canonical_url ?? source?.url; })).size}`,
    `- Claims: ${approaches.reduce((sum, item) => sum + item.claim_ids.length, 0)}`,
    `- Latest entry review: ${reviewed ?? 'Unknown'}. Individual source dates vary.`,
    '',
    `This file holds the ${section} collection with all of its claims, qualifications, and`,
    'sources. The compact index is at ' + `${ORIGIN}/agents/index.json`,
    `and the complete dataset is at ${ORIGIN}/agents.json.`,
    '',
    `[Agents](${ORIGIN}/index.md) · [Infrastructure](${ORIGIN}/infrastructure.md). Historical JSON endpoints contain both collections.`,
    '',
    'Company-reported metrics and catalog judgments are not independent verification.',
    'Keep the qualifications and the dates with the statements that they belong to.',
    '',
  ];
  for (const approach of approaches) {
    lines.push(...entryMarkdown(entryView(catalog, approach.id), 2));
  }
  return document(canonicalUrl(section === 'agents' ? homePath() : '/infrastructure'), lines);
}
