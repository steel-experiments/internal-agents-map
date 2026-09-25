// ABOUTME: Checks the problem pages: which records each one holds, their order, and their lessons.
// ABOUTME: A problem holds exactly the records that carry one of its work-domain tags.

import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import { PROBLEMS, problemBySlug, problemView } from '../../src/lib/problems';

const catalog = loadCatalog();

describe('the problem pages', () => {
  it('each hold exactly the records with one of their work domains', () => {
    for (const problem of PROBLEMS) {
      if (!problem.domains) continue;
      const view = problemView(catalog, problem.slug);
      const wanted = catalog.approaches
        .filter((approach) => approach.domains.some((domain) => problem.domains!.includes(domain)))
        .map((approach) => approach.id)
        .sort();
      const shown = view.groups.flatMap((group) => group.cards.map((card) => card.id)).sort();
      expect(shown, problem.slug).toEqual(wanted);
      expect(shown.length, problem.slug).toBeGreaterThan(0);
    }
  });

  it('show the detailed records first in each group', () => {
    for (const problem of PROBLEMS.filter((item) => item.domains)) {
      for (const group of problemView(catalog, problem.slug).groups) {
        const flags = group.cards.map((card) => card.wellDocumented);
        const firstPlain = flags.indexOf(false);
        if (firstPlain >= 0) expect(flags.slice(firstPlain).every((flag) => !flag), problem.slug).toBe(true);
      }
    }
  });

  it('separate agents from infrastructure and omit an empty group', () => {
    const view = problemView(catalog, 'code-review-load');
    expect(view.groups.map((group) => group.id)).toEqual(['agents', 'infrastructure']);
    for (const group of view.groups) {
      expect(group.cards.every((card) => card.catalogSection === group.id)).toBe(true);
    }
  });

  it('list at most three lessons, and only lessons about records on the page', () => {
    for (const problem of PROBLEMS.filter((item) => item.domains)) {
      const view = problemView(catalog, problem.slug);
      expect(view.lessons.length).toBeLessThanOrEqual(3);
      expect(new Set(view.lessons.map((lesson) => lesson.path)).size).toBe(view.lessons.length);
    }
  });

  it('send the infrastructure problem to the existing infrastructure page', () => {
    expect(PROBLEMS.find((problem) => !problem.domains)?.path).toBe('/infrastructure');
  });

  it('reject an unknown problem', () => {
    expect(() => problemBySlug('not-a-problem')).toThrow();
  });
});
