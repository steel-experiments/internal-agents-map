// ABOUTME: The link preview card of one problem page, built once per problem.
// ABOUTME: The problem page links to this file from its og:image tag.

import type { APIRoute } from 'astro';
import { loadCatalog } from '../../../lib/catalog';
import { problemPages, problemView } from '../../../lib/problems';
import { problemCard } from '../../../lib/section-cards';
import { pngResponse, renderCard } from '../../../og/render';

export function getStaticPaths() {
  return problemPages().map((problem) => ({ params: { slug: problem.slug } }));
}

export const GET: APIRoute = async ({ params }) => {
  return pngResponse(await renderCard(problemCard(problemView(loadCatalog(), params.slug!))));
};
