// ABOUTME: Serves the notes index as Markdown, with one preview for every note.
// ABOUTME: The previews come from the note metadata, not from the rendered page.
import type { APIRoute } from 'astro';
import { loadCatalog } from '../lib/catalog';
import {
  NOTES_CLOSING,
  NOTES_HEADING,
  NOTES_INTRO_AFTER,
  NOTES_INTRO_BEFORE,
  NOTES_LEDE,
} from '../lib/guide-content';
import { notePreviewsMarkdown } from '../lib/notes';
import { canonicalUrl, homePath, notesIndexPath } from '../lib/routes';

function document(): string {
  const catalog = loadCatalog();
  const catalogLink = `[agent catalog](${canonicalUrl(homePath())}#catalog)`;
  return [
    `Source: ${canonicalUrl(notesIndexPath())}`,
    `# ${NOTES_HEADING}`,
    NOTES_LEDE,
    `${NOTES_INTRO_BEFORE}${catalogLink}${NOTES_INTRO_AFTER}`,
    ...notePreviewsMarkdown(catalog),
    NOTES_CLOSING,
  ].join('\n\n');
}

export const GET: APIRoute = () =>
  new Response(`${document()}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
