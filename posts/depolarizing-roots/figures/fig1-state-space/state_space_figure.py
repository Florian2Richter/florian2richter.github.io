"""
Generate the classical state space figure for a 3-outcome system.

The simplex (probability distributions over three outcomes) is drawn as
a 2D face sitting inside the positive octant of R^3. Three coordinate
axes from the origin show the embedding; the triangular face spans the
three unit basis vectors.

Colour does two jobs here. The simplex fill encodes PURITY: a
distribution's purity is the collision probability sum_i p_i^2, which
runs from 1/d at the uniform distribution (maximally mixed) to 1 at a
pure state. We fill the simplex with this field, blue-teal and saturated
at the corners, fading to a pale glow at the maximally mixed centre. On
top of that, the three pure-state corners are marked in their own
identity colours, red, green, and blue, so the reader sees three
distinct pure colours (e1 red, e2 green, e3 blue) blending toward the
grey maximally mixed state p0 at the centre. That grey centre is the
"grey noise" the post opens with. p0 is drawn as a solid, fully visible
grey marker with its coordinates labelled at full strength.

Usage:
    python state_space_figure.py [output.svg]

Defaults to ./state_space.svg.
"""

from __future__ import annotations

import sys


# ---------------------------------------------------------------------------
# Knobs -- edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (640, 620)  # viewBox width, height

ORIGIN = (310, 430)

# Simplex vertices (where each axis hits "1") in canvas coordinates.
VERTEX_E1 = (140, 510)   # front-left ("out of the page")
VERTEX_E2 = (540, 430)   # to the right
VERTEX_E3 = (310, 130)   # upward
VERTICES = (VERTEX_E1, VERTEX_E2, VERTEX_E3)

# Axes extend past the simplex vertices (for arrowheads).
AXIS_E1_END = (95, 530)
AXIS_E2_END = (590, 430)
AXIS_E3_END = (310, 75)

P0 = (
    (VERTEX_E1[0] + VERTEX_E2[0] + VERTEX_E3[0]) / 3,
    (VERTEX_E1[1] + VERTEX_E2[1] + VERTEX_E3[1]) / 3,
)

# Blue-grey scientific palette. Colour encodes purity: blue-teal (pure)
# fading to a soft blue-grey (maximally mixed), never to white.
OUTLINE = "#233746"            # axes, ticks, text labels (dark blue-grey)
MUTED = "#829aa6"              # grid lines (medians) and muted sublabels
PURE = "#2d6f8f"               # boundary + pure-state dots (blue-teal)
PURE_RGB = (45, 111, 143)      # field high end (pure)
MIXED_RGB = (214, 229, 234)    # field low end (maximally mixed, soft blue-grey)
MIXED_RING = "#5e7886"         # the faint ring at p0
CENTER = "#f5f7f8"             # centre marker halo
GREY_CENTER = "#8a8f94"        # centre marker dot (neutral grey, the "grey noise")

# Identity colours for the three pure-state corners (e1, e2, e3).
# Distinct from the purity field; these say *which* pure state, not how pure.
CORNER_COLOURS = ("#cc3b3b", "#2e9e5b", "#3b6fb0")  # e1 red, e2 green, e3 blue

SIMPLEX_FILL_OPACITY = 0.9
MESH_N = 26                    # triangular subdivisions of the purity field

FONT_FAMILY = "Georgia, 'Times New Roman', serif"
LABEL_SIZE = 22
VECTOR_LABEL_SIZE = 14

SIMPLEX_STROKE_W = 2.2
AXIS_STROKE_W = 1.8
TICK_STROKE_W = 1.6
MEDIAN_STROKE_W = 0.9
MEDIAN_OPACITY = 0.22


# ---------------------------------------------------------------------------
# Purity -> colour
# ---------------------------------------------------------------------------

def purity_t(p):
    """Normalised purity of a distribution p: 0 at the uniform
    distribution, 1 at a pure state. t = (sum p_i^2 - 1/3) / (1 - 1/3)."""
    s = sum(x * x for x in p)
    return max(0.0, min(1.0, (s - 1.0 / 3) / (2.0 / 3)))


