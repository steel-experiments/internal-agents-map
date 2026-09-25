// ABOUTME: Company indexes preserve registry identity, membership and authored direction.
import { describe, expect, it } from 'vitest';
import { recordMarkdown } from '../../src/lib/exports';
import { loadCatalog, type Relationship } from '../../src/lib/catalog';
import { organizationView, organizationMarkdown } from '../../src/lib/organization-view';
import { organizationPath, organizationPaths, routeInventory } from '../../src/lib/routes';
const catalog = loadCatalog();
describe('organization indexes', () => {
  it('groups Airbnb records and publishes matching Markdown', () => {
    const view = organizationView(catalog, 'airbnb');
    expect(view.groups.map((group) => [group.id, group.cards.length])).toEqual([['agents', 2], ['infrastructure', 1]]);
    const markdown = organizationMarkdown(catalog, 'airbnb');
    expect(markdown).toContain('Source: https://internal-agents.com/organizations/airbnb');
    expect(recordMarkdown(catalog, 'airbnb-datako')).toContain('- Company: [Airbnb](https://internal-agents.com/organizations/airbnb)');
    for (const group of view.groups) for (const card of group.cards) {
      expect(markdown).toContain(card.path);
      expect(markdown).toContain(card.excerpt);
      for (const domain of card.domains) expect(markdown).toContain(domain.label);
    }
  });
  it('hides empty groups and does not invent Harvey dependencies', () => {
    expect(organizationView(catalog, 'stripe').groups.map((group) => group.id)).toEqual(['agents']);
    expect(organizationView(catalog, 'databricks').groups.map((group) => group.id)).toEqual(['infrastructure']);
    const harvey = organizationView(catalog, 'harvey');
    expect(harvey.connections).toHaveLength(1);
    expect(harvey.connections[0]?.type).toBe('related-to');
  });
  it('uses safe stable ids and publishes only referenced companies', () => {
    expect(organizationPath('ycombinator')).toBe('/organizations/ycombinator');
    expect(() => organizationPath('../escape')).toThrow();
    expect(() => organizationView(catalog, 'missing')).toThrow();
    const extra = { ...catalog, companies: [...catalog.companies, { id: 'unused', name: 'Unused', homepage: 'https://example.com', logo: null }] };
    expect(organizationPaths(extra)).not.toContain('/organizations/unused');
    expect(() => organizationView(extra, 'unused')).toThrow(/no catalog records/);
    expect(organizationPaths(extra)).toHaveLength(new Set(catalog.approaches.map((entry) => entry.company_id)).size);
    expect(routeInventory(extra).routes['/organizations/airbnb']).toEqual({ html: '/organizations/airbnb.html', markdown: '/organizations/airbnb.md' });
  });
  it('deduplicates symmetric related links, retains directed dependencies and ignores other companies', () => {
    const fixture = { ...catalog, approaches: catalog.approaches.map((entry) => entry.id === 'airbnb-datako' ? { ...entry, relationships: [
      { type: 'built-on', approach_id: 'airbnb-airchat' }, { type: 'built-on', approach_id: 'airbnb-airchat' },
      { type: 'related-to', approach_id: 'airbnb-pascal' }, { type: 'related-to', approach_id: 'harvey-spectre' },
    ] satisfies Relationship[] } : entry.id === 'airbnb-pascal' ? { ...entry, relationships: [{ type: 'related-to', approach_id: 'airbnb-datako' }] satisfies Relationship[] } : { ...entry, relationships: [] }) };
    const connections = organizationView(fixture, 'airbnb').connections;
    expect(connections.filter((item) => item.type === 'related-to')).toHaveLength(1);
    expect(connections.filter((item) => item.type === 'built-on')).toHaveLength(1);
    expect(connections.find((item) => item.type === 'built-on')?.from.id).toBe('airbnb-datako');
  });
});
