// ABOUTME: Checks that the JSON and Markdown exports keep the whole research record.
// ABOUTME: The JSON files must stay byte-identical to the published catalog interface.

import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { loadCatalog, validateCatalog, type Catalog, type Claim } from '../../src/lib/catalog';
import {
  catalogMarkdown,
  compactIndexJson,
  markdownLink,
  recordJson,
  recordMarkdown,
} from '../../src/lib/exports';
import { entryView } from '../../src/lib/entry-view';
import { canonicalUrl, entryPath } from '../../src/lib/routes';

const catalog = loadCatalog();

/** A committed file of the repository, read as the comparison baseline. */
function published(path: string): string {
  return readFileSync(new URL(`../../${path}`, import.meta.url), 'utf8');
}

describe('record JSON', () => {
  it('holds the whole catalog slice of every record, in the catalog format', () => {
    for (const approach of catalog.approaches) {
      const text = recordJson(catalog, approach.id);
      const record = JSON.parse(text) as Catalog;
      expect(record.schema_version, approach.id).toBe(catalog.schema_version);
      expect(record.approaches, approach.id).toEqual([approach]);
      expect(record.claims, approach.id).toEqual(
        approach.claim_ids.map((id) => catalog.claims.find((claim) => claim.id === id)),
      );
      expect(record.sources, approach.id).toEqual(
        approach.source_ids.map((id) => catalog.sources.find((source) => source.id === id)),
      );
      expect(record.companies, approach.id).toEqual([
        catalog.companies.find((company) => company.id === approach.company_id),
      ]);
      // A record is a complete catalog slice, so the catalog validator accepts it.
      expect(() => validateCatalog(record), approach.id).not.toThrow();
      expect(text, approach.id).toBe(`${JSON.stringify(record, null, 2)}\n`);
    }
  });

  it('keeps the whole dataset identical to the committed catalog', () => {
    const raw = published('data/agents.json');
    expect(`${JSON.stringify(catalog, null, 2)}\n`).toBe(raw);
  });

  it('carries the claims and the sources the approach lists, in that order', () => {
    const record = JSON.parse(recordJson(catalog, 'block-builderbot')) as {
      schema_version: number;
      approaches: Array<{ id: string; claim_ids: string[]; source_ids: string[] }>;
      claims: Claim[];
      sources: Array<{ id: string }>;
    };
    const approach = record.approaches[0]!;
    expect(record.schema_version).toBe(catalog.schema_version);
    expect(record.claims.map((claim) => claim.id)).toEqual(approach.claim_ids);
    expect(record.sources.map((source) => source.id)).toEqual(approach.source_ids);
  });
});

describe('compact index', () => {
  const current = JSON.parse(compactIndexJson(catalog)) as {
    schema_version: number;
    approaches: Array<Record<string, unknown>>;
  };

  it('describes every implementation of the catalog, in catalog order', () => {
    expect(current.schema_version).toBe(3);
    expect(current.approaches.map((entry) => entry.id)).toEqual(
      catalog.approaches.map((approach) => approach.id),
    );
    for (const [index, entry] of current.approaches.entries()) {
      const approach = catalog.approaches[index]!;
      expect(entry.company).toBe(approach.company);
      expect(entry.agent_name).toBe(approach.agent_name);
      expect(entry.approach_type).toBe(approach.approach_type);
      expect(entry.domains).toEqual(approach.domains);
      expect(entry.last_reviewed_at).toBe(approach.last_reviewed_at);
    }
  });

  it('points the page URL at the entry page and keeps the export URLs', () => {
    for (const entry of current.approaches) {
      const id = entry.id as string;
      expect(entry.url).toBe(canonicalUrl(entryPath(id)));
      expect(entry.json_url).toBe(canonicalUrl(`${entryPath(id)}.json`));
      expect(entry.markdown_url).toBe(canonicalUrl(`${entryPath(id)}.md`));
    }
  });
});

