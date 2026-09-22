// ABOUTME: The link preview card of one note, built once per note.
// ABOUTME: The note page links to this file from its og:image tag.

import type { APIRoute } from 'astro';
import { noteViewBySlug, noteViews } from '../../../lib/notes';
import { noteCard } from '../../../lib/section-cards';
import { pngResponse, renderCard } from '../../../og/render';

export function getStaticPaths() {
  return noteViews().map((note) => ({ params: { slug: note.slug } }));
}

export const GET: APIRoute = async ({ params }) => {
  return pngResponse(await renderCard(noteCard(noteViewBySlug(params.slug!))));
};
