// ABOUTME: Builds the reading model of one catalog entry from claims and sources.
// ABOUTME: It keeps evidence roles, metric caveats, and claim anchors intact.

import {
  requireApproach,
  sortedApproaches,
  sourcesById,
  type Approach,
  type CatalogSection,
  type Catalog,
  type Claim,
  type ClaimKind,
  type EvidenceRelation,
  type Source,
} from './catalog';
import { fieldLabel, levelLabel, termLabel } from './labels';
import { companyView, type CompanyView } from './companies';
import { isWellDocumented } from './documentation';
import { lessonsForApproach } from './lessons';
import { entryPath } from './routes';
import { shorten } from './text';

/** Where the repository keeps the preserved copy of a source. */
const REPOSITORY_BLOB = 'https://github.com/steel-experiments/internal-agents-map/blob/main/';

export interface PageProfile {
  readonly section: CatalogSection;
  readonly sectionOrder: readonly ('workflow' | 'people' | 'implementation')[];
  readonly label: string;
  readonly path: string;
  /** The mark the navigation draws for this section. */
  readonly icon: 'layers-two' | 'server';
  readonly workflow: string;
  readonly people: string;
  readonly implementation: string;
  readonly validation: string;
  readonly observations: string;
  readonly related: string;
}

/** One profile is shared by HTML and Markdown, with research keys unchanged. */
export function pageProfile(section: CatalogSection): PageProfile {
  return section === 'infrastructure' ? {
    section, sectionOrder: ['implementation', 'workflow', 'people'], label: 'Infrastructure', path: '/infrastructure', icon: 'server',
    workflow: 'Documented uses', people: 'Access and controls',
    implementation: 'Capabilities and architecture', validation: 'Reliability and validation',
    observations: 'Adoption and operating evidence', related: 'Agents using this and related reading',
  } : {
    section, sectionOrder: ['workflow', 'people', 'implementation'], label: 'Agents', path: '/', icon: 'layers-two', workflow: 'How it works',
    people: 'Where people stay involved', implementation: 'Implementation details',
    validation: 'Validation and failure handling', observations: 'Reported observations',
    related: 'Infrastructure used and related reading',
  };
}

export function showQuestion(entry: EntryView, key: string): boolean {
  return !entry.isSupportingSystem || entry.coverageQuestions[key]?.state !== 'not-applicable';
}

export interface CaveatView {
  readonly label: string;
  readonly value: string;
}

export interface CitationView {
  /** The citation number inside this entry, counted from the source list. */
  readonly number: number;
  readonly sourceId: string;
  readonly anchor: string;
  readonly relation: EvidenceRelation;
  readonly relationLabel: string;
  readonly locator: string | null;
  readonly title: string;
}

/**
 * Every architecture field an entry can report, in the order the table shows
 * them. The list is fixed so the table reads the same on every entry, and a
 * field the sources do not report still gets a row.
 */
export const ARCHITECTURE_FIELDS = [
  'model',
  'harness',
  'sandbox',
  'tool_access',
  'knowledge',
  'context_mgmt',
  'credentials',
  'interfaces',
] as const;

/** One row of the architecture table: its label, and the claim if there is one. */
export interface ArchitectureRowView {
  readonly field: string;
  readonly label: string;
  readonly claim: ClaimView | null;
  readonly state?: string;
  readonly note?: string | null;
}

export interface CoverageAnswerView {
  readonly state: string;
  readonly stateLabel: string;
  readonly note: string | null;
  readonly claimAnchors: readonly { readonly anchor: string; readonly label: string }[];
}

export interface ClaimView {
  readonly id: string;
  readonly anchor: string;
  readonly field: string;
  readonly label: string;
  readonly text: string;
  readonly displayName: string | null;
  readonly kind: ClaimKind;
  readonly kindLabel: string;
  readonly provenanceLabel: string;
  readonly confidenceLabel: string;
  readonly confidenceReason: string;
  readonly validAt: string | null;
  readonly isMetric: boolean;
  /** Qualifications that must stay beside the statement. Empty fields stay out. */
  readonly caveats: readonly CaveatView[];
  /** One line that says which qualification of a figure the sources do not report. */
  readonly qualification: string | null;
  /** Every research field of the claim, for the ledger. A metric shows its gaps. */
  readonly metadata: readonly CaveatView[];
  /**
   * True when the role of a citation carries information.
   * One supporting source under one statement needs only its number.
   */
  readonly showCitationRoles: boolean;
  readonly supporting: readonly CitationView[];
  readonly contextualizing: readonly CitationView[];
  readonly contradicting: readonly CitationView[];
  /** Every citation of this claim, in source order. */
  readonly citations: readonly CitationView[];
}

