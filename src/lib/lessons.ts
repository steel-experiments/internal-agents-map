// ABOUTME: Reads the authored lessons and turns their metadata into a reading model.
// ABOUTME: Pages, the entry view, the route list, and the exports all use it.

import { loadCatalog, type Catalog } from './catalog';
import { canonicalUrl, entryPath, lessonPath, lessonsIndexPath } from './routes';

/** One numbered source at the end of a lesson. */
export interface LessonSourceView {
  readonly id: string;
  /** The anchor the citations in the body point to. */
  readonly anchor: string;
  readonly title: string;
  readonly url: string;
  readonly note: string;
}

/** A link from a lesson to the entry page of an implementation it examines. */
export interface LessonCatalogLink {
  readonly id: string;
  readonly path: string;
  readonly label: string;
}

export interface LessonView {
  readonly slug: string;
  readonly path: string;
  readonly title: string;
  readonly description: string;
  readonly eyebrow: string;
  readonly lede: string;
  readonly summary: string;
  readonly readingTime: string;
  readonly order: number;
  readonly publishedAt: string;
  readonly updatedAt: string | null;
  /** The date a reader sees: the update date when one exists. */
  readonly displayDate: string;
  readonly relatedAgentIds: readonly string[];
  readonly sources: readonly LessonSourceView[];
}

interface LessonFrontmatter {
  readonly title: string;
  readonly description: string;
  readonly eyebrow: string;
  readonly lede: string;
  readonly summary: string;
  readonly readingTime: string;
  readonly order: number;
  readonly publishedAt: string;
  readonly updatedAt?: string;
  readonly relatedAgentIds: readonly string[];
  readonly sources: ReadonlyArray<{
    readonly id: string;
    readonly title: string;
    readonly url: string;
    readonly note: string;
  }>;
}

interface LessonModule {
  readonly frontmatter: LessonFrontmatter;
  /** The Markdown body of the file, without its metadata block. */
  rawContent(): string;
}

const modules = import.meta.glob<LessonModule>('../content/lessons/*.md', { eager: true });

function slugOf(file: string): string {
  const name = file.split('/').pop() ?? file;
  return name.replace(/\.md$/, '');
}

function lessonView(slug: string, data: LessonFrontmatter): LessonView {
  return {
    slug,
    path: lessonPath(slug),
    title: data.title,
    description: data.description,
    eyebrow: data.eyebrow,
    lede: data.lede,
    summary: data.summary,
    readingTime: data.readingTime,
    order: data.order,
    publishedAt: data.publishedAt,
    updatedAt: data.updatedAt ?? null,
    displayDate: data.updatedAt ?? data.publishedAt,
    relatedAgentIds: data.relatedAgentIds,
    sources: data.sources.map((source) => ({
      id: source.id,
      anchor: `source-${source.id}`,
      title: source.title,
      url: source.url,
      note: source.note,
    })),
  };
}

/**
 * Reject a lesson that points at an implementation the catalog does not hold.
 * The message names the lesson and the identifier, so the fix is obvious.
 */
export function assertRelatedAgentIds(
  lessons: readonly LessonView[],
  approachIds: ReadonlySet<string>,
): void {
  for (const lesson of lessons) {
    for (const id of lesson.relatedAgentIds) {
      if (!approachIds.has(id)) {
        throw new Error(`lesson "${lesson.slug}" lists unknown relatedAgentIds "${id}".`);
      }
    }
  }
}

/** Reject two lessons that claim the same position in the reading order. */
function assertUniqueOrder(lessons: readonly LessonView[]): void {
  const seen = new Map<number, string>();
  for (const lesson of lessons) {
    const other = seen.get(lesson.order);
    if (other) {
      throw new Error(`lessons "${other}" and "${lesson.slug}" both use order ${lesson.order}.`);
    }
    seen.set(lesson.order, lesson.slug);
  }
}

let cached: LessonView[] | undefined;

/** Every lesson, in reading order. The metadata is checked once per build. */
export function lessonViews(): readonly LessonView[] {
  if (!cached) {
    const lessons = Object.entries(modules)
      .map(([file, module]) => lessonView(slugOf(file), module.frontmatter))
      .sort((a, b) => a.order - b.order);
    assertUniqueOrder(lessons);
    assertRelatedAgentIds(lessons, new Set(loadCatalog().approaches.map((a) => a.id)));
    cached = lessons;
  }
  return cached;
}

/** One lesson. An unknown slug is an error, never an empty page. */
export function lessonViewBySlug(slug: string): LessonView {
  const lesson = lessonViews().find((item) => item.slug === slug);
  if (!lesson) throw new Error(`lesson "${slug}" is not in the lessons collection.`);
  return lesson;
}

/** The lessons that examine one implementation, in reading order. */
export function lessonsForApproach(approachId: string): Array<{
  slug: string;
  path: string;
  title: string;
}> {
  return lessonViews()
    .filter((lesson) => lesson.relatedAgentIds.includes(approachId))
    .map((lesson) => ({ slug: lesson.slug, path: lesson.path, title: lesson.title }));
}

/** The lesson a reader reaches next. The last lesson returns to the first. */
export function nextLesson(slug: string): { lesson: LessonView; isFirst: boolean } {
  const lessons = lessonViews();
  const index = lessons.findIndex((item) => item.slug === slug);
  if (index < 0) throw new Error(`lesson "${slug}" is not in the lessons collection.`);
  const next = lessons[(index + 1) % lessons.length]!;
  return { lesson: next, isFirst: index === lessons.length - 1 };
}

