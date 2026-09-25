// ABOUTME: Checks that the reading model keeps evidence roles, caveats, and anchors.
// ABOUTME: The three difficult entries of the plan are covered case by case.

import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import {
  CARD_SUMMARY_LIMIT,
  directoryCards,
  entryView,
  pageProfile,
  type ClaimView,
} from '../../src/lib/entry-view';

const catalog = loadCatalog();

function caveat(claim: ClaimView, label: string): string {
  const found = claim.caveats.find((item) => item.label === label);
  if (!found) throw new Error(`claim "${claim.id}" has no ${label} caveat.`);
  return found.value;
}

describe('every entry', () => {
  it('places every claim of the record in a section', () => {
    for (const approach of catalog.approaches) {
      const entry = entryView(catalog, approach.id);
      const placed = new Set([
        ...(entry.summary ? [entry.summary.id] : []),
        ...entry.workflowClaims.map((claim) => claim.id),
        ...entry.mechanismClaims.map((claim) => claim.id),
        ...entry.validationClaims.map((claim) => claim.id),
        ...entry.supervisionClaims.map((claim) => claim.id),
        ...entry.architectureClaims.map((claim) => claim.id),
        ...entry.metricClaims.map((claim) => claim.id),
        ...entry.resultStatementClaims.map((claim) => claim.id),
        ...entry.lessonClaims.map((claim) => claim.id),
        ...entry.otherClaims.map((claim) => claim.id),
        ...entry.researchOnlyClaims.map((claim) => claim.id),
      ]);
      expect(placed.size).toBe(approach.claim_ids.length);
      expect([...placed].sort()).toEqual([...approach.claim_ids].sort());
    }
  });

  it('keeps claim and source anchors', () => {
    for (const approach of catalog.approaches) {
      const entry = entryView(catalog, approach.id);
      for (const claim of entry.claims) expect(claim.anchor).toBe(`claim-${claim.id}`);
      for (const source of entry.sources) expect(source.anchor).toBe(`source-${source.id}`);
    }
  });

  it('numbers citations from the source list of the record', () => {
    for (const approach of catalog.approaches) {
      const entry = entryView(catalog, approach.id);
      expect(entry.sources.map((source) => source.number)).toEqual(
        entry.sources.map((_, index) => index + 1),
      );
      const numbers = new Map(entry.sources.map((source) => [source.id, source.number]));
      for (const claim of entry.claims) {
        for (const citation of claim.citations) {
          expect(citation.number).toBe(numbers.get(citation.sourceId));
        }
      }
    }
  });

  it('keeps the three evidence roles apart', () => {
    for (const approach of catalog.approaches) {
      const entry = entryView(catalog, approach.id);
      for (const claim of entry.claims) {
        expect(claim.supporting.length + claim.contextualizing.length + claim.contradicting.length)
          .toBe(claim.citations.length);
        for (const citation of claim.supporting) expect(citation.relation).toBe('supports');
        for (const citation of claim.contextualizing) expect(citation.relation).toBe('contextualizes');
        for (const citation of claim.contradicting) expect(citation.relation).toBe('contradicts');
      }
    }
  });

  it('keeps the research fields of every metric in the ledger', () => {
    for (const approach of catalog.approaches) {
      for (const claim of entryView(catalog, approach.id).metricClaims) {
        if (!claim.isMetric) continue;
        expect(claim.metadata.map((item) => item.label)).toEqual([
          'Reported by',
          'Scope',
          'Denominator',
          'Method',
          'Observation date',
        ]);
      }
    }
  });

  it('leaves an empty research field out of the reading flow', () => {
    for (const approach of catalog.approaches) {
      for (const claim of entryView(catalog, approach.id).claims) {
        for (const caveat of claim.caveats) {
          expect(caveat.value).not.toBe('Unknown');
          expect(caveat.value).not.toBe('Not reported');
          expect(caveat.value.length).toBeGreaterThan(0);
        }
      }
    }
  });

  it('qualifies a figure that has no denominator or no scope', () => {
    const claims = new Map(catalog.claims.map((claim) => [claim.id, claim]));
    for (const approach of catalog.approaches) {
      for (const claim of entryView(catalog, approach.id).claims) {
        const record = claims.get(claim.id)!;
        const missing =
          record.kind === 'metric' &&
          (record.denominator === null ||
            record.denominator === undefined ||
            record.metric_scope === null ||
            record.metric_scope === undefined);
        expect(claim.qualification === null).toBe(!missing);
        if (missing) expect(claim.qualification).toContain('does not report');
      }
    }
  });

  it('names the role of a citation only where the role carries information', () => {
    for (const approach of catalog.approaches) {
      for (const claim of entryView(catalog, approach.id).claims) {
        if (claim.contradicting.length > 0 || claim.contextualizing.length > 0) {
          expect(claim.showCitationRoles).toBe(true);
        } else if (claim.supporting.length === 1) {
          expect(claim.showCitationRoles).toBe(false);
        } else if (claim.supporting.length > 1) {
          expect(claim.showCitationRoles).toBe(true);
        }
      }
    }
  });
});