export interface SourceView {
  readonly id: string;
  readonly anchor: string;
  readonly number: number;
  readonly title: string;
  readonly url: string;
  readonly kindLabel: string;
  readonly provenanceClassLabel: string;
  readonly roleLabel: string;
  readonly publisher: string | null;
  readonly publishedAt: string | null;
  readonly accessedAt: string | null;
  readonly lastVerifiedAt: string | null;
  /** The preserved copy in the repository, when the source was captured. */
  readonly preservedUrl: string | null;
  readonly archivedUrl: string | null;
}

export interface OperatingModelView {
  readonly scope: string;
  readonly boundary: string;
  readonly boundaryLabel: string;
  readonly level: number | null;
  readonly levelLabel: string;
}

export interface RelatedEntryView {
  readonly id: string;
  readonly path: string;
  readonly company: string;
  readonly agentName: string;
  readonly relationLabel: string;
  readonly group: 'uses' | 'used-by' | 'related';
}

export interface RelatedLessonView {
  readonly slug: string;
  readonly path: string;
  readonly title: string;
}

export interface TermView {
  readonly id: string;
  readonly label: string;
}

export interface EntryView {
  readonly id: string;
  readonly path: string;
  readonly company: string;
  readonly companyId: string;
  /** The logo or monogram mark the entry header shows. */
  readonly companyView: CompanyView;
  readonly agentName: string;
  readonly title: string;
  readonly catalogSection: CatalogSection;
  readonly approachType: string;
  readonly approachTypeLabel: string;
  /** True when the entry describes infrastructure other systems build on. */
  readonly isSupportingSystem: boolean;
  readonly profile: PageProfile;
  readonly summary: ClaimView | null;
  readonly summaryText: string;
  readonly reviewedAt: string;
  readonly year: number | null;
  readonly statusLabel: string;
  readonly deploymentStageLabel: string;
  readonly autonomyLabel: string;
  readonly evidenceStrengthLabel: string;
  readonly domains: readonly TermView[];
  readonly interfaces: readonly TermView[];
  readonly invocation: readonly TermView[];
  readonly operatingModels: readonly OperatingModelView[];
  readonly isPilot: boolean;
  readonly workflowScope: string | null;
  readonly coverageQuestions: Readonly<Record<string, CoverageAnswerView>>;
  readonly workflowClaims: readonly ClaimView[];
  readonly mechanismClaims: readonly ClaimView[];
  readonly validationClaims: readonly ClaimView[];
  readonly supervisionClaims: readonly ClaimView[];
  readonly architectureClaims: readonly ClaimView[];
  /** The architecture table: one row per field, reported or not. */
  readonly architectureRows: readonly ArchitectureRowView[];
  /** Claims of a metric field whose kind is a metric. */
  readonly metricClaims: readonly ClaimView[];
  /** Claims of a metric field that state a fact, an inference, or an opinion. */
  readonly resultStatementClaims: readonly ClaimView[];
  readonly lessonClaims: readonly ClaimView[];
  readonly canonicalObservationClaims: readonly ClaimView[];
  readonly observationItems: readonly { readonly claim: ClaimView; readonly categoryLabel: string; readonly basisLabel: string; readonly subject: string }[];
  readonly aliasObservationClaims: readonly ClaimView[];
  readonly aliasObservationRelations: readonly { readonly claim: ClaimView; readonly target: ClaimView; readonly reason: string }[];
  readonly researchOnlyClaims: readonly ClaimView[];
  /** Claims that no section above classifies. They keep every claim reachable. */
  readonly otherClaims: readonly ClaimView[];
  readonly claims: readonly ClaimView[];
  readonly sources: readonly SourceView[];
  readonly relatedEntries: readonly RelatedEntryView[];
  /** Lessons about this entry. Later steps fill this from lesson metadata. */
  readonly relatedLessons: readonly RelatedLessonView[];
}

function termView(id: string): TermView {
  return { id, label: termLabel(id) };
}

