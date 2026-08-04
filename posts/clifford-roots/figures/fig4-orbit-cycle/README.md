# Figure 4: the d = 3 orbit cycle of h

**Status:** DONE, static. Built by `orbit_cycle_figure.py` and wired
into the higher-dimensions chapter
(`_05-clifford-higher-dimensions.qmd`) as `#fig-orbit`, referenced
from the prose as `@fig-orbit`, placed right after the grand cycle is
derived. The caption covers both the cycle (Ingredient 1) and the
antipodal vanishing pair (Ingredient 2).

**No d = 2 sibling is needed.** The qubit chapter's figure is
`fig5-continuum-grid` (`@fig-clifford-grid`), whose right panel
already draws the label plane `F_2^2` with an example `h` that is
exactly the qubit root's 3-cycle `(1,0) -> (0,1) -> (1,1) -> (1,0)`.
This figure generalises that right panel to `d = 3` and should reuse
its point-grid styling, so the reader meets the eight-ring already
knowing how to read it.

## What it should show

The grand orbit of the order-8 matrix `h` for `d = 3`: the eight
nonzero labels of the plane `F_3^2` arranged in the single cycle

```
(1,0) -> (0,1) -> (1,2) -> (2,2) -> (2,0) -> (0,2) -> (2,1) -> (1,1) -> (1,0)
```

laid out as a ring. The figure should mark the mirror pair where
`lambda` vanishes, here `(1,0)` and its antipode `(2,0)`, sitting at
opposite poles of the cycle and splitting it into two arcs of four
steps each. This is the picture behind the `(d^2 - 1)/2` bound: the
antipodal pairing is exactly what costs the factor of two.

The companion matrix is `h = [[0, 1], [1, 2]]` over `F_3` (companion
of the primitive polynomial `x^2 + x + 2`). The orbit above is its
action on column vectors starting from `(1,0)`.

## Suggested build

- An `orbit_cycle_figure.py` generator that places the eight labels
  evenly on a circle in cycle order, draws directed arrows between
  consecutive labels, and highlights the antipodal vanishing pair
  plus the two arcs in contrasting strokes.
- Navy structural palette and conventions as the other figures, and
  point-grid styling matching `fig5-continuum-grid`'s right panel.
  Note the purity colour scheme does NOT apply here: this is the
  label plane `F_d^2`, not a state space, so there is no purity to
  encode. Use a distinct accent for the highlighted vanishing pair /
  arcs.
- Output `orbit-d3.svg`.

## Interactive potential (optional, later)

A strong candidate for interactivity: let the reader pick an
`h in GL(2, F_d)` for small `d` (or step through the action vector by
vector) and see the orbit structure and where a valid `lambda` may
vanish. Keep the progressive-enhancement pattern: static SVG baseline,
interaction added on top, no-JS fallback. Because the orbit is pure
finite-field combinatorics, the geometry here is a layout choice
rather than a projection, so the "single source of truth" can be the
list of labels in cycle order emitted by the generator.

## To modify

Edit the constants at the top of `orbit_cycle_figure.py`,
regenerate, and re-inline the SVG body into `interactive.qmd`:

```bash
python orbit_cycle_figure.py orbit-d3.svg
# then re-copy the <svg>...</svg> body into interactive.qmd
```

No script to keep in sync (static figure). Captions live in the
chapter partial (no manual "Figure N" prefix).
