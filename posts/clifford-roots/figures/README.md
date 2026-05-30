# Figures for the Clifford-roots post

This directory holds everything related to the visualisations in
`../index.qmd`: source scripts, generated SVG/PNG assets, and any
interactive widgets.

## Convention

For each figure we keep:

- A **source script** (`.py` for matplotlib/numpy, `.ojs` for Observable JS,
  `.html` for hand-rolled D3, etc.) that fully regenerates the artefact.
- The **generated artefact** itself (`.svg` preferred for static figures,
  `.gif`/`.mp4` for animations, embedded `.ojs` for interactives).
- A short **caption draft** kept alongside the post (the figure caption
  in the `.qmd` is the source of truth, but keeping it visible here helps).

So a typical figure ends up as:

```
figures/
  simplex-d3.py            # script
  simplex-d3.svg           # generated, checked in
  simplex-root-d3.py
  simplex-root-d3.svg
  ...
```

## Static figures (matplotlib / similar)

Default tool: `matplotlib` with SVG output. Each script should be
runnable standalone:

```bash
python figures/simplex-d3.py
```

and should write its output to the same directory. We check the
generated SVGs into git so that `quarto render` does not need Python
on every machine that builds the site.

## Interactive widgets

For figures where reader interactivity earns its keep (e.g. "pick a
$3 \times 3$ stochastic matrix and watch the trajectory in the
simplex"), the natural tool in a Quarto site is **Observable JS**
(`ojs` code blocks inside the `.qmd`). Quarto has first-class support
for it, it runs entirely in the browser (no server needed for GitHub
Pages), and D3 is built in.

Candidate interactive moments for this post:

- §classical: reader chooses a $3 \times 3$ stochastic matrix (sliders
  or a convex combination of permutations) and sees its trajectory in
  the simplex.
- §reduction: reader picks an $h \in GL(2, \mathbb{F}_d)$ and sees its
  orbit structure on $\mathbb{F}_d^2$ for small $d$.
- §ingredient-h: reader steps through the action of a max-order $h$ on
  $\mathbb{F}_d^2$ vector by vector.

We will design these one at a time, not all up front.

## Animations

For animations (rather than interactives), `matplotlib.animation` →
GIF/MP4 is the lowest-friction path. Quarto embeds them with the same
`![]()` syntax as static images.
