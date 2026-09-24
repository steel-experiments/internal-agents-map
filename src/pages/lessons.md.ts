// ABOUTME: Serves the lessons index as Markdown, with one preview for every lesson.
// ABOUTME: The previews come from the lesson metadata, not from the rendered page.
import type { APIRoute } from 'astro';
import { loadCatalog } from '../lib/catalog';
import {
  LESSONS_CLOSING,
  LESSONS_HEADING,
  LESSONS_INTRO_AFTER,
  LESSONS_INTRO_BEFORE,
  LESSONS_LEDE,
} from '../lib/guide-content';
import { lessonPreviewsMarkdown } from '../lib/lessons';
import { canonicalUrl, homePath, lessonsIndexPath } from '../lib/routes';

function document(): string {
  const catalog = loadCatalog();
  const catalogLink = `[agent catalog](${canonicalUrl(homePath())}#catalog)`;
  return [
    `Source: ${canonicalUrl(lessonsIndexPath())}`,
    `# ${LESSONS_HEADING}`,
    LESSONS_LEDE,
    `${LESSONS_INTRO_BEFORE}${catalogLink}${LESSONS_INTRO_AFTER}`,
    ...lessonPreviewsMarkdown(catalog),
    LESSONS_CLOSING,
  ].join('\n\n');
}

export const GET: APIRoute = () =>
  new Response(`${document()}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
