// ABOUTME: The link preview card of the home page, published at /og.png.
// ABOUTME: Pages without a card of their own also point to this file.

import type { APIRoute } from 'astro';
import { HOME_CARD } from '../lib/section-cards';
import { pngResponse, renderCard } from '../og/render';

export const GET: APIRoute = async () => pngResponse(await renderCard(HOME_CARD));
