# Figure 1: the classical state space (2-simplex)

**Status:** done, interactive. Wired into the post as `#fig-simplex-d3`,
referenced in the prose as `@fig-simplex-d3`.

## What it shows

The classical state space for a three-outcome system: the probability
2-simplex drawn as a triangular face sitting inside the positive octant
of R^3. Three coordinate axes from the origin, the triangle spanning the
three unit basis vectors `e1, e2, e3` (the pure states), faint dashed
medians hinting at the barycentric structure, and the uniform
distribution `p0 = (1/3, 1/3, 1/3)` at the centroid.

**Colour encodes purity** (see the figures `README.md` for the shared
scheme): the simplex is filled with the purity field `sum_i p_i^2`,
blue-teal and saturated at the three pure corners, fading to a soft blue-grey glow at
the maximally mixed centre. `p0` is drawn as a faint hollow ring,
de-emphasised but locatable.

## The interaction

Clicking inside the triangle places a contrasting amber marker and
reads off the probability distribution `(p1, p2, p3)` for that point,
computed from barycentric coordinates relative to the three vertices.
On desktop, hovering shows a faint preview marker. A click outside the
triangle clears the marker. With JavaScript off, the
static triangle renders unchanged and the readout shows placeholder text.

Quick checks: the centroid reads `(0.33, 0.33, 0.33)`; a vertex reads
`1.00` on its own axis; a point on an edge reads `0` on the opposite
axis.

## Files

| file | role |
|------|------|
| `state_space_figure.py` | generator for the static SVG; all geometry (canvas, vertices, axis endpoints) is in named constants at the top |
| `state_space.svg` | the generated static SVG (checked in) |
| `interactive.qmd` | the partial the post includes: scoped `<style>`, the inlined SVG, the readout panel, and the `<script>` |

This README is the single self-contained doc for the figure; the useful
content of the original task spec and handover notes is folded in below.

## How geometry stays in sync

The `<script>` does not hard-code any vertex coordinates. It reads the
three vertex pixel positions from the SVG `<polygon points="...">`
attribute at load time, in `e1, e2, e3` order, and maps them to outcomes
1, 2, 3. The generator emits the polygon vertices in that order, so that
ordering is the only coupling between the Python and the JS.

## To modify

- **Geometry / palette / labels:** edit the constants at the top of
  `state_space_figure.py`, then regenerate:
  ```bash
  python state_space_figure.py state_space.svg
  ```
  Then re-copy the new SVG body (from `<svg ...>` through `</svg>`) into
  `interactive.qmd`, replacing the old inline SVG. Keep the `role` and
  `aria-label` attributes on the opening `<svg>` tag. The JS needs no
  edits as long as the polygon vertices stay in `e1, e2, e3` order.
- **Readout styling:** the scoped `.simplex-interactive` CSS lives in the
  `<style>` block at the top of `interactive.qmd`.
- **Palette:** the blue-grey field endpoints are `PURE_RGB` / `MIXED_RGB`
  in `state_space_figure.py`, mirrored in the script's `purityColour`
  helper. The placed marker is the fixed amber `STATE #bf6f30`.
- **Readout placement:** the readout sits below the figure (consistent at
  all widths). To place it beside the figure on wide screens, wrap the SVG
  and `.si-readout` in a flex/grid container with a responsive breakpoint.

After any change, re-render the post and confirm the figure and its
`@fig-simplex-d3` reference. No edit to `index.qmd` is needed.

## Design constraints (from the original spec)

- The interactive layer is **purely additive**: with JS disabled the
  reader must see the unaltered static triangle and a quiet, empty
  readout. Nothing may make the figure depend on JS to appear.
- Do **not** switch the embedding to `fetch()` the SVG at runtime: a
  failed or disabled fetch would leave no figure at all. The SVG is
  inlined for exactly this reason.
- The static SVG is navy strokes on a transparent background, intended
  for a light page. The site theme (`cosmo`) is light, so this is fine;
  if a dark mode is ever added, verify legibility rather than recolouring
  the SVG (it is the shipping static artifact).
