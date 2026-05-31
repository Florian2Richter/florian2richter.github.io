"""
Generate the classical state space figure for a 3-outcome system.

The simplex (probability distributions over three outcomes) is drawn as
a 2D face sitting inside the positive octant of R^3. Three coordinate
axes from the origin show the embedding; the triangular face spans the
three unit basis vectors.

The figure follows the layout of Figure 3.1 in Richter's diploma thesis
(state-space figure), but uses a restrained blue-toned palette and
includes vertex probability-vector labels.

Usage:
    python state_space_figure.py [output.svg]

Defaults to ./state_space.svg.
"""

from __future__ import annotations

import sys


# ---------------------------------------------------------------------------
# Knobs — edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (640, 620)  # viewBox width, height

# Projection of R^3 axes to 2D.
# Origin near lower-centre; axes splay outward.
ORIGIN = (310, 430)

# Simplex vertices (where each axis hits "1") in canvas coordinates.
# These define the projection of e_1, e_2, e_3 in R^3 to 2D.
VERTEX_E1 = (140, 510)   # front-left ("out of the page")
VERTEX_E2 = (540, 430)   # to the right
VERTEX_E3 = (310, 130)   # upward

# Axes extend past the simplex vertices (for arrowheads).
AXIS_E1_END = (95, 530)
AXIS_E2_END = (590, 430)
AXIS_E3_END = (310, 75)

# Centroid (uniform distribution p_0) — computed automatically.
P0 = (
    (VERTEX_E1[0] + VERTEX_E2[0] + VERTEX_E3[0]) / 3,
    (VERTEX_E1[1] + VERTEX_E2[1] + VERTEX_E3[1]) / 3,
)

# Palette — same blue tones as the v3 standalone simplex.
SIMPLEX_FILL = "#a8c5d8"
SIMPLEX_FILL_OPACITY = 0.55
SIMPLEX_STROKE = "#1a3550"
AXIS_COLOR = "#1a3550"
LABEL_COLOR = "#1a3550"
MUTED_COLOR = "#3a5a72"
ACCENT_COLOR = "#c0392b"  # the p_0 dot

# Stroke widths.
SIMPLEX_STROKE_W = 2.2
AXIS_STROKE_W = 1.8
TICK_STROKE_W = 1.6
MEDIAN_STROKE_W = 0.9
MEDIAN_OPACITY = 0.22

# Font.
FONT_FAMILY = "Georgia, 'Times New Roman', serif"
LABEL_SIZE = 22
VECTOR_LABEL_SIZE = 14


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def tick_perpendicular(point, axis_direction, length=14):
    """Return endpoints of a small tick mark, perpendicular to an axis,
    centred at `point`. `axis_direction` is any vector along the axis.
    """
    ax, ay = axis_direction
    norm = (ax ** 2 + ay ** 2) ** 0.5
    px, py = -ay / norm, ax / norm  # perpendicular unit vector
    cx, cy = point
    return (
        (cx - length / 2 * px, cy - length / 2 * py),
        (cx + length / 2 * px, cy + length / 2 * py),
    )


