// ABOUTME: The link preview card of one organization page, built once per company with records.
// ABOUTME: The organization page links to this file from its og:image tag.

import type { APIRoute } from 'astro';
import { loadCatalog } from '../../../lib/catalog';
import { organizationCard } from '../../../lib/og';
import { organizationView } from '../../../lib/organization-view';
import { organizationPaths } from '../../../lib/routes';
import { pngResponse, renderCard } from '../../../og/render';

export function getStaticPaths() {
  return organizationPaths(loadCatalog()).map((path) => ({ params: { id: path.split('/').pop() } }));
}

export const GET: APIRoute = async ({ params }) => {
  const view = organizationView(loadCatalog(), params.id!);
  const cards = view.groups.flatMap((group) => group.cards);
  return pngResponse(await renderCard(organizationCard(view.company, cards)));
};
