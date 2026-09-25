// ABOUTME: Lists the clean paths of the authored guide, problem, and lesson pages.
// ABOUTME: Discovery files and the routing manifest add these to the catalog routes.
import { lessonViews } from './lessons';
import { problemPages } from './problems';
import { guidePath, lessonsIndexPath } from './routes';

/** Clean paths of every guide page and lesson, without the home page or entries. */
export async function contentPaths(): Promise<string[]> {
  return [
    '/infrastructure',
    guidePath('definitions'),
    guidePath('methodology'),
    lessonsIndexPath(),
    ...problemPages().map((problem) => problem.path),
    ...lessonViews().map((lesson) => lesson.path),
  ];
}
