# Figure 5: continuum vs. finite grid

**Status:** done, static. Wired into the post as `#fig-clifford-grid`,
referenced as `@fig-clifford-grid`. Lives in the "Clifford channels as
the playground" section, after the second motivation paragraph.

## What it shows

A two-panel contrast that motivates why the rigid Clifford family is the
right place to work: a Clifford channel's structural core is a map on
*finitely many* points, not a deformation of the continuous ball.

- **Left panel: the continuum.** A Bloch ball with the **same
  purity-gradient fill and latitude/longitude wireframe as Figures 3 and
  4** (same projection angles, latitudes, meridians, gradient stops, and
  teal silhouette), so it reads as the same object as the big balls
  elsewhere in the post. Three coloured coordinate axes emerge from the
  centre, each
  double-labelled with its Pauli name and its Weyl label: `X = (1,0)`
  (teal, lower-left, toward the viewer), `Z = (0,1)` (purple, up),
  `Y = (1,1)` (coral, right). A grey identity dot sits at the centre
  (no inline label; the caption explains it). Sub-label: *qubit states:
  a continuum*.
- **Right panel: the finite grid.** The label plane $\mathbb{F}_2^2$:
  four points on faint coordinate guides through the origin. The
  identity `(0,0)` is a grey dot, matching the grey identity dot at the
  centre of the Bloch ball on the left (so the identity reads the same on
  both sides); the every-copier-fixes-it role is carried by the prose and
  the caption, and by the `h` arrows visibly leaving it alone. The three
  nonzero points `(1,0)`, `(0,1)`, `(1,1)` are solid, each in the
  colour of its matching Bloch axis. Three curved arrows show one
  example homomorphism `h` as the 3-cycle
  `(1,0) -> (0,1) -> (1,1) -> (1,0)`, bowed outward from the centroid so
  the origin is visibly left untouched. Sub-label: *Weyl labels: a
  finite grid*.

**The point of the figure is the colour correspondence:** each axis on
the left is the same colour as its matching point on the right
(`X` <-> `(1,0)` teal, `Z` <-> `(0,1)` purple, `Y` <-> `(1,1)` coral,
identity neutral grey), so the axis<->point map is read off by colour.

**Caveat honoured:** the figure illustrates only `h` (the relabelling).
The other half of a Clifford channel, the amplitudes $\lambda$ that
stretch and kill coordinates, is not drawn, so neither figure nor
caption implies a Clifford channel is *just* an axis permutation. This is
the `d = 2` instance; the right panel generalises to a `d x d` grid of
`d^2` points (the orbit-cycle figure reuses this point-grid styling).

## Files

| file | role |
|------|------|
| `continuum_grid_figure.py` | generator; geometry and palette as constants at the top |
| `continuum-grid-d2.svg` | the generated static SVG (checked in) |
| `interactive.qmd` | the partial the post includes: scoped `<style>` plus the inlined SVG (no script: this figure is static) |
| `README.md` | this file |

The post includes the figure as a `::: {#fig-clifford-grid}` figure div
with `{{< include figures/fig5-continuum-grid/interactive.qmd >}}`, the
same pattern as Figures 1 and 3.

## Geometry and colour

Canvas `680 x 300`. Left ball centre `(170,150)`, radius `72`; the fill
and wireframe are ported from `bloch_ball_figure.py` (projection
`ALPHA = 35deg`, `ELEV = 20deg`, `LATITUDES`, `N_MERIDIANS`, gradient
stops) scaled to that centre/radius. Axis tips `Z (170,64)`,
`Y (268,140)`, `X (96,212)`. Right
points `(0,0) (440,230)`, `(1,0) (560,230)`, `(0,1) (440,110)`,
`(1,1) (560,110)`; the `h` arcs bow outward from the centroid of the
three nonzero points by `H_BOW`, trimmed by `H_PAD` so the arrowheads
clear the markers. A faint dashed divider sits at `x = 350`.

Palette: structure in the shared blue-grey (`AXIS #233746` text and
`h`-arrows, `GRID #829aa6` ball outline / guides). Three categorical
colours carry the correspondence: `TEAL #2d6f8f`, `PURPLE #6f5499`,
`CORAL #c25b4e`, with `GREY #7d8a91` for the identity. The teal matches
the post's `PURE`/state-space accent; purple and coral are added only
here, for categorical distinctness.

## To modify

Edit the constants at the top of `continuum_grid_figure.py` and
regenerate, then re-inline the SVG body into `interactive.qmd`:

```bash
python continuum_grid_figure.py continuum-grid-d2.svg
# then re-copy the <svg>...</svg> body into interactive.qmd
```

No script to keep in sync (static figure).
