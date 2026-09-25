// ABOUTME: Serves one lesson as Markdown, built from the body the author wrote.
// ABOUTME: Citations, diagram explanations, sources, and catalog links all remain.
import type { APIRoute, GetStaticPaths } from 'astro';
import { loadCatalog } from '../../lib/catalog';
import { lessonMarkdown, lessonViewBySlug, lessonViews } from '../../lib/lessons';

export const getStaticPaths: GetStaticPaths = () =>
  lessonViews().map((lesson) => ({ params: { slug: lesson.slug } }));

export const GET: APIRoute = ({ params }) => {
  const lesson = lessonViewBySlug(params.slug as string);
  return new Response(`${lessonMarkdown(loadCatalog(), lesson)}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
};
