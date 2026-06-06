# Figure 3: the Bloch ball (qubit state space)

**Status:** done, static. Wired into the post as `#fig-bloch`,
referenced in the prose as `@fig-bloch`. This is the quantum counterpart
of Figure 1 (the classical simplex state space): both are static
state-space sketches. The click-to-trace interaction lives in Figure 4
(the root trajectories), mirroring how Figure 2 carries the classical
interaction.

## What it shows

The qubit state space: a wireframe Bloch ball under a fixed orthographic
projection (azimuth 35 degrees, elevation 20 degrees). Latitude and
longitude lines, a crisp silhouette, three coordinate axes (x, y, z) from
the centre, the poles `|0>` and `|1>`, and the maximally mixed state
`I/2` at the centre. Front-hemisphere wires are solid, back-hemisphere
wires dashed.

**Colour encodes purity** (the shared scheme, see the figures
`README.md`). The quantum purity `tr(rho^2) = (1 + r^2)/2` runs from 1/2
at the centre to 1 on the surface, so the ball is a blue-teal shell
fading to a soft blue-grey core (the "inside the sphere" depth), and the
poles `|0>`, `|1>` are blue-teal. The maximally mixed state `I/2` is the
solid, fully visible marker used in Figures 1, 2 and 4 (white halo + dark
`AXIS #233746` dot, full-strength label), not the faint ring it used to
be. The wireframe and axes stay navy.

## No interaction (static figure)

This figure is static. The earlier click-to-pick-a-state + purity-slider
interaction (and its density-matrix readout) was moved to Figure 4, so
there is no readout panel and no `<script>` here; the partial is the
inlined SVG only. With or without JavaScript the reader sees the same
static ball. (The generator still emits `data-*` projection attributes on
the `<svg>` tag; they are harmless here and are what Figure 4's script
relies on in its own SVG.)

## Files

| file | role |
|------|------|
| `bloch_ball_figure.py` | generator for the static SVG; geometry, viewing angles, and wireframe density are constants at the top |
| `bloch_ball.svg` | the generated static SVG (checked in) |
| `interactive.qmd` | the partial the post includes: scoped `<style>` plus the inlined static SVG (no readout, no script) |

## To modify

- **Geometry / viewing angles / wireframe density / palette:** edit the
  constants at the top of `bloch_ball_figure.py`, then regenerate:
  ```bash
  python bloch_ball_figure.py bloch_ball.svg
  ```
  Then re-copy the new SVG body (from `<svg ...>` through `</svg>`) into
  `interactive.qmd`, replacing the old inline SVG, keeping the
  `role`/`aria-label` on the opening `<svg>` tag.
- The projection (`ALPHA`, `ELEV`, `CX`, `CY`, `R`) is shared, by
  convention, with Figure 4 (`fig3b-bloch-root`) so the two balls
  register exactly. If you retune the angles here, mirror them there.

## Design constraints

- The figure is **static**: the SVG is the whole figure, no JS required.
- Do **not** switch the embedding to `fetch()` the SVG: a failed or
  disabled fetch would leave no figure at all. The SVG is inlined.