describe('record Markdown', () => {
  it('holds every claim, every qualification, and every source of the entry', () => {
    for (const approach of catalog.approaches) {
      const markdown = recordMarkdown(catalog, approach.id);
      const view = entryView(catalog, approach.id);
      for (const claim of view.claims) {
        expect(markdown, `${approach.id}: ${claim.id}`).toContain(claim.text.trim());
        expect(markdown, `${approach.id}: ${claim.id}`).toContain(`\`${claim.id}\``);
        for (const caveat of claim.caveats) {
          expect(markdown, `${approach.id}: ${claim.id} ${caveat.label}`).toContain(
            `- ${caveat.label}: ${caveat.value}`,
          );
        }
      }
      for (const source of view.sources) {
        expect(markdown, `${approach.id}: ${source.id}`).toContain(source.url);
        if (source.preservedUrl) {
          expect(markdown, `${approach.id}: ${source.id}`).toContain(source.preservedUrl);
        }
      }
    }
  });

  it('keeps a metric qualification beside the number it belongs to', () => {
    const markdown = recordMarkdown(catalog, 'uber-ureview');
    const metrics = entryView(catalog, 'uber-ureview').metricClaims;
    expect(metrics.length).toBeGreaterThan(0);
    for (const claim of metrics) {
      const position = markdown.indexOf(claim.text.trim());
      const block = markdown.slice(position, markdown.indexOf('\n### ', position + 1));
      for (const caveat of claim.caveats) expect(block).toContain(`- ${caveat.label}:`);
    }
  });

  it('names the page it represents and the relation of every citation', () => {
    const markdown = recordMarkdown(catalog, 'plaid-internal-mcp-server');
    expect(markdown.startsWith(`Source: ${canonicalUrl('/agents/plaid-internal-mcp-server')}\n`)).toBe(
      true,
    );
    expect(markdown).toContain('- Collection: Infrastructure');
    expect(markdown).not.toContain('This entry describes supporting infrastructure');
    for (const relation of entryView(catalog, 'plaid-internal-mcp-server').claims.flatMap(
      (claim) => claim.citations,
    )) {
      expect(markdown).toContain(`${relation.relationLabel} · [${relation.number}]`);
    }
  });

  it('keeps the section of a question the sources leave unanswered, state alone', () => {
    const markdown = recordMarkdown(catalog, 'brex-support-qa');
    const view = entryView(catalog, 'brex-support-qa');
    const sections = [
      [view.profile.validation, 'validation'],
      [view.profile.observations, 'observations'],
      ['Lessons', 'lessons'],
    ] as const;
    for (const [title, key] of sections) {
      expect(view.coverageQuestions[key]?.note, key).toBeNull();
      const section = markdown.split(`## ${title}`)[1] ?? '';
      expect(section.trimStart().startsWith('**Not reported**'), `${key}: ${section.slice(0, 60)}`).toBe(
        true,
      );
    }
  });

  it('exports pilot states and duplicate representations explicitly', () => {
    const notion = recordMarkdown(catalog, 'notion-custom-agents');
    expect(notion).toContain('## Duplicate observation representations');
    expect(notion).toContain('Duplicate of `notion-custom-agents--headline-metric`');
    const yc = recordMarkdown(catalog, 'ycombinator-agent-infra');
    expect(yc).toContain('## Adoption and operating evidence');
    expect(yc).toContain('**observations:** Not reported');
    expect(yc.indexOf('## Lessons')).toBeGreaterThan(yc.indexOf('## Adoption and operating evidence'));
  });
});

describe('lesson attribution in Markdown', () => {
  it('keeps reported opinion and catalog judgment provenance beside lesson text', () => {
    const reported = recordMarkdown(catalog, 'strongdm-software-factory');
    expect(reported).toContain('Opinion · Reported');
    const interpreted = recordMarkdown(catalog, 'sentry-junior');
    expect(interpreted).toContain('Inference · Catalog judgment');
  });
});

