// ABOUTME: The link preview card of one catalog implementation, built once per entry.
// ABOUTME: The entry page links to this file from its og:image tag.

import type { APIRoute } from 'astro';
import { loadCatalog } from '../../../lib/catalog';
import { directoryCards } from '../../../lib/entry-view';
import { entryCard } from '../../../lib/og';
import { assertPublishableId } from '../../../lib/routes';
import { pngResponse, renderCard } from '../../../og/render';

export function getStaticPaths() {
  return loadCatalog().approaches.map((approach) => {
    assertPublishableId(approach.id);
    return { params: { id: approach.id } };
  });
}

export const GET: APIRoute = async ({ params }) => {
  const card = directoryCards(loadCatalog()).find((item) => item.id === params.id);
  if (!card) throw new Error(`No catalog entry "${params.id}" for a preview card.`);
  return pngResponse(await renderCard(entryCard(card)));
};
