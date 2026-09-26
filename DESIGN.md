# Design

- Set headings and the wordmark in Nanum Myeongjo ExtraBold (800) through `--font-brand`: 24px page titles, 20px section and card headings, a 16px wordmark. Set everything else in ABC Areal: 14px body, opening paragraphs, and controls, 12px metadata, in regular (400) and medium (500). Labels inside a diagram stay in Areal. Inherit existing responsive overrides.
- Keep one font weight within a paragraph; use darker text for inline emphasis.
- Use a `--sand-1` page ground and Radix Sand colors: `--sand-12` for headings, `--sand-10` for body and secondary text, `--sand-3` for surfaces, and `--sand-6` for fine dividers.
- Use one blue, the wordmark's `--brand`. The `--blue-*` steps are mixed from it, so every accent, badge, and mark shares its hue.
- Reuse the centered 684px content column with a fixed sidebar and table of contents 60px either side of it, all three starting on one line. A wide screen has no top bar; the wordmark heads the sidebar. Follow the shared mobile layout, with its bar, and 24px page padding.
- Keep spacing tight: 8–16px within components, 32–40px between sections, and no stray margins that add to a section's own.
- Lay the catalog out as fully clickable cards, four wide to five tall, 16px apart: rounded 14px badges at the head with a bookmark on their line, the title and a two-line muted summary at the foot, on a white panel with a hairline Sand border, 26px corners, and a faint shadow. A card darkens on hover. Group the homepage's cards under the problems they answer. The floating bottom pill is a button that opens the command palette.
- Group workflows, lessons, and related links in soft Sand panels with 14–16px corners. Use consistent tables for structured details.
- Use 40px-high buttons with 10px corners, a label on the left, and an existing icon on the right. Use the dark variant for the main onward action.
- Reuse the shared icons and components. Draw diagrams bare, with no panel or frame, in one thin `--figure-line`; what moves along a line is a short dash of it in the accent, fading out at both ends.
- Keep motion subtle: quick hover feedback, smooth filtering and disclosures, and support for reduced motion. Preserve keyboard focus and accessible labels.

Reference: [tokens](src/styles/tokens.css), [layout](src/styles/layout.css), [components](src/styles/components.css).