function preservedUrl(source: Source): string | null {
  const path = source.capture?.artifacts?.markdown?.path;
  return path ? REPOSITORY_BLOB + path : null;
}

function sourceView(source: Source, number: number): SourceView {
  return {
    id: source.id,
    anchor: `source-${source.id}`,
    number,
    title: source.title,
    url: source.url,
    kindLabel: termLabel(source.kind),
    provenanceClassLabel: termLabel(source.provenance_class),
    roleLabel: termLabel(source.role),
    publisher: source.publisher ?? null,
    publishedAt: source.published_at ?? null,
    accessedAt: source.accessed_at ?? null,
    lastVerifiedAt: source.last_verified_at ?? null,
    preservedUrl: preservedUrl(source),
    archivedUrl: source.archived_url ?? null,
  };
}

/** The research fields that qualify a statement, in reading order. */
const QUALIFIER_FIELDS: ReadonlyArray<readonly [keyof Claim, string]> = [
  ['reported_by', 'Reported by'],
  ['metric_scope', 'Scope'],
  ['denominator', 'Denominator'],
  ['measurement_method', 'Method'],
  ['valid_at', 'Observation date'],
];

/** The qualifications a figure cannot stand without. */
const REQUIRED_METRIC_FIELDS: ReadonlyArray<readonly [keyof Claim, string]> = [
  ['metric_scope', 'Scope'],
  ['denominator', 'Denominator'],
];

function fieldValue(claim: Claim, key: keyof Claim): string | null {
  const value = claim[key];
  return value === undefined || value === null ? null : String(value);
}

/**
 * List the qualifications that belong next to a statement.
 * A field the sources do not report stays out of the reading flow.
 */
function caveats(claim: Claim): CaveatView[] {
  const result: CaveatView[] = [];
  for (const [key, label] of QUALIFIER_FIELDS) {
    const value = fieldValue(claim, key);
    if (value !== null) result.push({ label, value });
  }
  return result;
}

/**
 * Say which qualification of a figure the sources do not report.
 * Without this line a number with no denominator reads as a plain outcome.
 */
function qualification(claim: Claim): string | null {
  if (claim.kind !== 'metric') return null;
  const missing = REQUIRED_METRIC_FIELDS.filter(([key]) => fieldValue(claim, key) === null).map(
    ([, label]) => label.toLowerCase(),
  );
  if (missing.length === 0) return null;
  const names = missing.length === 1 ? missing[0] : `${missing[0]} and ${missing[1]}`;
  return `The source does not report the ${names} of this figure.`;
}

/** List every research field of a claim. A metric names the fields it lacks. */
function metadata(claim: Claim): CaveatView[] {
  const result: CaveatView[] = [];
  for (const [key, label] of QUALIFIER_FIELDS) {
    const value = fieldValue(claim, key);
    if (value !== null) result.push({ label, value });
    else if (claim.kind === 'metric') result.push({ label, value: 'Not reported' });
  }
  return result;
}

function claimView(claim: Claim, numbers: ReadonlyMap<string, number>, sources: ReadonlyMap<string, Source>): ClaimView {
  const citations: CitationView[] = claim.evidence.map((evidence) => {
    const source = sources.get(evidence.source_id);
    const number = numbers.get(evidence.source_id);
    if (!source || number === undefined) {
      throw new Error(
        `claim "${claim.id}" (approach "${claim.approach_id}", field "${claim.field}") ` +
          `cites source "${evidence.source_id}", which the approach does not list.`,
      );
    }
    return {
      number,
      sourceId: source.id,
      anchor: `source-${source.id}`,
      relation: evidence.relation,
      relationLabel: termLabel(evidence.relation),
      locator: evidence.locator ?? null,
      title: source.title,
    };
  });
  citations.sort((a, b) => a.number - b.number);
  return {
    id: claim.id,
    anchor: `claim-${claim.id}`,
    field: claim.field,
    label: claim.display_name ?? fieldLabel(claim.field),
    text: claim.text,
    displayName: claim.display_name ?? null,
    kind: claim.kind,
    kindLabel: termLabel(claim.kind),
    provenanceLabel: termLabel(claim.provenance),
    confidenceLabel: termLabel(claim.confidence),
    confidenceReason: claim.confidence_reason,
    validAt: claim.valid_at,
    isMetric: claim.kind === 'metric',
    caveats: caveats(claim),
    qualification: qualification(claim),
    metadata: metadata(claim),
    showCitationRoles:
      citations.length > 1 || citations.some((item) => item.relation !== 'supports'),
    supporting: citations.filter((item) => item.relation === 'supports'),
    contextualizing: citations.filter((item) => item.relation === 'contextualizes'),
    contradicting: citations.filter((item) => item.relation === 'contradicts'),
    citations,
  };
}

