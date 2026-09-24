// ABOUTME: Checks that every lesson loads, points at real entries, and keeps its sources.
// ABOUTME: It also checks the clean paths that the discovery files and the manifest read.

import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import { contentPaths } from '../../src/lib/content-routes';
import {
  assertRelatedAgentIds,
  htmlToText,
  nextLesson,
  lessonBody,
  lessonCatalogLinks,
  lessonMarkdown,
  lessonViewBySlug,
  lessonViews,
  lessonsForApproach,
  type LessonView,
} from '../../src/lib/lessons';
import { entryPath, guidePath, lessonPath, lessonsIndexPath } from '../../src/lib/routes';

const catalog = loadCatalog();
const lessons = lessonViews();

const SLUGS = [
  'stop-a-run',
  'review-noise',
  'split-the-work',
  'work-can-continue',
  'load-tools',
  'steps-without-a-model',
  'test-on-your-work',
];

describe('the lessons collection', () => {
  it('loads every published lesson in reading order', () => {
    expect(lessons.map((lesson) => lesson.slug)).toEqual(SLUGS);
    expect(lessons.map((lesson) => lesson.order)).toEqual([1, 2, 3, 4, 5, 6, 7]);
  });

  it('gives every lesson the metadata a page needs', () => {
    for (const lesson of lessons) {
      expect(lesson.title.length).toBeGreaterThan(0);
      expect(lesson.description.length).toBeGreaterThan(0);
      expect(lesson.lede.length).toBeGreaterThan(0);
      expect(lesson.summary.length).toBeGreaterThan(0);
      expect(lesson.publishedAt).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(lesson.path).toBe(lessonPath(lesson.slug));
      expect(lesson.sources.length).toBeGreaterThan(0);
    }
  });

  it('resolves every related implementation to a catalog entry', () => {
    const ids = new Set(catalog.approaches.map((approach) => approach.id));
    for (const lesson of lessons) {
      expect(lesson.relatedAgentIds.length).toBeGreaterThan(0);
      for (const id of lesson.relatedAgentIds) expect(ids.has(id)).toBe(true);
      for (const link of lessonCatalogLinks(catalog, lesson)) {
        expect(link.path).toBe(entryPath(link.id));
        expect(link.label.endsWith(' in the catalog')).toBe(true);
      }
    }
  });

  it('names the lesson and the identifier when a related implementation is unknown', () => {
    const broken = { ...lessons[0]!, slug: 'a-test-lesson', relatedAgentIds: ['no-such-agent'] };
    expect(() => assertRelatedAgentIds([broken as LessonView], new Set(['stripe-minions']))).toThrow(
      'lesson "a-test-lesson" lists unknown relatedAgentIds "no-such-agent".',
    );
  });

  it('cites only sources the lesson declares', () => {
    for (const lesson of lessons) {
      const declared = new Set(lesson.sources.map((source) => source.anchor));
      const cited = [...lessonBody(lesson.slug).matchAll(/#(source-[a-z0-9-]+)/g)].map(
        (match) => match[1]!,
      );
      expect(cited.length).toBeGreaterThan(0);
      for (const anchor of cited) expect(declared.has(anchor)).toBe(true);
    }
  });

  it('reads on from the last lesson to the first', () => {
    expect(nextLesson('stop-a-run')).toMatchObject({ isFirst: false });
    expect(nextLesson('stop-a-run').lesson.slug).toBe('review-noise');
    const wrap = nextLesson('test-on-your-work');
    expect(wrap.isFirst).toBe(true);
    expect(wrap.lesson.slug).toBe('stop-a-run');
  });
});

describe('related reading', () => {
  it('finds the lessons that examine one implementation', () => {
    expect(lessonsForApproach('stripe-minions').map((lesson) => lesson.slug)).toEqual([
      'stop-a-run',
      'steps-without-a-model',
    ]);
    expect(lessonsForApproach('airbnb-airchat')).toEqual([]);
  });

  it('links to the lesson by its clean path', () => {
    for (const lesson of lessonsForApproach('uber-ureview')) {
      expect(lesson.path).toBe(lessonPath(lesson.slug));
      expect(lesson.title).toBe(lessonViewBySlug(lesson.slug).title);
    }
  });
});

describe('the Markdown export of a lesson', () => {
  const lesson = lessonViewBySlug('stop-a-run');
  const markdown = lessonMarkdown(catalog, lesson);

  it('keeps the citations, the diagram text, and the sources', () => {
    expect(markdown).toContain('Source: https://internal-agents.com/lessons/stop-a-run');
    expect(markdown).toContain('[[1]](https://internal-agents.com/lessons/stop-a-run#source-stripe)');
    expect(markdown).toContain(
      '**Budget exhausted** Stop and return the current work, failed checks, and reason for stopping.',
    );
    expect(markdown).toContain(
      'Our proposed control flow. A passing check still leaves any required human approval in place.',
    );
    for (const source of lesson.sources) expect(markdown).toContain(source.url);
  });

  it('sends the catalog links to the entry pages', () => {
    expect(markdown).toContain(
      '[Stripe in the catalog](https://internal-agents.com/agents/stripe-minions)',
    );
    expect(markdown).not.toContain('/index.html#');
  });

  it('leaves no markup in the text', () => {
    expect(markdown).not.toMatch(/<[a-z]+[^>]*>/);
  });
});

describe('the diagram text', () => {
  it('keeps bold labels and links and removes decoration', () => {
    const html =
      '<figure><div><span>01</span><strong>Attempt</strong><small>Make a change</small></div>' +
      '<span aria-hidden="true">→</span>' +
      '<figcaption>Our <a href="/x">illustration</a>.</figcaption></figure>';
    expect(htmlToText(html)).toBe('01 **Attempt** Make a change\n\nOur [illustration](/x) .');
  });
});

describe('the content routes', () => {
  it('lists the guides, the lessons index, and every lesson', async () => {
    const paths = await contentPaths();
    expect(paths).toEqual([
      '/infrastructure',
      guidePath('definitions'),
      guidePath('methodology'),
      lessonsIndexPath(),
      ...SLUGS.map((slug) => lessonPath(slug)),
    ]);
    expect(paths).toHaveLength(11);
    expect(new Set(paths).size).toBe(paths.length);
  });
});
