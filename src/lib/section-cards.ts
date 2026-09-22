// ABOUTME: The card inputs of the section, guide, and note pages, read by page and endpoint alike.
// ABOUTME: Every value is a heading or description the page already shows.

import {
  DEFINITIONS_DESCRIPTION,
  DEFINITIONS_HEADING,
  METHODOLOGY_DESCRIPTION,
  METHODOLOGY_HEADING,
  NOTES_DESCRIPTION,
  NOTES_HEADING,
} from './guide-content';
import { longDate, type NoteView } from './notes';
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
  notes: sectionCard({ eyebrow: 'Notes', title: NOTES_HEADING, description: NOTES_DESCRIPTION }),
};

/** A note card carries its publication date beside the eyebrow. */
export function noteCard(note: NoteView): OgSectionCard {
  return sectionCard({ eyebrow: 'Note', title: note.title, description: note.description, date: longDate(note.publishedAt) });
}
