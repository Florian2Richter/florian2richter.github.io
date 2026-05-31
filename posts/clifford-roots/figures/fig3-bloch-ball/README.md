# Figure 3: the Bloch ball (qubit state space)

**Status:** done, interactive. Wired into the post as `#fig-bloch`,
referenced in the prose as `@fig-bloch`.

## What it shows

The qubit state space: a wireframe Bloch ball under a fixed orthographic
projection (azimuth 35 degrees, elevation 20 degrees), drawn in the same
restrained blue palette as Figure 1. Latitude and longitude lines, a
crisp silhouette, three coordinate axes (x, y, z) from the centre, the
poles `|0>` and `|1>`, and the maximally mixed state `I/2` marked in red
at the centre. Front-hemisphere wires are solid, back-hemisphere wires
dashed.

## The interaction

Clicking the visible **front face** picks a pure state, by inverting the
orthographic projection onto the camera-facing hemisphere. The **Purity**
slider, r in [0, 1], then scales the Bloch vector inward along the
radius: from the surface (r = 1, pure) toward `I/2` at the centre
(r = 0). As the marker sinks in it dims and shrinks, conveying depth in
the otherwise flat projection. The readout shows the Bloch vector
`r * n`, the density matrix `rho = 1/2 (I + r * sigma)`, and its
eigenvalues `(1 +/- r)/2`. A click outside the disc clears the selection.

Quick checks: the top pole reads `(0, 0, 1)` with `rho = |0><0|`
(eigenvalues 1, 0); the bottom pole `(0, 0, -1) = |1><1|`; at r = 0 the
vector is `(0, 0, 0)`, `rho = 1/2 I`, eigenvalues `0.50, 0.50`. With
JavaScript off, the static Bloch ball renders unchanged, the readout
shows placeholders, and the slider is disabled.

## Files

| file | role |
|------|------|
| `bloch_ball_figure.py` | generator for the static SVG; geometry, viewing angles, and wireframe density are constants at the top. Emits `data-*` projection attributes on the `<svg>` tag |
| `bloch_ball.svg` | the generated static SVG (checked in) |
| `interactive.qmd` | the partial the post includes: scoped `<style>`, the inlined SVG, the readout (with the purity slider and the 2x2 density-matrix grid), and the `<script>` |

This README is the single self-contained doc for the figure; the useful
content of the original task spec and handover notes is folded in below.

## How geometry stays in sync

The `<script>` does not hard-code the projection. It reads five values
from `data-*` attributes on the `<svg>` tag (`data-cx`, `data-cy`,
`data-r`, `data-alpha-deg`, `data-elev-deg`), which the generator emits
from its own constants. The inverse projection and the marker geometry
are all derived from those, so there is a single source of truth. Because
the projection is affine, the marker's inward path is just the straight
line from the clicked point to the centre, so it stays correct under any
retuning of the angles.

## Note: this figure was reconstructed

The originally delivered `figure3-interactive.html` arrived corrupted:
its `<style>` block and its `.bloch-interactive` wrapper were missing,
and the header comment had swallowed the `<svg>` opening tag. The figure
was rebuilt from the parts that were intact plus the generator:

- the **SVG** was regenerated verbatim from `bloch_ball_figure.py`;
- the **readout HTML** and the **`<script>`** were taken unchanged from
  the original file;
- the lost **`<style>` block** was rewritten, modeled on the Figure 1
  readout styling (same palette and panel look), extended for the purity
  slider and the 2x2 matrix grid.

So everything except the readout CSS is from the original sources. The
readout CSS is the one piece that is a reconstruction rather than the
author's original design.

## To modify

- **Geometry / viewing angles / wireframe density / palette:** edit the
  constants at the top of `bloch_ball_figure.py`, then regenerate:
  ```bash
  python bloch_ball_figure.py bloch_ball.svg
  ```
  Then re-copy the new SVG body (from `<svg ...>` through `</svg>`) into
  `interactive.qmd`, replacing the old inline SVG. Keep the opening
  `<svg>` tag as emitted; it carries the `data-*` attributes the JS
  reads. The `<script>` needs no edits.
- **Readout styling:** the scoped `.bloch-interactive` CSS lives in the
  `<style>` block at the top of `interactive.qmd`.
- **Depth-cue strength:** as purity goes 1 to 0, the marker opacity runs
  `1.0 -> 0.4` and its scale `1.0 -> 0.78` (the `0.4 + 0.6*t`,
  `0.78 + 0.22*t`, and halo-opacity `t` lines in the script's `render()`).
  The marker never fully vanishes, so the maximally mixed state stays
  visible at the centre. Dial these if the centre feels too faint or the
  shrink too strong.
- **Marker colour:** the user marker is teal to contrast with the red
  `I/2` centre dot; change the two marker circle fills/strokes to reuse
  the red.

After any change, re-render the post and confirm the figure and its
`@fig-bloch` reference. No edit to `index.qmd` is needed.

## Design constraints (from the original spec)

- The interactive layer is **purely additive**: with JS disabled the
  reader sees the unaltered static Bloch ball, a placeholder readout, and
  a disabled slider. Nothing may make the figure depend on JS to appear.
- Do **not** switch the embedding to `fetch()` the SVG: a failed or
  disabled fetch would leave no figure at all. The SVG is inlined.
- Do **not** have the JS redraw the wireframe. The wireframe, axes,
  poles, and labels are all in the baked SVG; the script only *adds* a
  faint radius guide, a hover-preview dot, and the marker, and updates
  the readout.
- Clicks map only to the camera-facing (front) hemisphere, the visible
  surface. Interior (mixed) states are reached via the purity slider
  scaling the chosen surface direction inward, not by clicking.
