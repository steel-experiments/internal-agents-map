// ABOUTME: The link preview card of one lesson, built once per lesson.
// ABOUTME: The lesson page links to this file from its og:image tag.

import type { APIRoute } from 'astro';
import { lessonViewBySlug, lessonViews } from '../../../lib/lessons';
import { lessonCard } from '../../../lib/section-cards';
import { pngResponse, renderCard } from '../../../og/render';

export function getStaticPaths() {
  return lessonViews().map((lesson) => ({ params: { slug: lesson.slug } }));
}

export const GET: APIRoute = async ({ params }) => {
  return pngResponse(await renderCard(lessonCard(lessonViewBySlug(params.slug!))));
};