function relatedEntries(catalog: Catalog, approach: Approach): RelatedEntryView[] {
  const byId = new Map(catalog.approaches.map((item) => [item.id, item]));
  const related: RelatedEntryView[] = [];
  const add = (id: string, relationLabel: string, group: RelatedEntryView['group']) => {
    const target = byId.get(id);
    if (!target || target.id === approach.id) return;
    if (related.some((item) => item.id === target.id)) return;
    related.push({
      id: target.id,
      path: entryPath(target.id),
      company: target.company,
      agentName: target.agent_name,
      relationLabel,
      group,
    });
  };
  for (const relationship of approach.relationships ?? []) {
    add(
      relationship.approach_id,
      relationship.type === 'built-on' ? 'Built on' : relationship.type === 'component-of' ? 'Component of' : 'Related implementation',
      relationship.type === 'built-on' ? 'uses' : 'related',
    );
  }
  for (const other of catalog.approaches) {
    for (const relationship of other.relationships ?? []) {
      if (relationship.approach_id !== approach.id) continue;
      add(
        other.id,
        relationship.type === 'built-on' ? 'Uses this infrastructure' : relationship.type === 'component-of' ? 'Includes component' : 'Related implementation',
        relationship.type === 'built-on' && other.catalog_section === 'agents' ? 'used-by' : 'related',
      );
    }
  }
  return related;
}

