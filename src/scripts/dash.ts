// ABOUTME: Draws a signal as a short dash of a link's own line, fading out at both ends.
// ABOUTME: The fade is a gradient laid along the dash and moved with it on every frame.

const SVG = 'http://www.w3.org/2000/svg';

/** How long a dash is. */
export const DASH = 20;

/** Counts the gradients made, so every one on the page has its own name. */
let made = 0;

export interface Dash {
  /** Put the dash on a link, `along` from 0 at its start to 1 past its end. */
  place: (along: number, link: SVGPathElement) => void;
}

/**
 * Turn a path element into a dash of whichever link it is given. A dash takes
 * the link's own curve, and a gap longer than the link keeps it to one. Its
 * colour is a gradient from nothing to the accent and back, set between the
 * two ends of the dash, so the dash fades out at both of them as it travels.
 */
export function fadingDash(signal: SVGPathElement): Dash {
  const svg = signal.ownerSVGElement;
  let defs = svg?.querySelector('defs') ?? null;
  if (svg && !defs) {
    defs = document.createElementNS(SVG, 'defs');
    svg.prepend(defs);
  }
  const gradient = document.createElementNS(SVG, 'linearGradient');
  made += 1;
  gradient.id = `signal-fade-${made}`;
  gradient.setAttribute('gradientUnits', 'userSpaceOnUse');
  for (const [offset, opacity] of [[0, 0], [0.5, 1], [1, 0]] as const) {
    const stop = document.createElementNS(SVG, 'stop');
    stop.setAttribute('offset', String(offset));
    stop.style.stopColor = 'var(--blue-9)';
    stop.style.stopOpacity = String(opacity);
    gradient.append(stop);
  }
  defs?.append(gradient);
  signal.style.stroke = `url(#${gradient.id})`;

  let current: SVGPathElement | null = null;
  let span = 0;
  return {
    place(along, link) {
      if (current !== link) {
        current = link;
        span = link.getTotalLength();
        signal.setAttribute('d', link.getAttribute('d') ?? '');
        signal.style.strokeDasharray = `${DASH} ${span + DASH * 2}`;
      }
      // The dash enters from before the link and leaves past its end.
      const start = along * (span + DASH) - DASH;
      signal.style.strokeDashoffset = String(-start);
      const from = link.getPointAtLength(Math.max(0, start));
      const to = link.getPointAtLength(Math.min(span, start + DASH));
      gradient.setAttribute('x1', String(from.x));
      gradient.setAttribute('y1', String(from.y));
      gradient.setAttribute('x2', String(to.x));
      gradient.setAttribute('y2', String(to.y));
    },
  };
}
