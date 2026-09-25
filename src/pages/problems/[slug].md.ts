// ABOUTME: Publishes the same records and lessons as the HTML page of one problem.
// ABOUTME: Machine readers find this file through llms.txt and the routing manifest.
import type { APIRoute } from 'astro';
import { loadCatalog } from '../../lib/catalog';
import { problemMarkdown, problemPages } from '../../lib/problems';

export function getStaticPaths() {
  return problemPages().map((problem) => ({ params: { slug: problem.slug } }));
}
export const GET: APIRoute = ({ params }) => new Response(problemMarkdown(loadCatalog(), params.slug!), {
  headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
});