/** Build the reading model of one entry from the normalized catalog. */
export function entryView(catalog: Catalog, id: string): EntryView {
  const approach = requireApproach(catalog, id);
  const allSources = sourcesById(catalog);
  const allClaims = new Map(catalog.claims.map((claim) => [claim.id, claim]));

  const numbers = new Map<string, number>();
  const sources: SourceView[] = approach.source_ids.map((sourceId, index) => {
    const source = allSources.get(sourceId);
    if (!source) throw new Error(`approach "${approach.id}" lists unknown source "${sourceId}".`);
    numbers.set(sourceId, index + 1);
    return sourceView(source, index + 1);
  });

  const claims = approach.claim_ids.map((claimId) => {
    const claim = allClaims.get(claimId);
    if (!claim) throw new Error(`approach "${approach.id}" lists unknown claim "${claimId}".`);
    return claimView(claim, numbers, allSources);
  });

  const of = (test: (claim: ClaimView) => boolean) => claims.filter(test);
  const summary = claims.find((claim) => claim.field === 'summary') ?? null;
  const page = approach.page_content;
  const byField = new Map(claims.map((claim) => [claim.field, claim]));
  const fromPaths = (paths: readonly string[]) =>
    paths
      .map((path) => byField.get(path))
      .filter((claim): claim is ClaimView => Boolean(claim));
  const legacyWorkflowClaims = of((claim) => claim.field.startsWith('primitives.'));
  const workflowClaims = page ? fromPaths(page.questions.workflow.claim_paths) : legacyWorkflowClaims;
  const mechanismClaims = page
    ? of((claim) => page.primitive_roles[claim.field] === 'mechanism')
    : [];
  const validationClaims = page
    ? of((claim) => page.primitive_roles[claim.field] === 'validation')
    : [];
  const supervisionClaims = approach.catalog_section === 'agents' ? of((claim) => claim.field.startsWith('operating_models.')) : [];
  const allArchitectureClaims = of((claim) => claim.field.startsWith('architecture.'));
  const architectureClaims = page
    ? allArchitectureClaims.filter((claim) => {
        const key = claim.field.slice('architecture.'.length) as keyof typeof page.implementation_fields;
        return page.implementation_fields[key]?.state === 'reported';
      })
    : allArchitectureClaims;
  const resultClaims = of(
    (claim) => claim.field === 'headline_metric' || claim.field.startsWith('key_metrics.'),
  );
  const lessonClaims = of((claim) => claim.field.startsWith('lessons_learned.'));
  const canonicalObservationClaims = page
    ? resultClaims.filter((claim) => !page.observations[claim.field]?.duplicate_of)
    : resultClaims;
  const aliasObservationClaims = page
    ? resultClaims.filter((claim) => Boolean(page.observations[claim.field]?.duplicate_of))
    : [];
  const aliasObservationRelations = page
    ? aliasObservationClaims.map((claim) => ({
        claim,
        target: byField.get(page.observations[claim.field]!.duplicate_of!)!,
        reason: page.observations[claim.field]!.reason ?? 'Duplicate representation.',
      }))
    : [];
  const observationItems = page
    ? canonicalObservationClaims.map((claim) => {
        const observation = page.observations[claim.field]!;
        return {
          claim,
          categoryLabel: termLabel(observation.category!),
          basisLabel: termLabel(observation.basis!),
          subject: observation.subject!,
        };
      })
    : [];
  const metricClaims = canonicalObservationClaims.filter((claim) => claim.isMetric);
  const resultStatementClaims = canonicalObservationClaims.filter((claim) => !claim.isMetric);
  const placed = new Set(
    [summary, ...workflowClaims, ...mechanismClaims, ...validationClaims, ...supervisionClaims, ...architectureClaims, ...canonicalObservationClaims, ...lessonClaims]
      .filter((claim): claim is ClaimView => claim !== null)
      .map((claim) => claim.id),
  );
  const researchOnlyClaims = page ? claims.filter((claim) => !placed.has(claim.id)) : [];
  const coverageQuestions = Object.fromEntries(
    Object.entries(page?.questions ?? {}).map(([key, disposition]) => [
      key,
      {
        state: disposition.state,
        stateLabel: termLabel(disposition.state),
        note: disposition.note ?? null,
        claimAnchors: disposition.claim_paths
          .map((path) => byField.get(path))
          .filter((claim): claim is ClaimView => Boolean(claim))
          .map((claim) => ({ anchor: claim.anchor, label: claim.displayName ?? claim.label })),
      },
    ]),
  );

  return {
    id: approach.id,
    path: entryPath(approach.id),
    company: approach.company,
    companyId: approach.company_id,
    companyView: companyView(catalog, approach.company_id),
    agentName: approach.agent_name,
    title: `${approach.company} — ${approach.agent_name}`,
    catalogSection: approach.catalog_section,
    approachType: approach.approach_type,
    approachTypeLabel: termLabel(approach.approach_type),
    isSupportingSystem: approach.catalog_section === 'infrastructure',
    profile: pageProfile(approach.catalog_section),
    summary,
    summaryText: summary?.text ?? '',
    reviewedAt: approach.last_reviewed_at,
    year: approach.year ?? null,
    statusLabel: termLabel(approach.status),
    deploymentStageLabel: termLabel(approach.deployment_stage),
    autonomyLabel: termLabel(approach.autonomy),
    evidenceStrengthLabel: termLabel(approach.rubric.evidence_strength),
    domains: approach.domains.map(termView),
    interfaces: (approach.interfaces ?? []).map(termView),
    invocation: approach.rubric.invocation.map(termView),
    operatingModels: approach.operating_models.map((model) => ({
      scope: model.scope,
      boundary: model.attention_boundary,
      boundaryLabel: termLabel(model.attention_boundary),
      level: model.level,
      levelLabel: levelLabel(model.level),
    })),
    isPilot: Boolean(page),
    workflowScope: page?.workflow_scope ?? null,
    coverageQuestions,
    workflowClaims,
    mechanismClaims,
    validationClaims,
    supervisionClaims,
    architectureClaims,
    architectureRows: ARCHITECTURE_FIELDS.map((key) => {
      const field = `architecture.${key}`;
      return {
        field,
        label: fieldLabel(field),
        claim: architectureClaims.find((claim) => claim.field === field) ?? null,
        state: page?.implementation_fields[key].state,
        note: page?.implementation_fields[key].note ?? null,
      };
    }),
    metricClaims,
    resultStatementClaims,
    lessonClaims,
    canonicalObservationClaims,
    observationItems,
    aliasObservationClaims,
    aliasObservationRelations,
    researchOnlyClaims,
    otherClaims: page ? [] : claims.filter((claim) => !placed.has(claim.id)),
    claims,
    sources,
    relatedEntries: relatedEntries(catalog, approach),
    relatedLessons: lessonsForApproach(approach.id),
  };
}

