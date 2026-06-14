# Figure 2: the square-root channel collapsing the simplex (animated)

**Status:** done, animated. Wired into the post as `#fig-root-d3`,
referenced as `@fig-root-d3`.

## What it shows

A concrete square root of the `d = 3` bistochastic completely
depolarising channel, on the same triangle as Figure 1, shown as an
**animation** of the whole state space being crushed in two stages. We
use the specific bistochastic matrix

```
S = [ 1/2  1/2   0  ]
    [ 1/6  1/6  2/3 ]
    [ 1/3  1/3  1/3 ]
```

which satisfies `S^2 = P`. The animation makes the nilpotent structure
visible:

- **Beat 0.** A cloud of ~150 sampled states fills the triangle, each
  point coloured by its barycentric red/green/blue blend (so the cloud
  looks like a blurry RGB triangle).
- **Beat 1 (`S`).** Every point glides to `S(point)`. Because `S` acts on
  the deviations as the rank-one `N`, the 2D cloud **collapses onto a 1D
  line segment** through the centre. One dimension is gone.
- **Beat 2 (`S` again).** Because `N^2 = 0`, the segment **collapses onto
  the single grey centre** `p0`. Colours drain to grey on the way.
- Three highlighted **corner trajectories** (`e1, e2, e3`) draw trails in
  their identity colours; `e1` and `e2` merge onto the same intermediate
  point, the headline of the figure.

The three pure states take a two-step path to the centre:

```
e1 -> q_a -> p0
e2 -> q_a -> p0     (e1 and e2 MERGE at q_a)
e3 -> q_b -> p0
```

## Behaviour

- The animation **plays once when the figure scrolls into view**, then
  settles into a **resting view**: the labelled static trajectories
  (`Se₁ = Se₂` at the merge `q_a`, `Se₃` at `q_b`), the three identity
  coloured corner dots, and the grey `p0` marker.
- **Tap / click** anywhere on the figure to replay.
- `prefers-reduced-motion: reduce` skips the animation entirely and shows
  only the resting view. With JS off, the static skeleton (outline,
  corner labels, grey `p0`) renders unchanged.

## Files

| file | role |
|------|------|
| `trajectories_figure.py` | generator for the static **skeleton** SVG: the simplex outline (vertices in `e1,e2,e3` order, the geometry source), the three corner labels in identity colours, the grey `p0` marker, and the empty `resting / trails / cloud / hl` layers the script fills |
| `simplex-root-d3.svg` | the generated skeleton SVG (checked in) |
| `interactive.qmd` | the partial the post includes: a single `{=html}` block with the scoped `<style>`, the inlined skeleton SVG, and the animation `<script>` |
| `README.md` | this file |

The post includes the figure as a `::: {#fig-root-d3}` figure div with
`{{< include figures/fig2-simplex-root/interactive.qmd >}}`, the same
pattern as Figures 1 and 3.

## Geometry (single source of truth)

The simplex vertices are identical to Figure 1's
(`(140,510)/(540,430)/(310,130)`), so the two figures register exactly.
The script reads the three vertices from `polygon.tri` (in `e1,e2,e3`
order) and maps barycentric coordinates with
`b2c(p) = p1*V1 + p2*V2 + p3*V3`. The root `S` is a constant in the
script; every trajectory and the resting view are computed from it, so
the picture follows automatically if `S` is ever changed.

## Colour scheme

The three corners and `e1,e2,e3` labels use the identity colours
`CORNER_COLOURS` (red `#cc3b3b`, green `#2e9e5b`, blue `#3b6fb0`), shared
with Figure 1. The animated cloud is coloured by its barycentric RGB
blend and drains toward grey at the centre. Unlike the old static
version, this figure carries **no purity background field**: the moving
RGB cloud does that job now. The `p0` centre marker is a `#8a8f94` grey
dot under a white halo. Resting trajectories are drawn in the corner
colours at low opacity; the intermediate `q` dots are a neutral slate.

## To modify

- Geometry, corner colours, labels: edit the constants at the top of
  `trajectories_figure.py`, then regenerate:
  ```bash
  python trajectories_figure.py simplex-root-d3.svg
  ```
  Then rebuild `interactive.qmd` (it embeds the skeleton verbatim inside
  the `{=html}` block; re-paste the `<svg>…</svg>` body if the skeleton
  changes).
- Animation timing, cloud density, the matrix `S`: edit the constants at
  the top of the `<script>` in `interactive.qmd` (`A/MID/B`, `NPTS`, `S`).

## Out of scope (kept that way)

- The old click-to-trace interaction and the `S rho0 / S^2 rho0` readout
  panel were removed; the animation replaces them.
- Drawing the line through `q_a, q_b, p0` as a separate construct, and
  alternative roots.
