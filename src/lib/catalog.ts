// ABOUTME: Loads the normalized catalog and checks the structure the website needs.
// ABOUTME: A record, claim, or source reference that does not resolve stops the build.

import catalogText from '../../data/agents.json?raw';

/** The only catalog schema this website reads. */
export const CATALOG_SCHEMA_VERSION = 7;

const CATALOG_FILE = 'data/agents.json';

export type ClaimKind = 'fact' | 'inference' | 'metric' | 'opinion';
export type ClaimProvenance = 'reported' | 'catalog-judgment';
export type EvidenceRelation = 'supports' | 'contextualizes' | 'contradicts';

export interface Evidence {
  readonly source_id: string;
  readonly relation: EvidenceRelation;
  readonly locator?: string;
}

export interface Claim {
  readonly id: string;
  readonly approach_id: string;
  readonly field: string;
  readonly text: string;
  readonly kind: ClaimKind;
  readonly provenance: ClaimProvenance;
  readonly confidence: string;
  readonly confidence_reason: string;
  readonly valid_at: string | null;
  readonly evidence: readonly Evidence[];
  readonly reported_by?: string | null;
  readonly metric_scope?: string | null;
  readonly denominator?: string | null;
  readonly measurement_method?: string | null;
  readonly unit?: string | null;
  readonly value?: string | number | null;
  readonly display_name?: string;
}

export type ReviewState = 'reported' | 'unreported' | 'not-applicable' | 'not-reviewed';
export interface CoverageDisposition {
  readonly state: ReviewState;
  readonly claim_paths: readonly string[];
  readonly note?: string;
}
export interface ObservationMetadata {
  readonly category?: 'effectiveness' | 'adoption-output' | 'cost-latency' | 'implementation-scale' | 'runtime-capacity';
  readonly basis?: 'reported-measurement' | 'qualitative' | 'estimate' | 'target';
  readonly subject?: string;
  readonly duplicate_of?: string;
  readonly reason?: string;
}
export interface PageContent {
  readonly version: 1;
  readonly reviewed_at: string;
  readonly source_ids: readonly string[];
  readonly workflow_scope?: string;
  readonly questions: Readonly<Record<'purpose' | 'workflow' | 'human_involvement' | 'implementation' | 'validation' | 'observations' | 'lessons', CoverageDisposition>>;
  readonly implementation_fields: Readonly<Record<'model' | 'harness' | 'sandbox' | 'tool_access' | 'knowledge' | 'context_mgmt' | 'credentials' | 'interfaces', CoverageDisposition>>;
  readonly primitive_roles: Readonly<Record<string, 'workflow' | 'mechanism' | 'validation'>>;
  readonly observations: Readonly<Record<string, ObservationMetadata>>;
}

export interface SourceCapture {
  readonly artifacts?: {
    readonly markdown?: { readonly path?: string };
  };
}

export interface Source {
  readonly id: string;
  readonly approach_id: string;
  readonly title: string;
  readonly url: string;
  readonly canonical_url?: string;
  readonly kind: string;
  readonly provenance_class: string;
  readonly role: string;
  readonly publisher?: string | null;
  readonly authors?: readonly string[] | null;
  readonly published_at?: string | null;
  readonly accessed_at?: string | null;
  readonly last_verified_at?: string | null;
  readonly archived_url?: string | null;
  readonly duplicate_of?: string | null;
  readonly capture?: SourceCapture | null;
}

export interface OperatingModel {
  readonly scope: string;
  readonly attention_boundary: string;
  readonly level: number | null;
}

export interface Relationship {
  readonly type: string;
  readonly approach_id: string;
}

/** The vendored logo of one organization, with the provenance of the asset. */
export interface CompanyLogo {
  readonly path: string;
  readonly media_type: string;
  readonly width: number;
  readonly height: number;
  readonly bytes: number;
  readonly sha256: string;
  readonly source_url: string;
  readonly accessed_at: string;
}

/** One organization the catalog names, joined to its approaches by identifier. */
export interface Company {
  readonly id: string;
  readonly name: string;
  readonly homepage: string;
  readonly logo: CompanyLogo | null;
}

export interface Rubric {
  readonly invocation: readonly string[];
  readonly state: string;
  readonly identity: string;
  readonly evidence_strength: string;
}

export type CatalogSection = 'agents' | 'infrastructure';

/** Collection is always derived from the structural type, never editorially duplicated. */
export function catalogSection(type: string): CatalogSection {
  if (type === 'agent' || type === 'agent-system') return 'agents';
  if (['platform', 'supporting-pattern', 'orchestration-system'].includes(type)) return 'infrastructure';
  throw new Error(`Unknown approach type "${type}".`);
}

