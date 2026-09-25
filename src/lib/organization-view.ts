// ABOUTME: Derives company indexes from catalog membership and authored relationships.
// ABOUTME: HTML and Markdown share these groups; no company research is invented here.
import { type Catalog } from './catalog';
import { companyView, requireCompany } from './companies';
import { directoryCards, type DirectoryCard } from './entry-view';
import { organizationPath, canonicalUrl } from './routes';
import { outboundUrl } from './outbound';

interface Connection {
  readonly from: DirectoryCard;
  readonly to: DirectoryCard;
  readonly label: string;
  readonly type: string;
}

const RELATION_LABELS: Readonly<Record<string, string>> = {
  'built-on': 'Built on',
  'component-of': 'Component of',
  'related-to': 'Related implementation',
};

/** Resolve one populated company index without inferring relationships from membership. */
export function organizationView(catalog: Catalog, id: string) {
  const company = requireCompany(catalog, id);
  const members = catalog.approaches.filter((entry) => entry.company_id === id);
  if (!members.length) throw new Error(`Company "${id}" has no catalog records.`);
  const ids = new Set(members.map((entry) => entry.id));
  const cards = directoryCards(catalog).filter((card) => ids.has(card.id));
  const byId = new Map(cards.map((card) => [card.id, card]));
  const seen = new Set<string>();
  const connections: Connection[] = [];
  for (const card of cards) {
    const entry = members.find((member) => member.id === card.id)!;
    for (const relation of entry.relationships ?? []) {
      if (!ids.has(relation.approach_id)) continue;
      const endpoints = [entry.id, relation.approach_id];
      // Only related-to is symmetric; reversing a dependency changes its meaning.
      if (relation.type === 'related-to') endpoints.sort();
      const key = [relation.type, ...endpoints].join(':');
      if (seen.has(key)) continue;
      seen.add(key);
      const label = RELATION_LABELS[relation.type];
      if (!label) throw new Error(`Unknown relationship "${relation.type}".`);
      connections.push({ from: card, to: byId.get(relation.approach_id)!, label, type: relation.type });
    }
  }
  const groups = [
    { id: 'agents', label: 'Agents', cards: cards.filter((card) => card.catalogSection === 'agents') },
    { id: 'infrastructure', label: 'Infrastructure', cards: cards.filter((card) => card.catalogSection === 'infrastructure') },
  ].filter((group) => group.cards.length);
  return {
    company: companyView(catalog, id),
    homepage: company.homepage,
    websiteUrl: outboundUrl(company.homepage, 'organization-profile'),
    websiteLabel: new URL(company.homepage).hostname.replace(/^www\./, ''),
    path: organizationPath(id),
    groups,
    connections,
  };
}

const escape = (value: string) => value.replace(/([\\[\]])/g, '\\$1');
const link = (name: string, path: string) => `[${escape(name)}](${canonicalUrl(path)})`;

/** Publish exactly the record previews and connections of the HTML index. */
export function organizationMarkdown(catalog: Catalog, id: string): string {
  const view = organizationView(catalog, id);
  const lines = [
    `Source: ${canonicalUrl(view.path)}`, '',
    `# ${view.company.name}`, '',
    `Website: [${view.websiteLabel}](${view.homepage})`, '',
  ];
  for (const group of view.groups) {
    lines.push(`## ${group.label}`, '');
    for (const card of group.cards) {
      const tags = [card.approachTypeLabel, ...card.domains.map((domain) => domain.label)];
      lines.push(
        `### ${link(`${card.company}'s ${card.agentName}`, card.path)}`, '',
        card.excerpt, '', tags.join(' · '), '',
      );
    }
  }
  if (view.connections.length) {
    lines.push('## Connections', '');
    for (const connection of view.connections) {
      lines.push(`- ${link(connection.from.agentName, connection.from.path)} — ${connection.label}: ${link(connection.to.agentName, connection.to.path)}`);
    }
    lines.push('');
  }
  return lines.join('\n');
}