describe('block-builderbot', () => {
  const entry = entryView(catalog, 'block-builderbot');

  it('describes a ticket-to-code workflow', () => {
    expect(entry.workflowClaims.length).toBeGreaterThan(0);
    const workflow = entry.workflowClaims.map((claim) => claim.text).join(' ');
    expect(workflow).toContain('ticket');
    expect(workflow).toContain('PR');
    expect(entry.invocation.map((item) => item.id)).toContain('event-driven');
  });

  it('attributes the metrics to the company that reported them', () => {
    const headline = entry.metricClaims.find((claim) => claim.field === 'headline_metric');
    expect(headline).toBeDefined();
    expect(caveat(headline!, 'Reported by')).toBe('Block');
    expect(caveat(headline!, 'Denominator')).toContain('All production code changes across Block');
  });

  it('keeps the undefined meaning of an operation beside the operations figure', () => {
    const operations = entry.metricClaims.find((claim) => claim.text.includes('operations per day'));
    expect(operations).toBeDefined();
    expect(caveat(operations!, 'Scope')).toContain('does not define an operation');
  });

  it('is not labelled as supporting infrastructure', () => {
    expect(entry.isSupportingSystem).toBe(false);
    expect(entry.profile.section).toBe('agents');
  });
});

describe('uber-ureview', () => {
  const entry = entryView(catalog, 'uber-ureview');

  it('keeps the weekly and monthly conflict beside the metric', () => {
    const metrics = entry.metricClaims.filter((claim) => claim.text.includes('65,000'));
    expect(metrics.length).toBeGreaterThan(0);
    for (const metric of metrics) {
      expect(metric.text).toMatch(/month/);
      expect(caveat(metric, 'Scope')).toMatch(/conflicts and remains unresolved/);
      expect(caveat(metric, 'Denominator')).toMatch(/monthly|month/);
    }
  });

  it('marks the conflicting source as contradicting, not supporting', () => {
    const headline = entry.metricClaims.find((claim) => claim.field === 'headline_metric');
    expect(headline!.contradicting.length).toBeGreaterThan(0);
    for (const citation of headline!.contradicting) {
      expect(citation.relationLabel).toBe('Contradicts');
      expect(headline!.supporting.map((item) => item.relation)).not.toContain('contradicts');
    }
  });

  it('links the related Uber implementation', () => {
    expect(entry.relatedEntries.map((related) => related.id)).toContain('uber-coding-agent');
  });
});

