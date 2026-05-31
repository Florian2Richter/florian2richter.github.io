# Figures for the clifford-roots post

This directory holds the figures for `posts/clifford-roots/index.qmd`,
organised so that **each figure is self-contained and can be developed
or modified on its own, without touching the blog post**. The post only
*includes* a finished figure; it never carries the figure's source.

## Layout: one folder per figure

```
figures/
  README.md                 <- this file (the system + status)
  fig1-state-space/         <- Figure 1: classical 2-simplex (DONE, interactive)
  fig2-simplex-root/        <- Figure 2: square-root trajectories (PLANNED)
  fig3-bloch-ball/          <- Figure 3: Bloch ball (DONE, interactive)
  fig4-orbit-cycle/         <- Figure 4: the d=3 orbit cycle (PLANNED)
```

Each finished figure folder contains, by convention:

| file | what it is |
|------|------------|
| `README.md` | the single self-contained doc: what the figure shows, the design knobs and constraints, how to build and modify it, how it is wired in |
| `*_figure.py` | the generator: emits the **static** SVG, all geometry as constants at the top |
| `*.svg` | the generated static SVG (the artifact that ships and survives with JS off) |
| `interactive.qmd` | the partial the post includes: a single `{=html}` block with the inlined SVG plus a progressive-enhancement readout and `<script>` |

The original task specs and handover notes have been summarised into each
figure's `README.md`, so the folder carries only the working pipeline plus
its one doc.

## The pattern: progressive enhancement

Every interactive figure is built as a **purely additive** layer on top
of a static SVG:

1. A Python generator emits a static SVG. This is the baseline that
   survives in print, RSS, PDF, screenshots, and any context where
   JavaScript fails or is disabled.
2. `interactive.qmd` inlines that SVG **verbatim** and adds a scoped
   `<style>`, a readout panel, and a `<script>`. The script only *adds*
   overlay elements (markers, guides) and updates the readout. It never
   redraws or mutates the static SVG.
3. With JavaScript off, the reader sees exactly the static figure and a
   quiet, empty readout. Nothing is allowed to make the figure depend on
   JS to appear. The SVG is inlined (never `fetch()`ed) for this reason.

Geometry has a **single source of truth**: the script reads the figure's
geometry from the SVG itself (the `<polygon points>` for Figure 1, the
`data-*` projection attributes for Figure 3), so nothing is retyped and
the interaction stays correct if the figure is regenerated.

## Colour scheme: purity

Across the three **state-space** figures (simplex, trajectories, Bloch
ball) the *background field* encodes **purity**, the quantity the post
is about. The field is a calm blue-teal where states are pure, fading to
a soft blue-grey at the maximally mixed state (a tinted centre, never
white), which is drawn as a faint hollow ring (de-emphasised, but
locatable). The same notion drives all three:

- classical purity is the collision probability `sum_i p_i^2`, from `1/d`
  (uniform) to `1` (pure);
- qubit purity is `tr(rho^2) = (1 + r^2)/2`, from `1/2` (centre) to `1`
  (surface).

So "erasure" reads visually as the field draining from blue-teal to
blue-grey, and the Bloch ball's "inside the sphere" depth is the same
language in 3D. The blue-grey scientific palette:

- field high end (pure / boundary / pure-state dots): `PURE #2d6f8f`
- field low end (maximally mixed): `MIXED #d6e5ea`
- axes and text labels: `AXIS #233746`
- grid lines (medians, wireframe): `GRID #829aa6`
- centre marker fill: `CENTER #f5f7f8`, with a visible blue-grey outline

The **current sampled state** (the interactive marker the reader places)
is a contrasting muted **amber `#bf6f30`**, so it pops against the blue
field. In Figure 2 the whole user trajectory is amber; the placed point
is also set apart by **shape** (a square). The static default
trajectories there use neutral-grey arrows.

Figure 4 (the orbit cycle) is the label plane `F_d^2`, not a state
space, so purity does not apply there; it uses its own scheme.

## How a figure is wired into the post

In `index.qmd`, each figure is a Quarto figure div that includes the
partial and carries the caption:

```markdown
::: {#fig-simplex-d3}

{{< include figures/fig1-state-space/interactive.qmd >}}

The caption goes here, with math like $p_0$ if needed.

:::
```

- The `#fig-...` id makes it a numbered, cross-referenceable figure.
- The prose references it with `@fig-...`, which renders as "Figure N".
  Every figure in the post is referenced from the text.
- Captions are **not** manually prefixed with "Figure N"; Quarto numbers
  them automatically.

The figure ids currently in use: `#fig-simplex-d3` (1), `#fig-root-d3`
(2), `#fig-bloch` (3), `#fig-orbit` (4).

## To modify a figure

1. Edit the generator's constants and rerun it to regenerate the SVG
   (e.g. `python fig1-state-space/state_space_figure.py
   fig1-state-space/state_space.svg`).
2. Re-copy the new SVG body (everything from `<svg ...>` to `</svg>`)
   into the `interactive.qmd` partial, replacing the old inline SVG. The
   `<script>` needs no edits; it re-reads the geometry from the SVG.
3. Re-render the post (`quarto render posts/clifford-roots/index.qmd`)
   and check the figure. No change to `index.qmd` is required.

See each figure's own `README.md` for the specifics.

## Status

| # | figure | id | state |
|---|--------|----|-------|
| 1 | classical state space (2-simplex) | `fig-simplex-d3` | done, interactive |
| 2 | square-root trajectories on the simplex | `fig-root-d3` | **planned** (no generator yet; placeholder image) |
| 3 | Bloch ball (qubit state space) | `fig-bloch` | done, interactive |
| 4 | the d=3 orbit cycle of h | `fig-orbit` | **planned** (no generator yet; placeholder image) |

Figures 2 and 4 currently render as broken-image placeholders in the
post (their SVGs do not exist yet). Their folders hold a README sketching
what they should become.

## A note on CSS

Each interactive figure carries its own scoped `<style>` block inside its
partial (`.simplex-interactive` for Figure 1, `.bloch-interactive` for
Figure 3). This keeps each figure fully self-contained. If a third
interactive figure is added, consider factoring the shared readout styles
into the site's `styles.css` so the common rules appear once.
