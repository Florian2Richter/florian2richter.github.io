# Task: add the interactive version of Figure 1 to the clifford-roots post

## What this is

`figure1-interactive.html` is a self-contained, progressive-enhancement version
of Figure 1 (the classical state space — the 2-simplex over three outcomes) for
the Quarto post at `posts/clifford-roots/` on
<https://florian2richter.github.io>.

It contains three things, in order: a small scoped `<style>` block, the **static
SVG** (byte-for-byte what `state_space_figure.py` emits into `state_space.svg`,
with only `role`/`aria-label` added to the opening tag), and a `<script>` that
adds the interaction. When the user clicks inside the triangle, a teal marker is
placed and a readout panel below shows the probability distribution
`(p1, p2, p3)` for that point, plus three live bars. On desktop, hovering shows
a lighter preview marker. A click outside the triangle clears the marker.

## The non-negotiable design constraint

**The interactive layer is purely additive.** With JavaScript disabled (or if it
errors), the reader must see the unaltered static figure and nothing broken. Do
not introduce anything that makes the figure depend on JS to appear. In
particular: **do not** change the embedding to `fetch()` the SVG from
`state_space.svg` at runtime — that was considered and rejected precisely because
a failed/disabled fetch would leave no figure at all. The SVG is inlined for this
reason.

## Where it goes

Into the post's `.qmd` (e.g. `posts/clifford-roots/index.qmd`), replacing the
current static Figure 1 include.

### Recommended embedding: a raw-HTML passthrough block

Paste the entire contents of `figure1-interactive.html` between a Quarto raw-HTML
fence so Pandoc passes it through verbatim (this reliably handles the `<script>`
tag):

````markdown
```{=html}
<!-- paste the full contents of figure1-interactive.html here -->
```
````

Keep the existing figure caption / cross-reference machinery (e.g. a surrounding
`::: {#fig-statespace}` div or a `: caption {#fig-statespace}` line) so `@fig-...`
references in the prose still resolve. The raw-HTML block sits where the static
SVG used to.

### Alternative: keep it as a separate partial

If you prefer not to inline a large block, save the file as a `.qmd` partial
(e.g. `_figure1-interactive.qmd`) whose entire body is the `{=html}` fence above,
then `{{< include _figure1-interactive.qmd >}}` at the figure's location. Either
approach is fine; the inline raw block is simplest.

## How the geometry stays in sync (single source of truth)

The JS does **not** hard-code any vertex coordinates. It reads the three vertex
pixel positions from the SVG `<polygon points="...">` attribute at load time, in
the order they appear, and maps them to outcomes 1, 2, 3. The Python script emits
the polygon vertices in `e1, e2, e3` order, so that order is the only coupling.

**If you regenerate the figure** (`python state_space_figure.py`, e.g. after a
geometry or label tweak): re-copy the new `state_space.svg` body into the
fragment, replacing everything between the `<svg ...>` opening tag and `</svg>`.
Preserve the `role`/`aria-label` attributes already added to the opening tag. The
JS needs no edits — it re-reads the new vertices automatically. As long as the
vertices remain in `e1, e2, e3` order, the readout stays correct.

## Styling notes

- All styles are scoped under `.simplex-interactive` so they cannot leak into or
  collide with the site theme. The readout uses the figure's own palette
  (navy `#1a3550`, muted `#3a5a72`, teal accent `#1d9e75`).
- The static SVG uses dark navy strokes on a transparent background, intended for
  a **light** page background. If the site's theme has a dark mode, verify the
  figure is still legible in dark mode; if not, wrap the figure in a
  light-background container (do not recolor the SVG itself — that's the shipping
  static artifact). Confirm against the actual theme before assuming.
- The script handles multiple instances: it sets up every `.simplex-interactive`
  on the page. The scoped `<style>` block, however, should appear only once — if
  this pattern is later reused for other figures in the post, factor the style
  block out to a shared CSS file and keep only the per-figure markup + script.

## Two open design choices (currently set to sensible defaults; change if desired)

These were left to author preference and are easy one-liners:

1. **Marker colour.** The user-placed marker is teal (`#1d9e75` fill / `#0f6e56`
   stroke) to distinguish it from the structural red `p0` dot. To reuse the
   `p0` red instead, change the two `marker` circle fills/strokes in the script
   to `#c0392b`.
2. **Readout placement.** The readout sits below the figure. To place it beside
   the figure on wide screens, wrap the SVG and `.si-readout` in a flex/grid
   container with a responsive breakpoint (stack below on narrow screens). Below
   is the current default because it is consistent across all widths.

## Verification checklist

- [ ] With JS enabled: clicking inside the triangle places a teal marker; the
      readout shows `(p1, p2, p3)` and three bars. Centroid reads
      `(0.33, 0.33, 0.33)`; a corner reads `1.00` on its axis; an edge reads
      `0` on the opposite axis. Clicking outside clears it.
- [ ] On desktop: hovering inside shows a faint preview marker.
- [ ] With JS disabled (or `<script>` removed): the static figure renders exactly
      as before; the readout simply shows the placeholder text and empty bars.
- [ ] `@fig-...` cross-references in the prose still resolve and the caption is
      unchanged.
- [ ] Figure is legible in both the site's light and (if present) dark themes.

## Out of scope

Do not restyle or re-lay-out the static figure (colours, geometry, labels),
animate anything, touch the other figures (trajectories, Bloch ball, orbit
cycle), or edit the post's prose. This task is only the interactive layer for
Figure 1.