def midpoint(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


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

    # Arrowhead marker for axes.
    parts.append(f'''
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{AXIS_COLOR}"/>
    </marker>
  </defs>''')

    # --- Layer 1: axes behind the simplex (so the simplex fill sits on top) ---
    # The three axes emanate from the origin. We draw them first so that the
    # fill of the simplex covers the portions hidden "behind" the simplex
    # face when read as a 3D figure.
    parts.append('\n  <!-- Coordinate axes -->')
    for end in (AXIS_E1_END, AXIS_E2_END, AXIS_E3_END):
        parts.append(
            f'\n  <line x1="{ORIGIN[0]}" y1="{ORIGIN[1]}" '
            f'x2="{end[0]}" y2="{end[1]}"\n'
            f'        stroke="{AXIS_COLOR}" stroke-width="{AXIS_STROKE_W}"\n'
            f'        marker-end="url(#arrow)"/>'
        )

    # --- Layer 2: the simplex face ---
    points_str = " ".join(f"{x},{y}" for x, y in [VERTEX_E1, VERTEX_E2, VERTEX_E3])
    parts.append('\n\n  <!-- Simplex (triangular face) -->')
    parts.append(
        f'\n  <polygon points="{points_str}"\n'
        f'           fill="{SIMPLEX_FILL}" fill-opacity="{SIMPLEX_FILL_OPACITY}"\n'
        f'           stroke="{SIMPLEX_STROKE}" stroke-width="{SIMPLEX_STROKE_W}"\n'
        f'           stroke-linejoin="round"/>'
    )

    # --- Layer 3: medians inside the simplex (faint barycentric hint) ---
    parts.append('\n\n  <!-- Medians from each vertex to opposite edge midpoint -->')
    parts.append(
        f'\n  <g stroke="{SIMPLEX_STROKE}" stroke-width="{MEDIAN_STROKE_W}" '
        f'stroke-opacity="{MEDIAN_OPACITY}" stroke-dasharray="4,5">'
    )
    median_endpoints = [
        (VERTEX_E1, midpoint(VERTEX_E2, VERTEX_E3)),
        (VERTEX_E2, midpoint(VERTEX_E1, VERTEX_E3)),
        (VERTEX_E3, midpoint(VERTEX_E1, VERTEX_E2)),
    ]
    for (sx, sy), (ex, ey) in median_endpoints:
        parts.append(
            f'\n    <line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}"/>'
        )
    parts.append('\n  </g>')

    # --- Layer 4: tick marks where axes meet simplex vertices ---
    parts.append('\n\n  <!-- Unit tick marks on the axes at the simplex vertices -->')
    tick_specs = [
        (VERTEX_E1, (VERTEX_E1[0] - ORIGIN[0], VERTEX_E1[1] - ORIGIN[1])),
        (VERTEX_E2, (VERTEX_E2[0] - ORIGIN[0], VERTEX_E2[1] - ORIGIN[1])),
        (VERTEX_E3, (VERTEX_E3[0] - ORIGIN[0], VERTEX_E3[1] - ORIGIN[1])),
    ]
    for vertex, axis_dir in tick_specs:
        (sx, sy), (ex, ey) = tick_perpendicular(vertex, axis_dir, length=14)
        parts.append(
            f'\n  <line x1="{sx:.1f}" y1="{sy:.1f}" '
            f'x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{AXIS_COLOR}" stroke-width="{TICK_STROKE_W}"/>'
        )

    # --- Layer 5: vertex dots ---
    parts.append('\n\n  <!-- Vertex dots -->')
    for vx, vy in (VERTEX_E1, VERTEX_E2, VERTEX_E3):
        parts.append(
            f'\n  <circle cx="{vx}" cy="{vy}" r="5.5" fill="{LABEL_COLOR}"/>'
        )

    # --- Layer 6: vertex labels and probability vectors ---
    parts.append('\n\n  <!-- Vertex labels and their probability vectors -->')
    label_specs = [
        # (vertex, label, vector, label_offset, vector_offset, anchor)
        # e_1: down-left of the front-left vertex (more vertical clearance for arrowhead)
        (VERTEX_E1, 'e₁', '(1, 0, 0)', (-16, 28),  (-16, 48), 'end'),
        # e_2: right of the right vertex, offset down to clear the arrowhead
        (VERTEX_E2, 'e₂', '(0, 1, 0)', (22, 8),    (22, 28),  'start'),
        # e_3: up-left of the top vertex. Vector goes BELOW the letter
        # (i.e. between letter and vertex) so the reading order is letter-first.
        (VERTEX_E3, 'e₃', '(0, 0, 1)', (-22, -8),  (-22, 12), 'end'),
    ]
    for (vx, vy), label, vec, (lx, ly), (vx_off, vy_off), anchor in label_specs:
        parts.append(
            f'\n  <text x="{vx + lx}" y="{vy + ly}" text-anchor="{anchor}" '
            f'font-size="{LABEL_SIZE}" font-style="italic" '
            f'fill="{LABEL_COLOR}">{label}</text>'
        )
        parts.append(
            f'\n  <text x="{vx + vx_off}" y="{vy + vy_off}" text-anchor="{anchor}" '
            f'font-size="{VECTOR_LABEL_SIZE}" '
            f'fill="{MUTED_COLOR}">{vec}</text>'
        )

    # --- Layer 7: centroid p_0 ---
    parts.append('\n\n  <!-- Centroid p_0 -->')
    parts.append(
        f'\n  <circle cx="{P0[0]}" cy="{P0[1]}" r="6.5" '
        f'fill="{ACCENT_COLOR}"/>'
    )
    parts.append(
        f'\n  <text x="{P0[0] + 14}" y="{P0[1] - 2}" '
        f'font-size="21" font-style="italic" '
        f'fill="{LABEL_COLOR}">p₀</text>'
    )
    parts.append(
        f'\n  <text x="{P0[0] + 14}" y="{P0[1] + 18}" '
        f'font-size="13" '
        f'fill="{MUTED_COLOR}">(⅓, ⅓, ⅓)</text>'
    )

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "state_space.svg"
    svg = build_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
