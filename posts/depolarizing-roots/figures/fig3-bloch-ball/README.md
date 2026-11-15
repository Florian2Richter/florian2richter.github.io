# Figure 3: the Bloch ball (qubit state space)

**Status:** done, interactive. Wired into the post as `#fig-bloch`,
referenced in the prose as `@fig-bloch`. The quantum counterpart of
Figure 1 (the classical simplex). Clicking the front of the ball picks a
pure direction, a Purity slider moves the state inward, and a plain-words
readout names the one yes/no measurement the state answers with certainty
(and how that certainty fades as the state mixes). The root *dynamics*
(applying `S`) live in Figure 4; this figure is the state-space explorer.

> **Note:** the click + Purity-slider machinery (projection `invert()`,
> the sinking marker, the slider) is shared with Figure 4. Figure 3 reuses
> it without the orbit; the readout here is the worded "certain question"
> rather than the four Bloch vectors of a trajectory.

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
poles `|0>`, `|1>` are blue-teal. The maximally mixed state `I/2` sits
*inside* the ball, so it is drawn **depth-cued**: a muted blue-grey dot
(`MIXED_RING #5e7886`), a little transparent, with a soft halo and a
muted label, so it reads as recessed in the middle rather than as a bold
foreground marker. (The flat 2D figures, 1 and 2, keep their solid
centre marker; the two Bloch balls, 3 and 4, use this recessed one.) The
wireframe and axes stay navy.

## Interaction (progressive enhancement)

The static SVG is the whole figure with JS off (the same ball renders).
The `<script>` then *adds* a click-to-pick-a-direction marker and a
Purity slider: clicking the front face inverts the orthographic
projection onto the camera-facing hemisphere to a pure direction `n`, the
slider `r` in `[0,1]` sets the state `r0 = r * n` (surface inward toward
`I/2`), and the marker sinks into the ball as purity drops (halo fades,
`opacity = 0.4 + 0.6 r`), the depth cue. The readout is plain words: it
names the one measurement the state answers with certainty (the poles are
the "0 or 1?" question), and as `r` drops it reports the fading agreement
(`(1+r)/2`) until, at the centre, every question is a coin flip. The
projection is read from the `<svg>` `data-*` attributes.

## Files

| file | role |
|------|------|
| `bloch_ball_figure.py` | generator for the SVG; geometry, viewing angles, wireframe density, and the emitted `data-*` projection attrs are constants at the top |
| `bloch_ball.svg` | the generated SVG (checked in), carrying the `data-*` projection attributes |
| `interactive.qmd` | the partial the post includes: scoped `<style>`, the inlined SVG, the Purity slider + readout, and the `<script>` |

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