describe('plaid-internal-mcp-server', () => {
  const entry = entryView(catalog, 'plaid-internal-mcp-server');

  it('is labelled as supporting infrastructure', () => {
    expect(entry.isSupportingSystem).toBe(true);
    expect(entry.approachTypeLabel).toBe('Component');
    expect(entry.profile.section).toBe('infrastructure');
  });

  it('keeps coding-tool adoption apart from server adoption', () => {
    const adoption = entry.metricClaims.filter((claim) => claim.text.includes('80%'));
    expect(adoption.length).toBeGreaterThan(0);
    for (const claim of adoption) {
      expect(caveat(claim, 'Scope')).toContain('separate from internal MCP server adoption');
    }
    const detailed = adoption.find((claim) => claim.field.startsWith('key_metrics.'));
    expect(detailed!.text).toContain('the source does not report internal MCP server adoption');
  });

  it('records no supervision level for the scope it serves', () => {
    expect(entry.operatingModels[0]!.levelLabel).toBe('Level unknown');
    expect(entry.operatingModels[0]!.boundaryLabel).toBe('Unknown');
  });
});

describe('the directory model', () => {
  const cards = directoryCards(catalog);

  it('has one card per approach, ordered by company', () => {
    expect(cards.length).toBe(catalog.approaches.length);
    const companies = cards.map((card) => card.company.toLowerCase());
    expect([...companies]).toEqual([...companies].sort());
  });

  it('names every card by its company and its name, as the palette does', () => {
    for (const card of cards) expect(card.title).toBe(`${card.company} · ${card.agentName}`);
    expect(cards.find((card) => card.id === 'brex-disputes')?.title).toBe('Brex · Dispute preparation agent');
  });

  it('carries a summary and a link for every card', () => {
    for (const card of cards) {
      expect(card.summary.length).toBeGreaterThan(0);
      expect(card.path).toBe(`/agents/${card.id}`);
    }
  });

  it('makes a card searchable by company, name, work, type, supervision, and summary', () => {
    for (const card of cards) {
      expect(card.search).toBe(card.search.toLowerCase());
      expect(card.search).not.toMatch(/\s{2,}/);
      expect(card.search).toContain(card.company.toLowerCase());
      expect(card.search).toContain(card.agentName.toLowerCase());
      expect(card.search).toContain(card.approachType);
      for (const domain of card.domains) expect(card.search).toContain(domain.id);
      for (const boundary of card.boundaries) {
        expect(card.search).toContain(boundary.id);
        if (boundary.level !== null) expect(card.search).toContain(`level ${boundary.level}`);
      }
    }
  });

  it('carries the derived level next to every attention boundary', () => {
    const ureview = cards.find((card) => card.id === 'uber-ureview')!;
    expect(ureview.boundaries).toEqual([{ id: 'work-product-review', label: 'Work-product review', level: 3 }]);
    for (const card of cards) {
      if (card.catalogSection === 'agents') expect(card.boundaries.length).toBeGreaterThan(0);
      else expect(card.boundaries).toEqual([]);
      for (const boundary of card.boundaries) {
        expect(boundary.level === null).toBe(boundary.id === 'unknown');
      }
    }
  });
});

describe('directory card summaries', () => {
  it('shortens a long summary and keeps the whole text for the entry page', () => {
    const card = directoryCards(catalog).find((item) => item.id === 'plaid-internal-mcp-server')!;
    expect(card.summary.length).toBeGreaterThan(CARD_SUMMARY_LIMIT);
    expect(card.excerpt.length).toBeLessThanOrEqual(CARD_SUMMARY_LIMIT + 1);
    expect(card.excerpt.endsWith('…')).toBe(true);
    expect(card.summary.startsWith(card.excerpt.slice(0, 60))).toBe(true);
  });

  it('leaves a short summary unchanged', () => {
    for (const card of directoryCards(catalog)) {
      if (card.summary.length <= CARD_SUMMARY_LIMIT) expect(card.excerpt).toBe(card.summary);
    }
  });
});

