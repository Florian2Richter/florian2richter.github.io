# Continuation: state-space figure and interactivity pilot

This is a focused-scope handover. The previous chat was a long working
session that covered the whole blog post; this continuation is **only
about the state-space figure** (figure 1 in the post) and adding
interactivity to it.

You do not need the thesis. You do not need the post text. You only
need the Python script that generates the figure, which is attached
separately, and the context below.

---

## What we are doing

Writing a technical blog post on a result from my 2010 diploma thesis:
**Clifford channels can divide the completely depolarising channel into
nearly as many discrete steps as the general quantum machinery allows.**
The blog post is in Quarto, hosted on GitHub Pages at
<https://florian2richter.github.io>, in the post directory
`posts/clifford-roots/`.

Figure 1 of the post is a static SVG showing the classical state space
for a three-outcome system: the 2-simplex sitting inside the positive
octant of $\mathbb{R}^3$. Three coordinate axes from the origin, a
filled triangular face spanning the three unit basis vectors, the
uniform distribution $p_0$ marked at the centroid.

The Python script that generates this figure (`state_space_figure.py`)
is attached. It is structured so that all geometry — canvas size,
vertex positions, axis endpoints — lives as named constants at the top.
Layers (axes / simplex / medians / ticks / vertex dots / labels /
centroid) are clearly separated with comment headers in the SVG output.

## Where we left off

The static figure is **done** and good enough to ship. The previous
chat finalised it: blue palette (a deliberately restrained
technical-illustration look, not the pinks of the thesis), dashed
medians hinting at the barycentric structure, red dot for $p_0$, both
symbolic names ($e_1, e_2, e_3$) and probability vectors
($(1,0,0)$, $(0,1,0)$, $(0,0,1)$) at each vertex.

## What this chat is for

**Pilot interactivity for figure 1.** The plan: keep the static SVG
exactly as it is — that is the baseline that survives in print, RSS,
PDF, screenshots, and any context where JavaScript fails — and layer
interactive behaviour on top as a progressive enhancement.

The interaction we want:

- When the user **hovers or clicks** inside the triangle, a marker
  appears at that point.
- A sibling display element shows the **probability vector
  $(p_1, p_2, p_3)$** corresponding to the clicked point, computed
  from the click position via barycentric coordinates relative to the
  three vertex positions.
- Optional but desirable: a small bar chart or three readouts showing
  the three probabilities live, so the reader sees the mapping
  "geometric point ↔ probability distribution."

The point of the pilot is to learn the technique on a low-stakes figure
before applying it to figures where interactivity matters more (the
trajectories figure, the orbit cycle figure). If the engineering for
this one is reasonable, we will reuse the pattern. If it turns out
painful, we retreat to static everywhere.

## Design constraints

1. **The static SVG must remain unchanged in appearance when JS fails.**
   The interactive layer is purely additive. A reader with JS disabled
   sees exactly what's there now.

2. **The implementation lives in the `.qmd` file**, embedded as raw
   HTML around the SVG. The Python script keeps generating the static
   SVG; the `.qmd` wraps it with a `<script>` and a sibling display
   `<div>` for the readouts.

3. **No external JS libraries** unless there is a compelling reason.
   The math is barycentric-coordinate conversion, which is a one-time
   ~20-line function. No D3, no React, no jQuery.

4. **The vertex positions used by the JavaScript must match the SVG.**
   The cleanest pattern: have the Python script also emit a small
   JSON or JS-constant block with the canonical vertex positions, so
   the JS reads them from a single source rather than the developer
   re-typing coordinates. Alternatively: read them from the SVG
   itself at load time by querying the polygon's `points` attribute.
   Either is fine; the second is more elegant.

5. **Time budget: roughly an hour of focused work, no more.** If we
   find ourselves wrestling with Quarto's HTML-passthrough
   conventions or with cross-browser SVG event-handling quirks beyond
   that, we stop and report.

## How to start this chat

1. Read this markdown.
2. Look at the attached `state_space_figure.py` to understand the
   figure's geometry.
3. Run the script (`python state_space_figure.py`) to get the SVG.
4. Open the SVG in a browser to confirm the rendering matches expectation.
5. Then propose a concrete plan for the interactive layer before
   writing code — what HTML structure, what JS, where it lives in the
   `.qmd` file.

## What is OUT of scope

- Redesigning the static figure. We are not iterating on colours,
  geometry, label positions, or any other static-visual decision.
- Animations for any figure. Interactivity is click-based, not
  time-driven.
- Other figures in the post (trajectories, Bloch ball, orbit cycle).
  Those are separate chats.
- The post text. Voice, structure, mathematical content — handled
  elsewhere.
- Adding new mathematical content to figure 1. The figure shows what
  it shows. The interactivity simply lets the reader sample it.

## Open questions to settle in this chat

- **Hover vs click.** Hover gives continuous feedback, click gives a
  more deliberate "I want to look at this point" feel. Mobile devices
  have no hover. I lean toward click with a persistent marker,
  optionally augmented by hover-preview on desktop.
- **Where does the readout live?** Below the figure, beside it, or
  inside the SVG itself (as a floating annotation)? Quarto's
  responsive layout tends to favour stacking on mobile, so
  below-or-beside is probably the way.
- **Reset behaviour.** Should a click outside the triangle clear the
  marker, or should it stay until another point inside is clicked?
- **Visual style of the marker.** Same red as $p_0$, or a different
  accent colour to mark "user-placed" vs. "structural"?

## Attached

`state_space_figure.py` — the Python script that generates the static
SVG. All geometry constants are at the top. The script writes its
output to `state_space.svg` by default; pass a different path as the
first argument to write elsewhere.

When you have a plan, share it before writing the implementation.
