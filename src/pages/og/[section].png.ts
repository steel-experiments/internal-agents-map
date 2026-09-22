// ABOUTME: The link preview cards of the section and guide pages, one file per page.
// ABOUTME: Each page and this endpoint read the same card input from src/lib/section-cards.

import type { APIRoute } from 'astro';
import { SECTION_CARDS } from '../../lib/section-cards';
import { pngResponse, renderCard } from '../../og/render';

export function getStaticPaths() {
  return Object.keys(SECTION_CARDS).map((section) => ({ params: { section } }));
}

export const GET: APIRoute = async ({ params }) => {
  const card = SECTION_CARDS[params.section as keyof typeof SECTION_CARDS];
  if (!card) throw new Error(`No section card for "${params.section}".`);
  return pngResponse(await renderCard(card));
};
