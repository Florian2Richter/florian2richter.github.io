# Task: add the interactive Bloch ball (Figure 3) to the clifford-roots post

## What this is

`figure3-interactive.html` is a self-contained, progressive-enhancement version
of Figure 3 (the qubit state space — the Bloch ball) for the Quarto post at
`posts/clifford-roots/` on <https://florian2richter.github.io>.

It contains, in order: a scoped `<style>` block, the **static SVG** (byte-for-byte
what `bloch_ball_figure.py` emits into `bloch_ball.svg`), a readout panel with a
**purity slider**, and a `<script>` that adds the interaction.

Interaction: clicking the visible front face picks a **pure state** (by inverting
the orthographic projection). The **Purity** slider, r in [0, 1], then scales the
Bloch vector inward along the radius — from the surface (r = 1, pure) toward the
maximally mixed state I/2 at the centre (r = 0). As the marker sinks in it dims
and shrinks, conveying depth in the otherwise flat projection. The readout shows
the Bloch vector r·n, the density matrix rho = 1/2(I + r·sigma), and its
eigenvalues (1 ± r)/2. A click outside the disc clears the selection.

## The non-negotiable constraints

1. **The interactive layer is purely additive.** With JavaScript disabled (or on
   error), the reader must see the unaltered static Bloch ball and a quiet, empty
   readout. Nothing may make the figure depend on JS to appear.

2. **Do not change the embedding to `fetch()` the SVG.** It is inlined on purpose:
   a failed or disabled fetch would leave no figure at all, breaking constraint 1.

3. **Do not have the JS redraw the wireframe.** The wireframe, axes, poles, and
   labels are all in the baked SVG. The script only *adds* three things — a faint
   radius guide, a hover-preview dot, and the marker — and updates the readout. (A
   chat prototype did redraw the wireframe in JS for convenience; this production
   file deliberately does not, so the no-JS fallback stays intact.)

## Where it goes

Into the post's `.qmd` (e.g. `posts/clifford-roots/index.qmd`), where Figure 3
lives. Paste the entire contents of `figure3-interactive.html` into a Quarto
raw-HTML passthrough block so Pandoc passes it through verbatim (this reliably
handles the `<script>`):

````markdown
```{=html}
<!-- paste the full contents of figure3-interactive.html here -->
```
````

Keep the existing figure caption / cross-reference wrapper (e.g. the
`#fig-blochball` div or caption line) so `@fig-...` references in the prose still
resolve. The raw-HTML block sits where the static SVG used to. (Alternatively,
save the file as a `_figure3-interactive.qmd` partial whose body is the `{=html}`
fence above and `{{< include _figure3-interactive.qmd >}}` it — either is fine.)

## How the geometry stays in sync (single source of truth)

The JS does **not** hard-code the projection. It reads five values from `data-*`
attributes on the `<svg>` tag — `data-cx`, `data-cy`, `data-r`, `data-alpha-deg`,
`data-elev-deg` — which `bloch_ball_figure.py` emits from its own constants. The
inverse projection and the marker geometry are all derived from those, so there
is one source of truth and nothing is retyped.

The inversion picks the **camera-facing hemisphere** (the front cap, depth > 0);
that is the visible surface, and it is the only hemisphere clicks map to. Interior
(mixed) states are reached not by clicking but via the purity slider scaling the
chosen surface direction inward.

**If you regenerate the figure** (`python bloch_ball_figure.py`, after a geometry,
angle, or label tweak): re-copy the new `bloch_ball.svg` body into the fragment,
replacing everything between the `<svg ...>` opening tag and `</svg>`. Keep the
opening tag as emitted — it carries the `data-*` attributes. The JS needs no edits;
it re-reads the new geometry automatically. (Because the projection is affine, the
marker's inward path is just the straight line from the clicked point to the centre,
so it stays correct under any retuning.)

## Styling notes

- All styles are scoped under `.bloch-interactive` and use the figure's own palette
  (navy `#1a3550`, muted `#3a5a72`, teal accent `#1d9e75`/`#0f6e56`, light readout
  panel `#f4f6f8`). They cannot leak into or collide with the site theme.
- The static SVG uses dark navy strokes on a transparent background, intended for a
  **light** page. If the site theme has a dark mode, verify legibility; if needed,
  wrap the figure in a light-background container — do **not** recolor the SVG, it
  is the shipping static artifact.
- The script sets up every `.bloch-interactive` on the page. The `<style>` block
  should appear only once; if the pattern is reused for other figures, factor the
  style out to shared CSS and keep only the per-figure markup + script.

## Two design defaults (easy to change)

1. **Depth cue strength.** As purity goes 1 -> 0, marker opacity runs 1.0 -> 0.4
   and scale 1.0 -> 0.78 (the `0.4 + 0.6*t`, `0.78 + 0.22*t`, and halo-opacity `t`
   lines in `render()`). The marker never fully vanishes so the maximally mixed
   state stays visible at the centre. Dial these if the centre feels too faint or
   the shrink too strong.
2. **Marker colour.** The user marker is teal to contrast with the structural red
   `I/2` centre dot. To reuse the red, change the two `marker` circle fills/strokes.

## Verification checklist

- [ ] JS on: clicking the top pole reads (0, 0, 1) with rho = |0><0| (eigenvalues
      1, 0); the bottom pole reads (0, 0, -1) = |1><1|. The dead-centre of the disc
      gives the pure state facing the camera.
- [ ] Dragging Purity moves the marker straight down the dashed radius toward the
      centre; at r = 0 the Bloch vector is (0, 0, 0), rho = 1/2 I, eigenvalues
      0.50, 0.50, and the marker sits on the red `I/2` dot. The marker dims and
      shrinks as r decreases.
- [ ] A new click resets purity to 1; a click outside the disc clears everything.
- [ ] Desktop hover shows a faint preview dot on the surface.
- [ ] JS off (or `<script>` removed): the static Bloch ball renders exactly as
      before; the readout shows placeholder text, dashes, and a disabled slider.
- [ ] `@fig-...` cross-references and the caption are unchanged.
- [ ] Legible in both the site's light and (if present) dark themes.

## Out of scope

Do not restyle or re-lay-out the static figure (colours, geometry, labels, viewing
angles), animate anything, touch the other figures (classical simplex = Figure 1,
done; trajectories; orbit cycle), or edit the post's prose. This task is only the
interactive layer for Figure 3.
