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
import { longDate, type LessonView } from './lessons';
import type { ProblemView } from './problems';
import { sectionCard, type OgSectionCard } from './og';

/** The infrastructure directory shares its heading and description with the card. */
export const INFRASTRUCTURE_HEADING = 'Infrastructure companies build to support their agents.';
export const INFRASTRUCTURE_DESCRIPTION =
  'Source-backed research on platforms, runtimes, and components companies use to enable internal agents.';

/** Keyed by the last path segment, which is also the file name under /og/. */
export const SECTION_CARDS: Readonly<Record<string, OgSectionCard>> = {
  infrastructure: sectionCard({ eyebrow: 'Infrastructure', title: INFRASTRUCTURE_HEADING, description: INFRASTRUCTURE_DESCRIPTION }),
  definitions: sectionCard({ eyebrow: 'Definitions', title: DEFINITIONS_HEADING, description: DEFINITIONS_DESCRIPTION }),
  methodology: sectionCard({ eyebrow: 'Methodology', title: METHODOLOGY_HEADING, description: METHODOLOGY_DESCRIPTION }),
  lessons: sectionCard({ eyebrow: 'Lessons', title: LESSONS_HEADING, description: LESSONS_DESCRIPTION }),
};

/** A lesson card carries its publication date beside the eyebrow. */
export function lessonCard(lesson: LessonView): OgSectionCard {
  return sectionCard({ eyebrow: 'Lesson', title: lesson.title, description: lesson.description, date: longDate(lesson.publishedAt) });
}

/** A problem card names the problem and what a reader can compare on its page. */
export function problemCard(view: ProblemView): OgSectionCard {
  return sectionCard({ eyebrow: 'Problem', title: view.problem.heading, description: view.problem.compare });
}
