# Figure 2: square-root trajectories on the simplex

**Status:** done, interactive. Wired into the post as `#fig-root-d3`,
referenced as `@fig-root-d3`.

## What it shows

A concrete square root of the `d = 3` bistochastic completely
depolarising channel, on the same triangle as Figure 1. We use the
specific bistochastic matrix

```
T = [ 1/2  1/2   0  ]
    [ 1/6  1/6  2/3 ]
    [ 1/3  1/3  1/3 ]
```

which satisfies `T^2 = P`. The three pure states take a two-step path to
the centre:

```
e1 -> q_a -> p0
e2 -> q_a -> p0     (e1 and e2 MERGE at q_a)
e3 -> q_b -> p0
```

- The simplex carries the same **purity field** as Figure 1 (blue-teal pure
  corners fading to a blue-grey centre).
- Starting points `e1, e2, e3` at the vertices are pure, so blue-teal.
- Intermediate points `q_a, q_b` are coloured by their own purity. `q_a`
  is already quite mixed, so it reads pale; `q_b` a little more blue-teal. `q_a`
  is drawn slightly larger because two trajectories arrive there.
  These are internal code names; in the figure the points are labelled as
  their images under the root `S`. `q_b = S e3` is shown as **`Se₃`**, and
  the merge point `q_a = S e1 = S e2` is shown as the equality
  **`Se₁ = Se₂`** (the cleanest way to name a point two pure states share).
- All arrows are **neutral grey** (three step-1, two converging on `q_a`;
  two step-2). Colour is reserved for purity, so the arrows carry only
  the dynamics; the dots draining blue-teal to blue-grey carry the erasure.
- The uniform distribution `p0` is a solid, fully opaque marker at the
  centre (white halo + dark `OUTLINE` dot), matching Figure 1, with its
  `(1/3, 1/3, 1/3)` coordinates labelled at full strength.

**The merge at `q_a` is the headline:** three step-1 arrows arrive but
only two step-2 arrows leave, so the figure shows information being lost
in a stage. This is `T` for the caption's "square root `S`"; it is one of
infinitely many roots (the prose notes others exist).

A true feature of this particular root: `q_b = (0, 2/3, 1/3)` has first
coordinate zero, so it lies on the `e2-e3` edge, and the `e3 -> q_b`
arrow rides along that edge.

## Files

| file | role |
|------|------|
| `trajectories_figure.py` | generator; geometry and palette as constants at the top. Computes the trajectory points directly from `T` (via `apply_T` and `barycentric_to_canvas`), so nothing in the picture is hand-placed |
| `simplex-root-d3.svg` | the generated static SVG (checked in) |
| `interactive.qmd` | the partial the post includes: scoped `<style>`, the inlined SVG, the readout, and the `<script>` for the click-to-trace layer |
| `README.md` | this file |

The post includes the figure as a `::: {#fig-root-d3}` figure div with
`{{< include figures/fig2-simplex-root/interactive.qmd >}}`, the same
pattern as Figures 1 and 3.

## Geometry (single source of truth)

The simplex vertices are identical to Figure 1's
(`(140,510)/(540,430)/(310,130)`), so the two figures register exactly.
Every point is placed by `barycentric_to_canvas(p) = p1*V1 + p2*V2 +
p3*V3`. The script computes `q_a, q_b, p0` by applying `T`, so the
picture stays correct if `T` is ever changed.

## Colour scheme

Blue-grey scheme shared with Figure 1: `AXIS #233746` labels, `GRID
#829aa6` grid lines, blue-teal `PURE #2d6f8f` (pure) fading to blue-grey
`MIXED #d6e5ea` (maximally mixed). Mixed dots get a dark blue-teal
`#1c4a60` outline. Default-trajectory arrows are neutral grey. The user
trajectory (every moving object) is a strong blue `STATE #1565c0`
(dark-blue `#0d3f8f` stroke), with the placed point also set apart by
**shape** (a square).

## To modify

- Edit the constants at the top of `trajectories_figure.py` (palette,
  arrow trims, dot sizes, label sizes) and regenerate:
  ```bash
  python trajectories_figure.py simplex-root-d3.svg
  ```
- The matrix `T` is a constant too; change it and every point in the
  figure follows, because the trajectories are computed, not hand-placed.

## Interactive layer

Clicking inside the simplex drops a starting distribution `rho0` as a
**square** (distinct in shape from the round structural dots), coloured
by its purity, then shows `S rho0` and `S^2 rho0` as blue dots
joined by blue arrows, and a readout of the three probability vectors
`rho0`, `S rho0`, `S^2 rho0`. The second image always lands on `p0`,
which the reader can verify for any point they pick. On desktop a faint
blue dot previews where a click would land.

The figure starts by showing the three baked pure-state trajectories.
**On a click, those three default trajectories vanish** and only the
reader's chosen trajectory is drawn; a click outside the triangle
restores the defaults. The toggle works by hiding every
`<g class="default-traj">` group (the step arrows, the `q_a`/`q_b` dots,
and their labels) via `display:none`, set by `setDefaults()` in the
script. The `p0` marker and the `e1/e2/e3` vertex dots are outside those
groups, so they stay put.

The script reads the vertices from the polygon (single source of truth)
and holds the root `S` as a constant that must stay in sync with the
generator's `T`. It is plain JS, no libraries. With JS off, the static
figure with its three default trajectories renders unchanged (the
`default-traj` groups are only hidden by script, never by default).

Out of scope (kept that way): drawing the line through `q_a, q_b, p0`
(the prose can mention it as a "did you notice"), alternative roots, and
animation.
