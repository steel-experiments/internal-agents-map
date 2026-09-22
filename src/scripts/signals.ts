// ABOUTME: Sends small signals along a diagram's links, in both directions.
// ABOUTME: Every diagram reads the same without this: the signals only show the traffic.

import { animate } from 'motion';

/** How long one signal takes to cross a link, unless its diagram states otherwise. */
const TRAVEL_SECONDS = 2.6;
/** How long the gap is before a signal sets off again. */
const REPEAT_SECONDS = 1.4;
/** The share of the crossing a signal spends fading in, and again fading out. */
const FADE = 0.15;

/** Readers who ask for less motion get the diagram still. */
function reducedMotion(): boolean {
  return typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** Full at the middle of a crossing, nothing at either end. */
function fade(progress: number): number {
  if (progress < FADE) return progress / FADE;
  if (progress > 1 - FADE) return (1 - progress) / FADE;
  return 1;
}

/** The signals now crossing, so the page that replaces this one can stop them. */
let crossing: { stop: () => void }[] = [];

/** Start the signals in every diagram that declares them. */
export function startSignals(): void {
  // The router swaps the diagram rather than reloading the page, so the signals
  // of the diagram it replaced are stopped here; left alone they would go on
  // crossing a diagram that is no longer on the page.
  for (const signal of crossing) signal.stop();
  crossing = [];
  if (reducedMotion()) return;

  for (const scene of document.querySelectorAll<HTMLElement | SVGElement>('[data-signals]')) {
    const travel = Number(scene.dataset.signals) || TRAVEL_SECONDS;
    for (const signal of scene.querySelectorAll<SVGCircleElement>('.signal')) {
      const link = scene.querySelector<SVGPathElement>(`#${signal.dataset.link}`);
      if (!link) continue;
      const span = link.getTotalLength();
      // A returning signal walks the same link backwards, from the far end home.
      const returning = signal.dataset.return !== undefined;

      const crossed = animate(0, 1, {
        duration: travel,
        ease: 'linear',
        repeat: Infinity,
        repeatDelay: REPEAT_SECONDS,
        delay: Number(signal.dataset.delay ?? 0),
        onUpdate: (progress: number) => {
          const at = link.getPointAtLength((returning ? 1 - progress : progress) * span);
          signal.setAttribute('cx', String(at.x));
          signal.setAttribute('cy', String(at.y));
          signal.style.opacity = String(fade(progress));
        },
      });
      crossing.push(crossed);
    }
  }
}