def purity_colour(t):
    """Lerp from the soft blue-grey (maximally mixed) to blue-teal (pure)."""
    r = round(MIXED_RGB[0] + t * (PURE_RGB[0] - MIXED_RGB[0]))
    g = round(MIXED_RGB[1] + t * (PURE_RGB[1] - MIXED_RGB[1]))
    b = round(MIXED_RGB[2] + t * (PURE_RGB[2] - MIXED_RGB[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


def barycentric_to_canvas(p):
    x = sum(p[i] * VERTICES[i][0] for i in range(3))
    y = sum(p[i] * VERTICES[i][1] for i in range(3))
    return (x, y)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def tick_perpendicular(point, axis_direction, length=14):
    ax, ay = axis_direction
    norm = (ax ** 2 + ay ** 2) ** 0.5
    px, py = -ay / norm, ax / norm
    cx, cy = point
    return (
        (cx - length / 2 * px, cy - length / 2 * py),
        (cx + length / 2 * px, cy + length / 2 * py),
    )


def midpoint(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def bary_grid(a, b, n):
    """Barycentric coords of grid point (a, b) at subdivision n."""
    return (a / n, b / n, (n - a - b) / n)


# ---------------------------------------------------------------------------
# SVG construction
# ---------------------------------------------------------------------------

def build_svg():
    width, height = CANVAS
    parts = []

    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="{FONT_FAMILY}">'
    )

    parts.append(f'''
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{OUTLINE}"/>
    </marker>
  </defs>''')

    # --- Layer 1: axes behind the simplex ---
    parts.append('\n  <!-- Coordinate axes -->')
    for end in (AXIS_E1_END, AXIS_E2_END, AXIS_E3_END):
        parts.append(
            f'\n  <line x1="{ORIGIN[0]}" y1="{ORIGIN[1]}" '
            f'x2="{end[0]}" y2="{end[1]}"\n'
            f'        stroke="{OUTLINE}" stroke-width="{AXIS_STROKE_W}"\n'
            f'        marker-end="url(#arrow)"/>'
        )

    # --- Layer 2: the purity field (triangular mesh) ---
    parts.append('\n\n  <!-- Purity field: blue-teal at the pure corners, '
                 'pale at the maximally mixed centre -->')
    parts.append('\n  <g stroke-linejoin="round">')
    n = MESH_N

    def tile(corners):
        cen = tuple(sum(c[k] for c in corners) / 3 for k in range(3))
        colour = purity_colour(purity_t(cen))
        pts = " ".join(
            "%.2f,%.2f" % barycentric_to_canvas(c) for c in corners
        )
        return (f'\n    <polygon points="{pts}" fill="{colour}" '
                f'fill-opacity="{SIMPLEX_FILL_OPACITY}" '
                f'stroke="{colour}" stroke-width="0.6" '
                f'stroke-opacity="{SIMPLEX_FILL_OPACITY}"/>')

    for a in range(n):
        for b in range(n - a):
            up = (bary_grid(a, b, n), bary_grid(a + 1, b, n),
                  bary_grid(a, b + 1, n))
            parts.append(tile(up))
            if a + b < n - 1:
                down = (bary_grid(a + 1, b, n), bary_grid(a, b + 1, n),
                        bary_grid(a + 1, b + 1, n))
                parts.append(tile(down))
    parts.append('\n  </g>')

    # --- Layer 3: crisp simplex outline on top of the mesh ---
    points_str = " ".join(f"{x},{y}" for x, y in VERTICES)
    parts.append('\n\n  <!-- Simplex outline -->')
    parts.append(
        f'\n  <polygon points="{points_str}" fill="none" '
        f'stroke="{PURE}" stroke-width="{SIMPLEX_STROKE_W}" '
        f'stroke-linejoin="round"/>'
    )

    # --- Layer 4: medians (faint barycentric hint) ---
    parts.append('\n\n  <!-- Medians -->')
    parts.append(
        f'\n  <g stroke="{MUTED}" stroke-width="{MEDIAN_STROKE_W}" '
        f'stroke-opacity="{MEDIAN_OPACITY}" stroke-dasharray="4,5">'
    )
    for v, opp in ((VERTEX_E1, midpoint(VERTEX_E2, VERTEX_E3)),
                   (VERTEX_E2, midpoint(VERTEX_E1, VERTEX_E3)),
                   (VERTEX_E3, midpoint(VERTEX_E1, VERTEX_E2))):
        parts.append(f'\n    <line x1="{v[0]}" y1="{v[1]}" '
                     f'x2="{opp[0]}" y2="{opp[1]}"/>')
    parts.append('\n  </g>')

    # --- Layer 5: tick marks at the vertices ---
    parts.append('\n\n  <!-- Unit tick marks -->')
    for vertex in VERTICES:
        axis_dir = (vertex[0] - ORIGIN[0], vertex[1] - ORIGIN[1])
        (sx, sy), (ex, ey) = tick_perpendicular(vertex, axis_dir, length=14)
        parts.append(
            f'\n  <line x1="{sx:.1f}" y1="{sy:.1f}" '
            f'x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{OUTLINE}" stroke-width="{TICK_STROKE_W}"/>'
        )

    # --- Layer 6: pure-state dots (identity colours: red, green, blue) ---
    parts.append('\n\n  <!-- Pure states (identity colours: e1 red, e2 green, e3 blue) -->')
    for (vx, vy), colour in zip(VERTICES, CORNER_COLOURS):
        parts.append(f'\n  <circle cx="{vx}" cy="{vy}" r="6" fill="{colour}"/>')

    # --- Layer 7: maximally mixed state p0 (solid grey marker, fully visible) ---
    parts.append('\n\n  <!-- Maximally mixed state p0 (solid grey marker) -->')
    parts.append(
        f'\n  <circle cx="{P0[0]}" cy="{P0[1]}" r="9" fill="{CENTER}"/>'
    )
    parts.append(
        f'\n  <circle cx="{P0[0]}" cy="{P0[1]}" r="6" fill="{GREY_CENTER}"/>'
    )

    # --- Layer 8: labels ---
    parts.append('\n\n  <!-- Vertex labels (identity colours) + probability vectors (muted) -->')
    label_specs = [
        (VERTEX_E1, 'e₁', '(1, 0, 0)', (-16, 28), (-16, 48), 'end', CORNER_COLOURS[0]),
        (VERTEX_E2, 'e₂', '(0, 1, 0)', (22, 8), (22, 28), 'start', CORNER_COLOURS[1]),
        (VERTEX_E3, 'e₃', '(0, 0, 1)', (-22, -8), (-22, 12), 'end', CORNER_COLOURS[2]),
    ]
    for (vx, vy), label, vec, (lx, ly), (vox, voy), anchor, colour in label_specs:
        parts.append(
            f'\n  <text x="{vx + lx}" y="{vy + ly}" text-anchor="{anchor}" '
            f'font-size="{LABEL_SIZE}" font-style="italic" '
            f'fill="{colour}">{label}</text>'
        )
        parts.append(
            f'\n  <text x="{vx + vox}" y="{vy + voy}" text-anchor="{anchor}" '
            f'font-size="{VECTOR_LABEL_SIZE}" fill="{MUTED}">{vec}</text>'
        )

    parts.append('\n\n  <!-- p0 label (full strength) -->')
    parts.append(
        f'\n  <text x="{P0[0] + 16}" y="{P0[1] - 2}" '
        f'font-size="21" font-style="italic" fill="{OUTLINE}">p₀</text>'
    )
    parts.append(
        f'\n  <text x="{P0[0] + 16}" y="{P0[1] + 18}" '
        f'font-size="13" fill="{OUTLINE}">(⅓, ⅓, ⅓)</text>'
    )

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "state_space.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