describe('collection profiles', () => {
  it('leads infrastructure with architecture and keeps operational scopes in research', () => {
    for (const approach of catalog.approaches.filter((item) => item.catalog_section === 'infrastructure')) {
      const entry = entryView(catalog, approach.id);
      expect(entry.profile.sectionOrder[0]).toBe('implementation');
      expect(entry.profile.workflow).toBe('Documented uses');
      expect(entry.supervisionClaims).toEqual([]);
      for (const claim of entry.claims.filter((claim) => claim.field.startsWith('operating_models.'))) expect(entry.researchOnlyClaims).toContainEqual(claim);
    }
  });
  it('keeps task-performing Horizon and Slack in agents', () => {
    for (const id of ['workos-project-horizon', 'slack-context-system']) expect(entryView(catalog, id).profile.section).toBe('agents');
  });
});

describe('page-content pilot reading model', () => {
  it('covers the whole catalog with explicit workflow roles', () => {
    for (const approach of catalog.approaches) {
      const entry = entryView(catalog, approach.id);
      expect(entry.isPilot, approach.id).toBe(true);
      const workflowReported = entry.coverageQuestions.workflow?.state === 'reported';
      expect(entry.workflowClaims.length > 0, approach.id).toBe(workflowReported);
      if (workflowReported) {
        expect(entry.workflowScope, approach.id).toBeTruthy();
        for (const claim of entry.workflowClaims) expect(claim.displayName, approach.id).toBeTruthy();
      }
    }
    expect(entryView(catalog, 'doordash-code-review').mechanismClaims.map((claim) => claim.field)).toContain('primitives.0');
  });

  it('separates validation, lessons, canonical observations, and aliases', () => {
    expect(entryView(catalog, 'github-qubot').validationClaims.length).toBeGreaterThan(0);
    const notion = entryView(catalog, 'notion-custom-agents');
    expect(notion.aliasObservationClaims.map((claim) => claim.field)).toEqual(['key_metrics.0']);
    expect(notion.canonicalObservationClaims.map((claim) => claim.field)).not.toContain('key_metrics.0');
    const yc = entryView(catalog, 'ycombinator-agent-infra');
    expect(yc.canonicalObservationClaims).toHaveLength(0);
    expect(yc.lessonClaims.length).toBeGreaterThan(0);
  });

  it('leaves no record on the legacy path', () => {
    for (const approach of catalog.approaches) {
      expect(entryView(catalog, approach.id).isPilot, approach.id).toBe(true);
    }
  });
});

describe('the results of an entry', () => {
  /** Claims of a metric field whose normalized kind is not a metric. */
  const statements = catalog.claims.filter(
    (claim) =>
      (claim.field === 'headline_metric' || claim.field.startsWith('key_metrics.')) &&
      claim.kind !== 'metric',
  );
  const grouped = catalog.approaches.map((approach) => entryView(catalog, approach.id));

  it('leaves only metrics under the reported metrics', () => {
    for (const entry of grouped) {
      for (const claim of entry.metricClaims) expect(claim.kind, claim.id).toBe('metric');
    }
  });

  it('keeps every statement of a metric field in the results, under its kind', () => {
    const placed = grouped.flatMap((entry) => entry.resultStatementClaims);
    expect(placed.map((claim) => claim.id).sort()).toEqual(
      statements.map((claim) => claim.id).sort(),
    );
    for (const claim of placed) {
      expect(claim.kind, claim.id).not.toBe('metric');
      expect(claim.kindLabel.length, claim.id).toBeGreaterThan(0);
    }
  });

  it('reads the months-to-days opinion of block-builderbot as an opinion', () => {
    const entry = entryView(catalog, 'block-builderbot');
    const claim = entry.resultStatementClaims.find((item) => item.text.includes('now takes days'));
    expect(claim).toBeDefined();
    expect(claim!.kind).toBe('opinion');
    expect(claim!.kindLabel).toBe('Opinion');
    expect(entry.metricClaims.map((item) => item.id)).not.toContain(claim!.id);
  });
});

describe('pageProfile', () => {
  it('marks each section with the icon its navigation entry draws', () => {
    expect(pageProfile('agents').icon).toBe('layers-two');
    expect(pageProfile('infrastructure').icon).toBe('server');
  });
});