export interface Approach {
  readonly id: string;
  readonly company: string;
  readonly company_id: string;
  readonly agent_name: string;
  readonly approach_type: string;
  readonly catalog_section: CatalogSection;
  readonly deployment_stage: string;
  readonly year: number | null;
  readonly last_reviewed_at: string;
  readonly status: string;
  readonly domains: readonly string[];
  readonly autonomy: string;
  readonly operating_models: readonly OperatingModel[];
  readonly rubric: Rubric;
  readonly claim_ids: readonly string[];
  readonly source_ids: readonly string[];
  readonly interfaces?: readonly string[];
  readonly aliases?: readonly string[];
  /** True when the catalog shows the record before all others in the default order. */
  readonly featured?: boolean;
  readonly relationships?: readonly Relationship[];
  readonly page_content?: PageContent;
}

/** Count one family once and deduplicate shared source URLs within a collection. */
export function collectionCounts(catalog: Catalog, section: CatalogSection) {
  const approaches = catalog.approaches.filter((item) => item.catalog_section === section);
  const sources = new Map(catalog.sources.map((source) => [source.id, source]));
  return {
    entries: approaches.length,
    organizations: new Set(approaches.map((item) => item.company_id)).size,
    sources: new Set(approaches.flatMap((item) => item.source_ids).map((id) => sources.get(id)?.canonical_url ?? sources.get(id)?.url)).size,
  };
}

export interface Catalog {
  readonly schema_version: number;
  readonly approaches: readonly Approach[];
  readonly claims: readonly Claim[];
  readonly sources: readonly Source[];
  readonly companies: readonly Company[];
}

