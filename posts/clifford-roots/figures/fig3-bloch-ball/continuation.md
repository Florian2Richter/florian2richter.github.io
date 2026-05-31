# Continuation: Bloch ball figure

Focused-scope handover for a new chat. This one builds the **qubit
state space figure** (figure 3 in the blog post): the Bloch ball.

You do not need the thesis or the post text. You only need the context
below and the previous figure's Python script for reference, which is
attached.

---

## Context

The blog post is in Quarto, hosted at <https://florian2richter.github.io>,
post directory `posts/clifford-roots/`. We are building static SVG
figures via Python scripts, with optional interactive overlays added
in the `.qmd` file as a progressive enhancement.

Figure 1 of the post (the classical 3-outcome simplex) is done. Its
Python generator (`state_space_figure.py`) and its successful
interactive overlay are the templates this figure should follow:

- Restrained technical-illustration aesthetic (not a pastel/decorative
  look).
- Blue palette: `#a8c5d8` fill at moderate opacity, `#1a3550` dark
  outlines and labels, `#3a5a72` muted secondary, `#c0392b` red accent
  for the centre/origin marker, Georgia serif font.
- All geometry as named constants at the top of the Python script,
  layers separated by comment headers in the SVG output.
- Static SVG looks complete on its own. Interactivity layers on top.

The Python script for figure 1 is attached as a reference for both
the colour palette and the code structure.

## What this figure is

The **Bloch ball**: the state space of a single qubit, in
3-dimensional real space. The post will use this figure to make one
structural point: where the classical simplex was 2-dimensional
($d - 1 = 1$ for the classical bit, $d - 1 = 2$ for the 3-outcome
case), the qubit state space is 3-dimensional ($d^2 - 1 = 3$). The
jump in dimension is what drives the jump in the divisibility bound
from $d - 1$ to $d^2 - 1$.

The figure must convey:

1. **Pure states live on the surface** of the ball, mixed states in
   the interior.
2. **The maximally mixed state $\mathbb{1}/2$ sits at the centre.**
3. **Antipodal points on the surface are orthogonal pure states**
   (e.g. $|0\rangle$ and $|1\rangle$ at the poles).
4. **Three real parameters** $(r_x, r_y, r_z)$ describe a state, in
   contrast to the simplex's two — this is the dimension-count fact
   the post will build on.

Points (1)–(3) the figure carries directly; (4) the surrounding prose
handles, but the figure should have visible $x$, $y$, $z$ axes so the
"three parameters" framing has somewhere to land.

## Design decisions, locked in

**Wireframe sphere, not opaque shading.** The interior of the ball is
the structurally important region (mixed states), so we should not
hide it behind an opaque surface. Latitude lines and longitude lines
give the "this is a 3D ball" feeling while keeping the inside visible.

**Static pre-baked 3D projection.** The Python script computes the 2D
projection of the wireframe in 3D and emits static SVG. No rotation,
no drag interaction. A reader who wants to imagine the other side
does so in their head — this is a textbook figure, not a toy. The
view is fixed: $z$-axis vertical, viewer looking from slightly above
the equator (a conventional Bloch-ball orientation).

**Three pure states labelled.** $|0\rangle$ at the north pole,
$|1\rangle$ at the south pole, and $|+\rangle$ on the equator at the
front. Other pure states ($|-\rangle$, $|\pm i\rangle$) are noted in
the prose but not on the figure, to keep visual clutter down.

**Maximally mixed state $\mathbb{1}/2$ at the centre**, marked with
the same red accent as $p_0$ in the simplex figure. Visual consistency
between "the centre of the simplex" and "the centre of the ball" is
deliberate — both are the maximally mixed state for their respective
systems.

**Coordinate axes $x$, $y$, $z$ visible**, labelled, emerging from
the centre. The $z$-axis goes through the poles. These do real work:
they let the prose refer to "three real parameters" with a concrete
referent.

**No axes labelled "$r_x, r_y, r_z$"** — just $x$, $y$, $z$. The
$r$-vector framing is fine in prose, but on the figure the simpler
labels are cleaner.

## Design decisions still open

These are for the new chat to propose on:

- **How many latitude / longitude lines.** Too few looks bare; too
  many looks busy. A reasonable starting point: maybe 5 latitude
  circles (poles + equator + 2 between) and 8 longitude meridians.
  The chat should iterate visually.
- **How to convey "front" vs "back" of the sphere.** Conventional
  technique: solid lines for the visible hemisphere, dashed lines for
  the hidden hemisphere. This is essential for the figure to read as
  3D rather than flat.
- **Whether to draw the equator as a distinguished circle.** A
  slightly heavier stroke for the equator (and possibly the prime
  meridian) helps the eye see the sphere's orientation.
- **Whether to add a faint translucent fill** to suggest the ball's
  interior, or leave it purely as wireframe lines.
- **Final positioning of axes.** Do they extend visibly outside the
  ball, like the simplex figure's axes do, or stop at the surface?
  My guess: extend slightly outside, with arrowheads, for visual
  consistency with figure 1.

## Interactivity (pilot follow-up)

After the static figure is done and looks right, we add an interactive
overlay in the same spirit as figure 1's: click or hover on the
visible surface, see the Bloch vector $(r_x, r_y, r_z)$ and optionally
the density matrix

$$\rho = \tfrac{1}{2}(I + r_x \sigma_x + r_y \sigma_y + r_z \sigma_z).$$

**Constraint:** interactivity is only for points on the **visible
front hemisphere**. The user can't click on the back of the ball.
Prose will note that "antipodal points are also pure states" — the
figure doesn't have to demonstrate that interactively.

**Mapping click to 3D point.** Given a click at 2D position $(u, v)$
on the canvas, recover the 3D Bloch vector by inverting the projection.
For a click *inside* the visible disc, the projected 3D point is
the front-hemisphere preimage (the one with $r_y > 0$, if $y$ points
out of the screen). For a click outside the disc, no readout.

This is more interesting math than the simplex's barycentric
inversion — it's a fun small problem to work through. The chat should
expect to derive the inversion explicitly rather than copy-paste a
formula.

**Time budget for the static figure: ~1 hour.** For the interactive
layer on top: another ~1 hour, since the inverse-projection math is
trickier than the barycentric case. Total ~2 hours of focused work.
If either piece blows past its budget, stop and report.

## How to start

1. Read this markdown.
2. Look at the attached `state_space_figure.py` to absorb the colour
   palette and code structure.
3. Sketch the static figure mentally — how the wireframe is laid out,
   where the axes go, where the labels sit.
4. Propose a concrete plan for the static figure before writing code:
   the projection convention you'll use (e.g. orthographic with a
   specific viewing angle), the number of wireframe lines, the layer
   structure.
5. Once we agree, implement, render, iterate until it looks right.
6. Then move to interactivity.

## What is OUT of scope

- Other figures (trajectories, orbit cycle). Separate chats.
- The classical simplex (figure 1) — already done.
- Rotation, drag, animation. We are doing a fixed view with click
  interactivity only.
- The post's text. Voice and structure handled elsewhere.
- WebGL, Three.js, or any other 3D library. Pure SVG with a small
  JavaScript projection function for the interactive layer.
- Showing density matrices for points in the **interior** of the
  ball as part of the interactive readout. We can mention in prose
  that interior points are mixed states, but the click-readout
  focuses on surface points (pure states) since they have a cleaner
  interpretation.

## Attached

`state_space_figure.py` — reference for palette and code structure.
The Bloch ball figure will be a different script in the same
directory: `bloch_ball_figure.py`.
