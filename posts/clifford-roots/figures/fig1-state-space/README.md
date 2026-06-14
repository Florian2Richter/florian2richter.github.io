# Figure 1: the classical state space (2-simplex)

**Status:** done, static. Wired into the post as `#fig-simplex-d3`,
referenced in the prose as `@fig-simplex-d3`. (The click-to-sample
interaction was removed from this figure and lives in Figure 2; Figure 1
shows the static simplex with `p0` marked.)

## What it shows

The classical state space for a three-outcome system: the probability
2-simplex drawn as a triangular face sitting inside the positive octant
of R^3. Three coordinate axes from the origin, the triangle spanning the
three unit basis vectors `e1, e2, e3` (the pure states), faint dashed
medians hinting at the barycentric structure, and the uniform
distribution `p0 = (1/3, 1/3, 1/3)` at the centroid.

**Colour does two jobs.** The simplex *fill* encodes purity (the
`sum_i p_i^2` field, blue-teal at the corners fading to a soft blue-grey
glow at the centre). On top of that, the three pure-state *corners* are
marked in their own identity colours, red, green, and blue (`e1` red,
`e2` green, `e3` blue), so the reader sees three distinct pure colours
blending toward grey at the maximally mixed centre. That grey centre is
the "grey noise" the post opens with. `p0` is drawn as a solid, fully
opaque grey marker (white halo + `GREY_CENTER` dot) with its `p0` label
and `(1/3, 1/3, 1/3)` coordinates at full strength.

## No interaction (static figure)

This figure is static. The click-to-sample interaction (place a marker,
read off `(p1, p2, p3)` from barycentric coordinates) was moved to
Figure 2, so there is no readout panel and no `<script>` here. The
partial is the inlined SVG only; with or without JavaScript the reader
sees the same static triangle.

## Files

| file | role |
|------|------|
| `state_space_figure.py` | generator for the static SVG; all geometry (canvas, vertices, axis endpoints) is in named constants at the top |
| `state_space.svg` | the generated static SVG (checked in) |
| `interactive.qmd` | the partial the post includes: scoped `<style>` plus the inlined static SVG (no readout, no script) |

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
  `aria-label` attributes on the opening `<svg>` tag. (This figure is
  static, so there is no script to keep in sync.)
- **Container styling:** the scoped `.simplex-static` CSS lives in the
  `<style>` block at the top of `interactive.qmd`.
- **Palette:** the blue-grey field endpoints are `PURE_RGB` / `MIXED_RGB`
  in `state_space_figure.py`. The three corner identity colours are
  `CORNER_COLOURS` (red, green, blue), used for both the pure-state dots
  and the `e1, e2, e3` labels. The `p0` marker is a `CENTER #f5f7f8` halo
  over a `GREY_CENTER #8a8f94` dot.

After any change, re-render the post and confirm the figure and its
`@fig-simplex-d3` reference. No edit to `index.qmd` is needed.

## Design constraints (from the original spec)

- The figure is **static**: the SVG is the whole figure, no JS required.
  (The click-to-sample layer that used to live here was removed; the
  interaction is in Figure 2.)
- Do **not** switch the embedding to `fetch()` the SVG at runtime: a
  failed or disabled fetch would leave no figure at all. The SVG is
  inlined for exactly this reason.
- The static SVG is navy strokes on a transparent background, intended
  for a light page. The site theme (`cosmo`) is light, so this is fine;
  if a dark mode is ever added, verify legibility rather than recolouring
  the SVG (it is the shipping static artifact).