function fail(message: string): never {
  throw new Error(`${CATALOG_FILE}: ${message}`);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/**
 * Check the structural contract the website depends on and return a typed catalog.
 * An unresolved reference names the record and the claim path that holds it.
 */
export function validateCatalog(value: unknown): Catalog {
  if (!isRecord(value)) fail('the catalog must be a JSON object.');
  if (value.schema_version !== CATALOG_SCHEMA_VERSION) {
    fail(
      `schema_version must be ${CATALOG_SCHEMA_VERSION}, ` +
        `found ${JSON.stringify(value.schema_version)}.`,
    );
  }
  for (const key of ['approaches', 'claims', 'sources', 'companies']) {
    if (!Array.isArray(value[key])) fail(`${key} must be an array.`);
  }
  const catalog = value as unknown as Catalog;

  const companies = new Map<string, Company>();
  const companyNames = new Set<string>();
  for (const company of catalog.companies) {
    if (!isRecord(company)) fail('every company must be an object.');
    if (companies.has(company.id)) fail(`company "${company.id}" is declared more than once.`);
    if (companyNames.has(company.name)) {
      fail(`company name "${company.name}" is declared more than once.`);
    }
    companies.set(company.id, company);
    companyNames.add(company.name);
  }

  const claims = new Map<string, Claim>();
  for (const claim of catalog.claims) {
    if (claims.has(claim.id)) fail(`claim "${claim.id}" is declared more than once.`);
    claims.set(claim.id, claim);
  }
  const sources = new Map<string, Source>();
  for (const source of catalog.sources) {
    if (sources.has(source.id)) fail(`source "${source.id}" is declared more than once.`);
    sources.set(source.id, source);
  }
  const approaches = new Set<string>();
  for (const approach of catalog.approaches) {
    if (approaches.has(approach.id)) fail(`approach "${approach.id}" is declared more than once.`);
    approaches.add(approach.id);
  }

  const usedCompanies = new Set<string>();
  for (const approach of catalog.approaches) {
    if (approach.catalog_section !== catalogSection(approach.approach_type)) {
      fail(`approach "${approach.id}" has inconsistent catalog_section.`);
    }
    const company = companies.get(approach.company_id);
    if (!company) {
      fail(`approach "${approach.id}" lists unknown company "${approach.company_id}".`);
    }
    if (company.name !== approach.company) {
      fail(
        `approach "${approach.id}" names company "${approach.company}", ` +
          `but company "${company.id}" is "${company.name}".`,
      );
    }
    usedCompanies.add(approach.company_id);
    for (const relationship of approach.relationships ?? []) {
      if (!['built-on', 'component-of', 'related-to'].includes(relationship.type) || relationship.approach_id === approach.id) {
        fail(`approach "${approach.id}" has an invalid relationship target or type.`);
      }
    }
    for (const claimId of approach.claim_ids) {
      const claim = claims.get(claimId);
      if (!claim) fail(`approach "${approach.id}" lists unknown claim "${claimId}".`);
      if (claim.approach_id !== approach.id) {
        fail(
          `claim "${claimId}" (approach "${claim.approach_id}") ` +
            `is listed by approach "${approach.id}".`,
        );
      }
    }
    for (const sourceId of approach.source_ids) {
      if (!sources.has(sourceId)) {
        fail(`approach "${approach.id}" lists unknown source "${sourceId}".`);
      }
    }
    if (approach.page_content) {
      const page = approach.page_content;
      if (page.version !== 1 || !/^\d{4}-\d{2}-\d{2}$/.test(page.reviewed_at)) {
        fail(`approach "${approach.id}" has invalid page_content version or review date.`);
      }
      const fields = new Map(
        approach.claim_ids.map((claimId) => claims.get(claimId)!).map((claim) => [claim.field, claim]),
      );
      const reviewed = new Set(page.source_ids);
      if (page.source_ids.some((sourceId) => !approach.source_ids.includes(sourceId))) {
        fail(`approach "${approach.id}" page_content lists a foreign reviewed source.`);
      }
      const dispositions = [
        ...Object.values(page.questions),
        ...Object.values(page.implementation_fields),
      ];
      for (const disposition of dispositions) {
        if (!['reported', 'unreported', 'not-applicable', 'not-reviewed'].includes(disposition.state)) {
          fail(`approach "${approach.id}" page_content has an invalid review state.`);
        }
        for (const path of disposition.claim_paths) {
          const claim = fields.get(path);
          if (!claim) fail(`approach "${approach.id}" page_content lists unknown claim path "${path}".`);
          if (disposition.state === 'reported' && !claim.evidence.some((item) => item.relation === 'supports' && reviewed.has(item.source_id))) {
            fail(`approach "${approach.id}" page_content claim "${path}" lacks reviewed support.`);
          }
        }
      }
      for (const [path, observation] of Object.entries(page.observations)) {
        if (!fields.has(path)) fail(`approach "${approach.id}" observation "${path}" does not resolve.`);
        if (observation.duplicate_of && !page.observations[observation.duplicate_of]) {
          fail(`approach "${approach.id}" observation "${path}" has a missing duplicate target.`);
        }
      }
    }
  }

  for (const claim of catalog.claims) {
    const where = `claim "${claim.id}" (approach "${claim.approach_id}", field "${claim.field}")`;
    if (!approaches.has(claim.approach_id)) fail(`${where} belongs to an unknown approach.`);
    for (const [index, evidence] of claim.evidence.entries()) {
      if (!sources.has(evidence.source_id)) {
        fail(`${where} cites unknown source "${evidence.source_id}" at evidence.${index}.`);
      }
    }
  }

  for (const source of catalog.sources) {
    if (!approaches.has(source.approach_id)) {
      fail(`source "${source.id}" belongs to unknown approach "${source.approach_id}".`);
    }
  }

  for (const company of catalog.companies) {
    if (!usedCompanies.has(company.id)) {
      fail(`company "${company.id}" is not used by any approach.`);
    }
  }

  return catalog;
}

let cached: Catalog | undefined;

/** Return the validated catalog. The file is read and checked once per build. */
export function loadCatalog(): Catalog {
  cached ??= validateCatalog(JSON.parse(catalogText) as unknown);
  return cached;
}

/** Index the claims of one approach by claim identifier. */
export function claimsById(catalog: Catalog): Map<string, Claim> {
  return new Map(catalog.claims.map((claim) => [claim.id, claim]));
}

/** Index the sources by source identifier. */
export function sourcesById(catalog: Catalog): Map<string, Source> {
  return new Map(catalog.sources.map((source) => [source.id, source]));
}

/** Return one approach. An unknown identifier is an error, never an empty page. */
export function requireApproach(catalog: Catalog, id: string): Approach {
  const approach = catalog.approaches.find((item) => item.id === id);
  if (!approach) fail(`approach "${id}" is not in the catalog.`);
  return approach;
}

/** Order the catalog the way the directory reads: company, then implementation. */
export function sortedApproaches(catalog: Catalog): Approach[] {
  return [...catalog.approaches].sort(
    (a, b) =>
      a.company.toLowerCase().localeCompare(b.company.toLowerCase()) ||
      a.agent_name.toLowerCase().localeCompare(b.agent_name.toLowerCase()) ||
      a.id.localeCompare(b.id),
  );
}
