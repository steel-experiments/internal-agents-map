// ABOUTME: The problems the homepage offers as entry points, and the page view of each one.
// ABOUTME: A problem page holds every record that carries one of its work-domain tags.

import type { Catalog, CatalogSection } from './catalog';
import { WELL_DOCUMENTED_LABEL, documentationOrder } from './documentation';
import { directoryCards, type DirectoryCard } from './entry-view';
import { markdownLink } from './exports';
import { termLabel } from './labels';
import { lessonViews } from './lessons';
import { canonicalUrl, problemPath } from './routes';

export interface Problem {
  /** The link text on the homepage. */
  readonly label: string;
  /** The page path. The infrastructure problem uses the existing infrastructure page. */
  readonly path: string;
  readonly slug: string;
  /** The work domains whose records the page holds. Null when the problem links to another page. */
  readonly domains: readonly string[] | null;
  readonly heading: string;
  /** What a reader can compare across the records of the page. */
  readonly compare: string;
}

function problem(slug: string, label: string, domains: readonly string[], heading: string, compare: string): Problem {
  return { slug, label, path: problemPath(slug), domains, heading, compare };
}

export const PROBLEMS: readonly Problem[] = [
  problem(
    'code-review-load',
    'Reduce code-review load',
    ['code-review'],
    'Reduce code-review load',
    'Compare what each agent comments on, what it can change, and where a person still approves the work.',
  ),
  problem(
    'security-alerts',
    'Triage security alerts',
    ['security'],
    'Triage security alerts',
    'Compare what starts an investigation, which tools and data the agent can use, and who acts on the result.',
  ),
  problem(
    'company-data',
    'Answer questions about company data',
    ['data'],
    'Answer questions about company data',
    'Compare how each system finds the correct data, how it checks its answers, and who can see the results.',
  ),
  problem(
    'operations',
    'Automate an operations workflow',
    ['ops', 'finance-ops'],
    'Automate an operations workflow',
    'Compare which steps use a model, which steps use ordinary code, and where a person approves an action.',
  ),
  {
    slug: 'infrastructure',
    label: 'Build shared agent infrastructure',
    path: '/infrastructure',
    domains: null,
    heading: 'Build shared agent infrastructure',
    compare: '',
  },
];

/** The problems that have a page of their own. */
/** A titled run of cards on the homepage: one problem, or the agents no problem holds. */
export interface CardGroup {
  readonly id: string;
  readonly title: string;
  readonly cards: readonly DirectoryCard[];
}

/** The group that closes the homepage, holding every agent no problem claims. */
export const MORE_AGENTS = { id: 'more-agents', title: 'More agents' } as const;

/**
 * Split the homepage's cards by the problems the site offers. A card joins
 * the first problem whose work domains it carries, so each card is on the page
 * once and keeps its one anchor; the cards no problem claims close the page
 * together. A problem that is its own page, such as infrastructure, holds none.
 */
export function catalogGroups(cards: readonly DirectoryCard[]): CardGroup[] {
  const placed = new Set<string>();
  const groups: CardGroup[] = [];
  for (const problem of PROBLEMS) {
    const domains = problem.domains;
    if (!domains) continue;
    const held = cards.filter(
      (card) => !placed.has(card.id) && card.domains.some((domain) => domains.includes(domain.id)),
    );
    for (const card of held) placed.add(card.id);
    if (held.length > 0) groups.push({ id: problem.slug, title: problem.label, cards: held });
  }
  const rest = cards.filter((card) => !placed.has(card.id));
  if (rest.length > 0) groups.push({ ...MORE_AGENTS, cards: rest });
  return groups;
}

export function problemPages(): Problem[] {
  return PROBLEMS.filter((item) => item.domains !== null);
}

export function problemBySlug(slug: string): Problem {
  const found = problemPages().find((item) => item.slug === slug);
  if (!found) throw new Error(`Problem "${slug}" has no page.`);
  return found;
}

export interface ProblemGroup {
  readonly id: CatalogSection;
  readonly label: string;
  readonly cards: readonly DirectoryCard[];
}

export interface ProblemView {
  readonly problem: Problem;
  /** Which tags select the records, then what to compare across them. */
  readonly intro: string;
  readonly groups: readonly ProblemGroup[];
  readonly lessons: ReadonlyArray<{ readonly path: string; readonly title: string }>;
}

/** The number of lessons a problem page lists. */
const LESSON_LIMIT = 3;

/** The records of one problem, detailed records first, and the lessons that discuss the most of them. */
export function problemView(catalog: Catalog, slug: string): ProblemView {
  const problem = problemBySlug(slug);
  const domains = new Set(problem.domains);
  const cards = documentationOrder(
    directoryCards(catalog).filter((card) => card.domains.some((domain) => domains.has(domain.id))),
  );
  const groups = (
    [
      { id: 'agents', label: 'Agents' },
      { id: 'infrastructure', label: 'Infrastructure' },
    ] as const
  )
    .map((group) => ({ ...group, cards: cards.filter((card) => card.catalogSection === group.id) }))
    .filter((group) => group.cards.length > 0);
  const ids = new Set(cards.map((card) => card.id));
  const lessons = lessonViews()
    .map((lesson) => ({ lesson, overlap: lesson.relatedAgentIds.filter((id) => ids.has(id)).length }))
    .filter((item) => item.overlap > 0)
    .sort((a, b) => b.overlap - a.overlap || a.lesson.order - b.lesson.order)
    .slice(0, LESSON_LIMIT)
    .map(({ lesson }) => ({ path: lesson.path, title: lesson.title }));
  const tags = (problem.domains ?? []).map((domain) => termLabel(domain));
  const intro = `These records have the ${tags.join(' or ')} work-domain tag. ${problem.compare}`;
  return { problem, intro, groups, lessons };
}

/** The Markdown version of a problem page, with the same records and lessons. */
export function problemMarkdown(catalog: Catalog, slug: string): string {
  const view = problemView(catalog, slug);
  const lines = [`Source: ${canonicalUrl(view.problem.path)}`, '', `# ${view.problem.heading}`, '', view.intro, ''];
  for (const group of view.groups) {
    lines.push(`## ${group.label}`, '');
    for (const card of group.cards) {
      const tags = [...(card.typeTag ? [card.typeTag] : []), ...card.domains.map((domain) => domain.label)];
      if (card.wellDocumented) tags.push(WELL_DOCUMENTED_LABEL);
      lines.push(`### ${markdownLink(card.title, canonicalUrl(card.path))}`, '', card.excerpt, '', tags.join(' · '), '');
    }
  }
  if (view.lessons.length > 0) {
    lines.push('## Related lessons', '');
    for (const lesson of view.lessons) lines.push(`- ${markdownLink(lesson.title, canonicalUrl(lesson.path))}`);
    lines.push('');
  }
  return lines.join('\n');
}