/** The entry pages a lesson links to, labelled with the company name. */
export function lessonCatalogLinks(catalog: Catalog, lesson: LessonView): LessonCatalogLink[] {
  return lesson.relatedAgentIds.map((id) => {
    const approach = catalog.approaches.find((item) => item.id === id);
    if (!approach) throw new Error(`lesson "${lesson.slug}" lists unknown relatedAgentIds "${id}".`);
    return { id, path: entryPath(id), label: `${approach.company} in the catalog` };
  });
}

/** The Markdown body of a lesson, as the author wrote it. */
export function lessonBody(slug: string): string {
  const entry = Object.entries(modules).find(([file]) => slugOf(file) === slug);
  if (!entry) throw new Error(`lesson "${slug}" is not in the lessons collection.`);
  return entry[1].rawContent();
}

/** Write a calendar date the way the lessons show it, such as `11 September 2026`. */
export function longDate(date: string): string {
  return new Intl.DateTimeFormat('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(`${date}T00:00:00Z`));
}

const ENTITIES: Record<string, string> = {
  '&amp;': '&',
  '&lt;': '<',
  '&gt;': '>',
  '&quot;': '"',
  '&#x27;': "'",
  '&nbsp;': ' ',
};

/**
 * Turn one authored diagram or inline block into plain text.
 * Links and bold text keep their Markdown form; decoration is removed.
 */
export function htmlToText(html: string): string {
  const withoutDecoration = html.replace(
    /<([a-z]+)[^>]*aria-hidden="true"[^>]*>[\s\S]*?<\/\1>/g,
    '',
  );
  const withMarkdown = withoutDecoration
    .replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g, '[$2]($1) ')
    .replace(/<strong[^>]*>([\s\S]*?)<\/strong>/g, '**$1** ')
    // Inline labels lose their visual spacing when the tags go away.
    .replace(/<\/(span|small|em|time)>/g, ' ');
  const blocks = withMarkdown
    .replace(/<\/(div|p|figcaption|figure|li|ol|ul|h[1-6])>/g, '\n\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&[a-z#0-9]+;/gi, (entity) => ENTITIES[entity] ?? entity)
    .split('\n\n')
    .map((block) => block.replace(/\s+/g, ' ').trim())
    .filter((block) => block.length > 0);
  return blocks.join('\n\n');
}

/**
 * Turn the Markdown body of a lesson into the text of its export.
 * The layout elements are removed; prose, citations, and diagram text remain.
 */
export function lessonBodyMarkdown(lesson: LessonView): string {
  const base = canonicalUrl(lesson.path);
  return lessonBody(lesson.slug)
    .replace(/^<\/?section[^>]*>\s*$/gm, '')
    .replace(/<blockquote[\s\S]*?<\/blockquote>/g, (block) => `> ${htmlToText(block)}`)
    .replace(/<figure[\s\S]*?<\/figure>/g, (block) => htmlToText(block))
    .replace(/<p[\s\S]*?<\/p>/g, (block) => htmlToText(block))
    .replace(/\]\(#/g, `](${base}#`)
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/** The complete Markdown representation of one lesson. */
export function lessonMarkdown(catalog: Catalog, lesson: LessonView): string {
  const lessonsUrl = canonicalUrl(lessonsIndexPath());
  const next = nextLesson(lesson.slug);
  const dates = lesson.updatedAt
    ? `${longDate(lesson.publishedAt)} · Updated ${longDate(lesson.updatedAt)} · ${lesson.readingTime}`
    : `${longDate(lesson.publishedAt)} · ${lesson.readingTime}`;
  const sources = lesson.sources.map(
    (source, index) => `${index + 1}. [${source.title}](${source.url}) ${source.note}`,
  );
  const catalogLinks = lessonCatalogLinks(catalog, lesson).map(
    (link) => `[${link.label}](${canonicalUrl(link.path)})`,
  );
  return [
    `Source: ${canonicalUrl(lesson.path)}`,
    `[← Lessons](${lessonsUrl})`,
    lesson.eyebrow,
    `# ${lesson.title}`,
    lesson.lede,
    dates,
    lessonBodyMarkdown(lesson),
    `## ${lesson.sources.length === 1 ? 'Source' : 'Sources'}`,
    sources.join('\n'),
    '### Related items',
    catalogLinks.join(' '),
    `[All lessons](${lessonsUrl}) [${next.isFirst ? 'Read' : 'Next'}: ${next.lesson.title} →](${canonicalUrl(next.lesson.path)})`,
  ].join('\n\n');
}

/** A lesson's subject without its place in the sequence: "01 / Run limits" reads "Run limits". */
export function lessonTopic(lesson: LessonView): string {
  return lesson.eyebrow.replace(/^\d+\s*\/\s*/, '');
}

/** The heading a lesson wears in a list: its subject, then the question it asks. */
export function lessonPreviewTitle(lesson: LessonView): string {
  return `${lessonTopic(lesson)}: ${lesson.title}`;
}

/** The companies a lesson reads, in the order the lesson lists them. */
export function lessonCompanies(catalog: Catalog, lesson: LessonView): string[] {
  return lessonCatalogLinks(catalog, lesson).map((link) => link.label.replace(' in the catalog', ''));
}

/** The Markdown blocks that describe every lesson on the index. */
export function lessonPreviewsMarkdown(catalog: Catalog): string[] {
  return lessonViews().flatMap((lesson) => [
    `## [${lessonPreviewTitle(lesson)}](${canonicalUrl(lesson.path)})`,
    lesson.summary,
    `${lessonCompanies(catalog, lesson).join(' · ')} ${lesson.readingTime}`,
  ]);
}
