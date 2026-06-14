"""
Generate the static skeleton for Figure 2: the square-root channel
collapsing the probability simplex to its grey centre.

This figure is animated. The skeleton drawn here is only the fixed
scaffold the script animates on top of: the simplex outline (whose
vertices are the single source of truth for the geometry, read by the
script), the three pure-state corner labels in their identity colours,
the grey maximally mixed marker p0 at the centre, and empty layers the
script fills in.

Colour does two jobs, the same scheme as Figure 1. The three pure-state
corners carry identity colours, red, green, blue (e1, e2, e3). The
animated cloud of states is coloured by its barycentric RGB blend and
drains toward the grey centre p0 as the channel S mixes it. The channel
acts in two stages: S collapses the 2D cloud onto a 1D segment (rank-one
N), and a second S collapses that segment onto the single grey point
(N^2 = 0).

Usage:
    python trajectories_figure.py [output.svg]

Defaults to ./simplex-root-d3.svg.
"""

from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# Knobs
# ---------------------------------------------------------------------------

CANVAS = (640, 620)

# Simplex vertices, IDENTICAL to Figure 1 so the figures register. The
# script reads these from the outline polygon, in e1, e2, e3 order.
VERTEX_E1 = (140, 510)
VERTEX_E2 = (540, 430)
VERTEX_E3 = (310, 130)
VERTICES = (VERTEX_E1, VERTEX_E2, VERTEX_E3)

P0 = (
    (VERTEX_E1[0] + VERTEX_E2[0] + VERTEX_E3[0]) / 3,
    (VERTEX_E1[1] + VERTEX_E2[1] + VERTEX_E3[1]) / 3,
)

PURE = "#2d6f8f"               # simplex outline (blue-teal)
OUTLINE = "#233746"            # dark blue-grey (unused decorative text)
MUTED = "#829aa6"              # muted vector sublabels
CENTER = "#f5f7f8"             # p0 marker halo
GREY_CENTER = "#8a8f94"        # p0 marker dot (neutral grey, the "grey noise")

# Identity colours for the three corners, shared with Figure 1.
CORNER_COLOURS = ("#cc3b3b", "#2e9e5b", "#3b6fb0")  # e1 red, e2 green, e3 blue

FONT_FAMILY = "Georgia, 'Times New Roman', serif"
LABEL_SIZE = 22
VECTOR_LABEL_SIZE = 14
SIMPLEX_STROKE_W = 2.2

ARIA = ("The square-root channel collapsing the probability simplex to its "
        "grey centre in two steps. The three pure-state corners are coloured "
        "red, green, and blue; a cloud of states flows under the channel onto "
        "a line segment, then onto the single grey maximally mixed point.")


def build_svg():
    width, height = CANVAS
    p = []
    p.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg role="img" aria-label="{ARIA}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_FAMILY}">'
    )

    # simplex outline (vertices in e1, e2, e3 order: the geometry source)
    pts = " ".join(f"{x},{y}" for x, y in VERTICES)
    p.append(f'\n  <polygon class="tri" points="{pts}" fill="none" '
             f'stroke="{PURE}" stroke-width="{SIMPLEX_STROKE_W}" '
             f'stroke-linejoin="round"/>')

    # layers the script fills (order = paint order)
    p.append('\n  <g class="resting"></g>')
    p.append('\n  <g class="trails"></g>')
    p.append('\n  <g class="cloud"></g>')
    p.append('\n  <g class="hl"></g>')

    # maximally mixed state p0 (grey marker, always visible)
    p.append(f'\n  <circle cx="{P0[0]}" cy="{P0[1]}" r="9" fill="{CENTER}"/>')
    p.append(f'\n  <circle cx="{P0[0]}" cy="{P0[1]}" r="6" fill="{GREY_CENTER}"/>')

    # corner labels (identity colours) + probability vectors (muted), static
    specs = [
        (VERTEX_E1, 'e₁', '(1, 0, 0)', (-8, 28), (-8, 46), 'end', CORNER_COLOURS[0]),
        (VERTEX_E2, 'e₂', '(0, 1, 0)', (16, 8), (16, 26), 'start', CORNER_COLOURS[1]),
        (VERTEX_E3, 'e₃', '(0, 0, 1)', (0, -28), (0, -10), 'middle', CORNER_COLOURS[2]),
    ]
    for (vx, vy), lab, vec, (lx, ly), (vox, voy), anchor, col in specs:
        p.append(f'\n  <text x="{vx + lx}" y="{vy + ly}" text-anchor="{anchor}" '
                 f'font-size="{LABEL_SIZE}" font-style="italic" fill="{col}">{lab}</text>')
        p.append(f'\n  <text x="{vx + vox}" y="{vy + voy}" text-anchor="{anchor}" '
                 f'font-size="{VECTOR_LABEL_SIZE}" fill="{MUTED}">{vec}</text>')

    # p0 label (full strength)
    p.append(f'\n  <text x="{P0[0] + 16}" y="{P0[1] - 4}" font-size="{LABEL_SIZE}" '
             f'font-style="italic" fill="{OUTLINE}">p₀</text>')

    p.append('\n</svg>\n')
    return "".join(p)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "simplex-root-d3.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