export interface DirectoryCard {
  readonly id: string;
  readonly path: string;
  readonly company: string;
  /** The logo or monogram mark the card shows beside the company name. */
  readonly companyView: CompanyView;
  readonly agentName: string;
  /** The company and the name, such as `Stripe · Minions`, as the card and the palette show them. */
  readonly title: string;
  readonly summary: string;
  /** The first sentences of the summary, for the directory card. */
  readonly excerpt: string;
  /** The text the directory search reads, normalized to lower case. */
  readonly search: string;
  readonly catalogSection: CatalogSection;
  readonly approachType: string;
  readonly approachTypeLabel: string;
  /**
   * The type the card names, or null for a plain agent: the Agents view holds only agents,
   * so the tag would say nothing there.
   */
  readonly typeTag: string | null;
  readonly domains: readonly TermView[];
  readonly invocation: readonly TermView[];
  /** The attention boundaries of the scoped operating models, with their derived levels. */
  readonly boundaries: readonly BoundaryView[];
  readonly reviewedAt: string;
  /** The source identifiers of the entry, so an old source fragment can find its page. */
  readonly sourceIds: readonly string[];
  /** True when the editors show the entry before all others in the default order. */
  readonly featured: boolean;
  /** True when the evidence of the entry meets the well-documented rule. */
  readonly wellDocumented: boolean;
  /** The position of the entry in the alphabetical order, so the browser can sort it again. */
  readonly alphabeticalRank: number;
}

/** An attention boundary as a filter term. The level is null when the boundary is unknown. */
export interface BoundaryView extends TermView {
  readonly level: number | null;
}

/** The length a directory card shows before it links to the whole entry. */
export const CARD_SUMMARY_LIMIT = 200;

/** Join the words a card is searchable by, in the form the browser compares. */
function searchText(parts: readonly string[]): string {
  return parts.join(' ').replace(/\s+/g, ' ').trim().toLowerCase();
}

/** Build the compact card of every implementation, ordered the way the directory reads. */
export function directoryCards(catalog: Catalog): DirectoryCard[] {
  const claims = new Map(catalog.claims.map((claim) => [claim.id, claim]));
  return sortedApproaches(catalog).map((approach, alphabeticalRank) => {
    const summary = approach.claim_ids
      .map((claimId) => claims.get(claimId))
      .find((claim) => claim?.field === 'summary');
    const levels = new Map(
      approach.operating_models.map((model) => [model.attention_boundary, model.level]),
    );
    if (levels.size === 0) levels.set('unknown', null);
    const boundaries: BoundaryView[] = [...levels.keys()]
      .sort()
      .map((id) => ({ ...termView(id), level: levels.get(id) ?? null }));
    const domains = approach.domains.map(termView);
    const invocation = approach.rubric.invocation.map(termView);
    return {
      id: approach.id,
      path: entryPath(approach.id),
      company: approach.company,
      companyView: companyView(catalog, approach.company_id),
      agentName: approach.agent_name,
      title: `${approach.company} · ${approach.agent_name}`,
      summary: summary?.text ?? 'Unknown',
      excerpt: shorten(summary?.text ?? 'Unknown', CARD_SUMMARY_LIMIT),
      search: searchText([
        approach.company,
        approach.agent_name,
        summary?.text ?? '',
        approach.approach_type,
        termLabel(approach.approach_type),
        ...domains.flatMap((domain) => [domain.id, domain.label]),
        ...(approach.catalog_section === 'agents' ? [
          ...invocation.flatMap((mode) => [mode.id, mode.label, mode.id === 'interactive' ? 'foreground' : '']),
          ...boundaries.flatMap((boundary) => [boundary.id, boundary.label, levelLabel(boundary.level)]),
          approach.autonomy,
          termLabel(approach.autonomy),
        ] : []),
      ]),
      catalogSection: approach.catalog_section,
      approachType: approach.approach_type,
      approachTypeLabel: termLabel(approach.approach_type),
      typeTag: approach.approach_type === 'agent' ? null : termLabel(approach.approach_type),
      sourceIds: approach.source_ids,
      domains,
      invocation: approach.catalog_section === 'agents' ? invocation : [],
      boundaries: approach.catalog_section === 'agents' ? boundaries : [],
      reviewedAt: approach.last_reviewed_at,
      featured: approach.featured === true,
      wellDocumented: isWellDocumented(catalog, approach),
      alphabeticalRank,
    };
  });
}
