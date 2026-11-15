# Figure 3b / Figure 4: Bloch-ball root, animated

**Status:** done, animated. Wired into the post as `#fig-bloch-root`,
referenced as `@fig-bloch-root`; it renders as **Figure 4**. Sits in
"The quantum upgrade" section, right after Figure 3 (the Bloch ball state
space). This is the quantum counterpart of Figure 2 (the classical
square-root collapse animation): both play the root crushing a cloud of
states to the centre in stages. The interactive state-space *pick* now
lives in Figure 3; this figure is the animation.

## What it shows

The quantum analogue of Figure 2: the maximal qubit root `S` driving
every state to the maximally mixed centre `I/2` in *stages*, not in one
shot. It is a concrete witness that the quantum bound `d^2 - 1 = 3` is
attained at `d = 2`.

On the Bloch vector, `S` acts as

```
(r1, r2, r3)  ->  (r2/2, r3/2, 0)
```

so each step shrinks the vector and rotates it onto the next axis
(`z -> y -> x -> 0`). Three pure axis states make the
direction-dependent timing visible:

```
(0,0,1) -> (0,1/2,0) -> (1/4,0,0) -> 0    3 steps  (HERO, maximal order)
(0,1,0) -> (1/2,0,0) -> 0                  2 steps
(1,0,0) -> 0                               1 step   (x-axis: in the kernel)
```

All intermediate points lie inside the ball (radii 1, 1/2, 1/4, 0), so
they render cleanly. The points are computed directly from the map, not
hand-placed.

## Style and colour

Same sphere rendering, projection (`ALPHA=35deg`, `ELEV=20deg`), axes
(`x, y, z`), poles (`|0>`/`|1>`), wireframe and purity gradient as
Figure 3 (`bloch_ball_figure.py`); the projection helpers are copied so
the figure is self-contained.

- **Points** are coloured by purity (`t = r^2`): blue-teal on the
  surface (pure), fading to soft blue-grey toward the centre, the shared
  convention from Figures 1 and 2. Pale points get a dark `#1c4a60`
  outline so they stay visible.
- **Arrows** carry the dynamics. The two ordinary orbits are neutral
  grey (`ARROW_GREY #829aa6`), as the baked default trajectories in
  Figure 2. The **hero z-pole orbit is strong blue** (`HERO_BLUE
  #1565c0`, dark `#0d3f8f` stroke / start dot), thicker, because it takes
  all three steps and so realises the order-3 bound. The hero start `|0>`
  is drawn slightly larger.
- **Depth fade.** Both arrows and points lose opacity as the orbit sinks
  toward `I/2`: opacity follows the Bloch-vector magnitude (`depth_op` for
  arrows, `dot_op` for points, which fade a touch more), so the orbit dims
  as it spirals into the centre. The interactive trajectory uses the same
  rule, and the user-placed start circle additionally fades its halo and
  dims (`0.4 + 0.6 r`) as the Purity slider sinks it inward, the depth cue
  of the original Bloch figure. Surface start states stay crisp.
- **Centre `I/2`** is depth-cued (it sits inside the ball): a muted
  blue-grey dot (`MIXED_RING #5e7886`), a little transparent, with a soft
  halo and muted label, matching Figure 3. The flat 2D figures (1, 2)
  keep their solid centre marker; the two Bloch balls (3, 4) use this
  recessed one.

## Files

| file | role |
|------|------|
| `bloch_root_figure.py` | generator; geometry, palette, projection and the three trajectories as constants/lists at the top. Points are computed from the map, not hand-placed. Emits `data-*` projection attributes on the `<svg>` tag, and wraps the three default orbits in `<g class="default-traj">` so the script can toggle them |
| `bloch-root-d2.svg` | the generated static SVG (checked in): the ball plus the three default orbits |
| `interactive.qmd` | the partial the post includes: scoped `<style>`, the inlined SVG, the readout, and the `<script>` for the click-to-trace layer |
| `README.md` | this file |

## Animation layer

Mirrors Figure 2's collapse animation, on the Bloch ball. The generator
emits only the **skeleton**: the ball *silhouette*, the latitude and
longitude wireframe, and the coordinate axes (poles, `I/2`, axis labels),
plus the `data-*` projection attributes and empty
`resting / trails / cloud / hl` layers. The wireframe is the same set of
guide lines as Figure 3, at the same opacities, so the two balls read as
the same object; it sits behind every dynamic layer. The purity *field*
(the tinted interior gradient) stays off: here the cloud carries the
purity colouring, and a tinted background would fight it. The script
builds everything dynamic from the map `applyS(r) =
[r1/2, r2/2, 0]` (thesis eq. 4.19; `S^3 = 0`):

- **Resting view** (shown at rest, and as the reduced-motion fallback):
  the three pure axis orbits drawn as arrows + purity-coloured dots, the
  `z`-pole hero in blue (3 steps), the `y`- and `x`-axis orbits in grey
  (2 and 1 step).
- **Animation** (plays once on scroll into view via `IntersectionObserver`,
  replays on tap): a cloud of ~150 Bloch vectors sampled in the ball is
  driven through the three stages `r0 -> S r0 -> S^2 r0 -> 0`, each move
  eased with a short dwell between. Cloud points are coloured by purity
  and depth-faded (back of the ball paler, `0.45 + 0.55 * frontness`);
  the three axis orbits are highlighted with trailing polylines. On
  finish it settles back to the resting view.

The script reads the projection from the `<svg>` `data-*` attributes
(single source of truth); its `project()` matches the generator exactly.
Plain JS, no libraries. With JS off or `prefers-reduced-motion`, the
static ball plus the resting orbits is what shows.

## To modify

- Edit the constants / trajectory lists at the top of
  `bloch_root_figure.py`, then regenerate:
  ```bash
  python bloch_root_figure.py bloch-root-d2.svg
  ```
  Then re-copy the new SVG body into `interactive.qmd`, replacing the old
  inline SVG, keeping the `role`/`aria-label` on the opening `<svg>` tag.
- The map and the three trajectories are the whole content of the figure;
  do not substitute a different map or different points.

## Verifying visually (headless)

```bash
python3 bloch_root_figure.py bloch-root-d2.svg
inkscape "$(pwd)/bloch-root-d2.svg" --export-type=png \
  --export-filename="$(pwd)/_preview.png" -w 760
# read _preview.png, then: rm _preview.png   (do not commit previews)
```
