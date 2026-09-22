// ABOUTME: Runs the background-work diagram: a trigger arrives, the agent works, a result lands.
// ABOUTME: One repeating timeline states every element, so a paused tab resumes coherently.

import { animate } from 'motion';

/** How long one pass of the cycle takes. */
const CYCLE_SECONDS = 7;

/**
 * Where each step begins and ends within a pass, as a share of it.
 * The agent's stretch is the long one: the work is the point of the diagram.
 */
const ARRIVE = [0, 0.15] as const;
const TO_AGENT = [0.2, 0.35] as const;
const WORKING = [0.35, 0.72] as const;
const TO_RESULT = [0.72, 0.87] as const;
/** The result holds just long enough to be read, then clears before the next pass. */
const DONE = [0.87, 1] as const;
const DONE_FALL = 0.2;
/** The trigger stays lit from its arrival, and fades out with the result. */
const LIT = [0.15, 1] as const;
const LIT_FALL = ((1 - DONE[0]) * DONE_FALL) / (1 - LIT[0]);
/** How many turns the spinner makes while the agent works. */
const SPINS = 3;
/** How much of a window a state spends arriving, and how much leaving. */
const RISE = 0.05;
const FALL = 0.12;

/** Readers who ask for less motion get the finished state, held still. */
function reducedMotion(): boolean {
  return typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** How far into a window the pass has come, or null when it is outside it. */
function within(progress: number, [from, to]: readonly [number, number]): number | null {
  if (progress < from || progress > to) return null;
  return (progress - from) / (to - from);
}

/** A firm ease-out: quick to arrive, unhurried as it settles. */
function easeOut(value: number): number {
  return 1 - (1 - value) ** 3;
}

/**
 * Rise into a state, hold it, then fall back out of it.
 * Nothing on the diagram switches on between one frame and the next.
 */
function pulse(along: number | null, rise = RISE, fall = FALL): number {
  if (along === null) return 0;
  if (along < rise) return easeOut(along / rise);
  if (along > 1 - fall) return easeOut((1 - along) / fall);
  return 1;
}

/** The pass now running, so the page that replaces this one can stop it. */
let running: { stop: () => void } | undefined;

/** Start the cycle. Without this the diagram still states its three steps. */
export function startWorkCycle(): void {
  // The router swaps the diagram rather than reloading the page, so the pass
  // over the one it replaced is stopped before another begins.
  running?.stop();
  running = undefined;
  const scene = document.querySelector('.cycle-scene');
  if (!scene) return;

  const find = <T extends SVGElement>(selector: string): T | null => scene.querySelector<T>(selector);
  const lit = find('.cycle-trigger-on');
  const spinner = find('.cycle-spinner');
  const result = find('.cycle-result-dot');
  const signal = find<SVGCircleElement>('.cycle-signal');
  const legs = ['#cycle-in', '#cycle-work', '#cycle-out'].map((id) => find<SVGPathElement>(id));
  if (!lit || !spinner || !result || !signal || legs.some((leg) => !leg)) return;

  if (reducedMotion()) {
    lit.setAttribute('opacity', '1');
    result.setAttribute('opacity', '1');
    return;
  }

  /**
   * Put the signal on one leg of the path, or take it off the page.
   * A signal keeps a constant speed: easing it would read as a state change
   * rather than as something crossing the distance.
   */
  const carry = (leg: SVGPathElement | null, along: number | null): boolean => {
    if (!leg || along === null) return false;
    const at = leg.getPointAtLength(along * leg.getTotalLength());
    signal.setAttribute('cx', String(at.x));
    signal.setAttribute('cy', String(at.y));
    signal.setAttribute('opacity', String(pulse(along, 0.18, 0.18)));
    return true;
  };

  running = animate(0, 1, {
    duration: CYCLE_SECONDS,
    ease: 'linear',
    repeat: Infinity,
    onUpdate: (progress: number) => {
      const carried =
        carry(legs[0]!, within(progress, ARRIVE)) ||
        carry(legs[1]!, within(progress, TO_AGENT)) ||
        carry(legs[2]!, within(progress, TO_RESULT));
      if (!carried) signal.setAttribute('opacity', '0');

      lit.setAttribute('opacity', String(pulse(within(progress, LIT), RISE, LIT_FALL)));
      result.setAttribute('opacity', String(pulse(within(progress, DONE), 0.3, DONE_FALL)));

      const working = within(progress, WORKING);
      spinner.setAttribute('opacity', String(pulse(working, 0.08, 0.08)));
      if (working !== null) {
        spinner.setAttribute('transform', `rotate(${working * SPINS * 360} 326 140)`);
      }
    },
  });
}
