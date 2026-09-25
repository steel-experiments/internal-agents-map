// ABOUTME: The card inputs of the section, guide, problem, and lesson pages, read by page and endpoint alike.
// ABOUTME: Every value is a heading or description the page already shows.

import {
  DEFINITIONS_DESCRIPTION,
  DEFINITIONS_HEADING,
  METHODOLOGY_DESCRIPTION,
  METHODOLOGY_HEADING,
  LESSONS_DESCRIPTION,
  LESSONS_HEADING,
} from './guide-content';
import { loadCatalog } from './catalog';
import { longDate, type LessonView } from './lessons';
import { SITE_DESCRIPTION, SITE_NAME } from './metadata';
import type { ProblemView } from './problems';
import { mosaicLogos, sectionCard, type OgSectionCard } from './og';

/** The infrastructure directory shares its heading and description with the card. */
export const INFRASTRUCTURE_HEADING = 'Infrastructure companies build to support their agents.';
export const INFRASTRUCTURE_DESCRIPTION =
  'Source-backed research on platforms, runtimes, and components companies use to enable internal agents.';

/** A section card whose front card shows the company logos, in an order its title sets. */
function mosaicCard(options: { eyebrow: string | null; title: string; description: string; date?: string | null }): OgSectionCard {
  return sectionCard({ ...options, logos: mosaicLogos(loadCatalog(), options.title) });
}

/** The card of the home page, drawn to /og.png. */
export const HOME_CARD: OgSectionCard = mosaicCard({ eyebrow: null, title: SITE_NAME, description: SITE_DESCRIPTION });

/** Keyed by the last path segment, which is also the file name under /og/. */
export const SECTION_CARDS: Readonly<Record<string, OgSectionCard>> = {
  infrastructure: mosaicCard({ eyebrow: 'Infrastructure', title: INFRASTRUCTURE_HEADING, description: INFRASTRUCTURE_DESCRIPTION }),
  definitions: mosaicCard({ eyebrow: 'Definitions', title: DEFINITIONS_HEADING, description: DEFINITIONS_DESCRIPTION }),
  methodology: mosaicCard({ eyebrow: 'Methodology', title: METHODOLOGY_HEADING, description: METHODOLOGY_DESCRIPTION }),
  lessons: mosaicCard({ eyebrow: 'Lessons', title: LESSONS_HEADING, description: LESSONS_DESCRIPTION }),
};

/** A lesson card carries its publication date beside the eyebrow. */
export function lessonCard(lesson: LessonView): OgSectionCard {
  return mosaicCard({ eyebrow: 'Lesson', title: lesson.title, description: lesson.description, date: longDate(lesson.publishedAt) });
}

/** A problem card names the problem and what a reader can compare on its page. */
export function problemCard(view: ProblemView): OgSectionCard {
  return mosaicCard({ eyebrow: 'Problem', title: view.problem.heading, description: view.problem.compare });
}