describe('catalog Markdown', () => {
  const markdown = catalogMarkdown(catalog) + catalogMarkdown(catalog, 'infrastructure');

  it('holds the text of every claim in the catalog', () => {
    for (const claim of catalog.claims) {
      expect(markdown, claim.id).toContain(claim.text.trim());
    }
  });

  it('holds every implementation and its page address', () => {
    for (const approach of catalog.approaches) {
      expect(markdown, approach.id).toContain(`## ${approach.company} — ${approach.agent_name}`);
      expect(markdown, approach.id).toContain(`Page: ${canonicalUrl(entryPath(approach.id))}`);
    }
  });

  it('counts each collection and never combines platforms into agent totals', () => {
    for (const section of ['agents', 'infrastructure'] as const) {
      const items = catalog.approaches.filter((item) => item.catalog_section === section);
      const text = catalogMarkdown(catalog, section);
      expect(text).toContain(`- ${section === 'agents' ? 'Agents' : 'Infrastructure records'}: ${items.length}`);
      expect(text).toContain(`- Organizations: ${new Set(items.map((item) => item.company_id)).size}`);
      expect(text).toContain(`- Claims: ${items.reduce((sum, item) => sum + item.claim_ids.length, 0)}`);
    }
  });
});

describe('Markdown links', () => {
  it('protects brackets in the text and wraps a URL that needs it', () => {
    expect(markdownLink('A [note]', 'https://example.com/a')).toBe(
      '[A \\[note\\]](https://example.com/a)',
    );
    expect(markdownLink('Title', 'https://example.com/a(b)')).toBe(
      '[Title](<https://example.com/a(b)>)',
    );
  });
});

describe('the qualification of a figure', () => {
  /** Metrics whose record does not report the scope or the denominator. */
  const unqualified = catalog.claims.filter(
    (claim) =>
      claim.kind === 'metric' &&
      (claim.metric_scope === null ||
        claim.metric_scope === undefined ||
        claim.denominator === null ||
        claim.denominator === undefined),
  );

  it('stays with the figure in the entry Markdown', () => {
    let written = 0;
    for (const approach of catalog.approaches) {
      const markdown = recordMarkdown(catalog, approach.id);
      for (const claim of entryView(catalog, approach.id).claims) {
        if (!claim.qualification) continue;
        written += 1;
        expect(markdown, `${approach.id}: ${claim.id}`).toContain(claim.qualification);
      }
    }
    expect(written).toBeGreaterThan(0);
    expect(written).toBe(unqualified.length);
  });

  it('stays with the figure in the catalog Markdown', () => {
    const markdown = catalogMarkdown(catalog);
    for (const approach of catalog.approaches) {
      for (const claim of entryView(catalog, approach.id).claims) {
        if (!claim.qualification) continue;
        expect(markdown, claim.id).toContain(claim.qualification);
      }
    }
  });

  it('keeps the missing denominator of the Brex accuracy figure', () => {
    const markdown = recordMarkdown(catalog, 'brex-agent-platform');
    const claim = entryView(catalog, 'brex-agent-platform').claims.find((item) =>
      item.text.includes('85%'),
    );
    expect(claim!.qualification).toContain('denominator');
    const position = markdown.indexOf(claim!.text.trim());
    const block = markdown.slice(position, markdown.indexOf('\n### ', position + 1));
    expect(block).toContain(claim!.qualification);
  });
});

describe('the results of an entry in Markdown', () => {
  it('renders reviewed observations with the statements of other kinds', () => {
    const markdown = recordMarkdown(catalog, 'ramp-inspect');
    expect(markdown).toContain('## Reported observations');
    expect(markdown).toContain('limited only by model-provider');
  });

  it('names the kind of every statement it groups outside the metrics', () => {
    for (const approach of catalog.approaches) {
      const entry = entryView(catalog, approach.id);
      if (entry.resultStatementClaims.length === 0) continue;
      const markdown = recordMarkdown(catalog, approach.id);
      expect(markdown, approach.id).toContain(
        entry.isPilot ? `## ${entry.profile.observations}` : '## Reported outcomes and statements',
      );
      for (const claim of entry.resultStatementClaims) {
        const position = markdown.indexOf(claim.text.trim());
        const block = markdown.slice(position, markdown.indexOf('\n### ', position + 1));
        expect(block, claim.id).toContain(claim.kindLabel);
      }
    }
  });
});
