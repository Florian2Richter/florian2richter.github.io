"""
Generate the two-step trajectories figure (Figure 2 of the clifford-roots
post): a concrete square root of the 3-outcome bistochastic completely
depolarising channel, visualised by tracing what it does to the three
pure states.

We use the specific bistochastic matrix

    T = [ 1/2  1/2   0  ]
        [ 1/6  1/6  2/3 ]
        [ 1/3  1/3  1/3 ]

which satisfies T^2 = P (every column of P is the uniform distribution).
The trajectories are computed directly from T here, so the script is
mathematically transparent: nothing about the picture is hand-placed.

Under T the three pure states go

    e1 -> q_a -> p0
    e2 -> q_a -> p0        (e1 and e2 MERGE at q_a)
    e3 -> q_b -> p0

The merging at q_a is the figure's headline: three step-1 arrows arrive,
but only two step-2 arrows leave, so information is visibly lost in a
stage.

Companion to state_space_figure.py (Figure 1): same simplex geometry and
the same restrained blue palette, with two extra accents for the
dynamics (purple for step 1, teal for step 2).

Usage:
    python trajectories_figure.py [output.svg]

Defaults to ./simplex-root-d3.svg.
"""

from __future__ import annotations

import sys


# ---------------------------------------------------------------------------
# Knobs -- edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (640, 620)  # viewBox width, height (same as Figure 1)

# Simplex vertices in canvas coordinates -- IDENTICAL to Figure 1 so the
# two figures register exactly.
VERTEX_E1 = (140.0, 510.0)   # front-left, e1 = (1,0,0)
VERTEX_E2 = (540.0, 430.0)   # right,      e2 = (0,1,0)
VERTEX_E3 = (310.0, 130.0)   # top,        e3 = (0,0,1)
VERTICES = (VERTEX_E1, VERTEX_E2, VERTEX_E3)

# The root. T^2 = P.
T = [
    [1.0 / 2, 1.0 / 2, 0.0],
    [1.0 / 6, 1.0 / 6, 2.0 / 3],
    [1.0 / 3, 1.0 / 3, 1.0 / 3],
]

# Palette. Blue baseline shared with Figure 1; two dynamic accents.
SIMPLEX_FILL = "#a8c5d8"
SIMPLEX_FILL_OPACITY = 0.55
SIMPLEX_STROKE = "#1a3550"
MUTED = "#3a5a72"
RED = "#c0392b"        # the uniform distribution p0
PURPLE = "#5a2d7a"     # step-1 dynamics (starting points + their arrows)
TEAL = "#3a7a7a"       # step-2 dynamics (intermediate points + their arrows)

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

SIMPLEX_STROKE_W = 2.2
MEDIAN_STROKE_W = 0.9
MEDIAN_OPACITY = 0.22
ARROW_W = 2.0

DOT_START = 6.0        # e1, e2, e3
DOT_QA = 7.0           # q_a slightly larger: two trajectories arrive here
DOT_QB = 5.5           # q_b
DOT_P0 = 6.5           # p0

LABEL_SIZE = 21
VECTOR_LABEL_SIZE = 13
Q_LABEL_SIZE = 15

# Arrow trims (pixels) so heads/tails sit cleanly against the dots.
TRIM_START = 11.0
TRIM_END = 13.0


# ---------------------------------------------------------------------------
# Math: probabilities -> canvas, and the action of T
# ---------------------------------------------------------------------------

def barycentric_to_canvas(p):
    """Place a probability vector p = (p1, p2, p3) on the canvas as the
    convex combination p1*V1 + p2*V2 + p3*V3 of the simplex vertices."""
    x = sum(p[i] * VERTICES[i][0] for i in range(3))
    y = sum(p[i] * VERTICES[i][1] for i in range(3))
    return (x, y)


def apply_T(p):
    """One application of the root: (T p)_i = sum_j T_ij p_j."""
    return [sum(T[i][j] * p[j] for j in range(3)) for i in range(3)]


def shorten(a, b, trim_start=TRIM_START, trim_end=TRIM_END):
    """Trim the segment a->b at both ends so an arrowhead at b clears the
    destination dot and the tail clears the source dot."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = (dx * dx + dy * dy) ** 0.5
    if length < trim_start + trim_end + 1e-9:
        return a, b
    ux, uy = dx / length, dy / length
    return (
        (a[0] + trim_start * ux, a[1] + trim_start * uy),
        (b[0] - trim_end * ux, b[1] - trim_end * uy),
    )


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

    # Two arrowhead markers, one per dynamic colour.
    parts.append(f'''
  <defs>
    <marker id="arrowP" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{PURPLE}"/>
    </marker>
    <marker id="arrowT" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/>
    </marker>
  </defs>''')

    # --- Compute the trajectory points from T (transparent placement) ---
    e1, e2, e3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    qa = apply_T(e1)            # = apply_T(e2): the merge
    qb = apply_T(e3)
    p0 = apply_T(qa)            # = apply_T(qb) = (1/3, 1/3, 1/3)

    cV1, cV2, cV3 = (barycentric_to_canvas(e) for e in (e1, e2, e3))
    cQA = barycentric_to_canvas(qa)
    cQB = barycentric_to_canvas(qb)
    cP0 = barycentric_to_canvas(p0)

    # --- Layer 1: the simplex face ---
    pts = " ".join(f"{x},{y}" for x, y in VERTICES)
    parts.append('\n\n  <!-- Simplex (triangular face) -->')
    parts.append(
        f'\n  <polygon points="{pts}"\n'
        f'           fill="{SIMPLEX_FILL}" fill-opacity="{SIMPLEX_FILL_OPACITY}"\n'
        f'           stroke="{SIMPLEX_STROKE}" stroke-width="{SIMPLEX_STROKE_W}"\n'
        f'           stroke-linejoin="round"/>'
    )

    # --- Layer 2: faint medians (barycentric hint), same as Figure 1 ---
    def midpoint(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    parts.append('\n\n  <!-- Medians -->')
    parts.append(
        f'\n  <g stroke="{SIMPLEX_STROKE}" stroke-width="{MEDIAN_STROKE_W}" '
        f'stroke-opacity="{MEDIAN_OPACITY}" stroke-dasharray="4,5">'
    )
    for v, opp in ((cV1, midpoint(cV2, cV3)),
                   (cV2, midpoint(cV1, cV3)),
                   (cV3, midpoint(cV1, cV2))):
        parts.append(f'\n    <line x1="{v[0]:.1f}" y1="{v[1]:.1f}" '
                     f'x2="{opp[0]:.1f}" y2="{opp[1]:.1f}"/>')
    parts.append('\n  </g>')

    # --- Layer 3: step-1 arrows (purple): e1->qa, e2->qa, e3->qb ---
    def arrow(a, b, color, marker):
        s, e = shorten(a, b)
        return (f'\n  <line x1="{s[0]:.1f}" y1="{s[1]:.1f}" '
                f'x2="{e[0]:.1f}" y2="{e[1]:.1f}" stroke="{color}" '
                f'stroke-width="{ARROW_W}" stroke-linecap="round" '
                f'marker-end="url(#{marker})"/>')

    parts.append('\n\n  <!-- Step-1 arrows (purple): two converge at q_a -->')
    parts.append(arrow(cV1, cQA, PURPLE, "arrowP"))
    parts.append(arrow(cV2, cQA, PURPLE, "arrowP"))
    parts.append(arrow(cV3, cQB, PURPLE, "arrowP"))

    # --- Layer 4: step-2 arrows (teal): qa->p0, qb->p0 (only two!) ---
    parts.append('\n\n  <!-- Step-2 arrows (teal): only two leave -->')
    parts.append(arrow(cQA, cP0, TEAL, "arrowT"))
    parts.append(arrow(cQB, cP0, TEAL, "arrowT"))

    # --- Layer 5: dots ---
    def dot(c, r, fill):
        return f'\n  <circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r}" fill="{fill}"/>'

    parts.append('\n\n  <!-- Intermediate points q_a, q_b (teal) -->')
    parts.append(dot(cQA, DOT_QA, TEAL))   # slightly larger: two arrived here
    parts.append(dot(cQB, DOT_QB, TEAL))

    parts.append('\n\n  <!-- Starting points e1, e2, e3 (purple) -->')
    for c in (cV1, cV2, cV3):
        parts.append(dot(c, DOT_START, PURPLE))

    parts.append('\n\n  <!-- Uniform distribution p0 (red) -->')
    parts.append(dot(cP0, DOT_P0, RED))

    # --- Layer 6: labels ---
    def text(x, y, s, size, fill, anchor="start", italic=False):
        st = ' font-style="italic"' if italic else ''
        return (f'\n  <text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
                f'font-size="{size}"{st} fill="{fill}">{s}</text>')

    parts.append('\n\n  <!-- Vertex labels (purple) + probability vectors (muted) -->')
    # e1: below-left of the bottom-left vertex
    parts.append(text(cV1[0] - 8, cV1[1] + 26, "e₁", LABEL_SIZE, PURPLE, "end", True))
    parts.append(text(cV1[0] - 8, cV1[1] + 44, "(1, 0, 0)", VECTOR_LABEL_SIZE, MUTED, "end"))
    # e2: right of the right vertex
    parts.append(text(cV2[0] + 16, cV2[1] + 8, "e₂", LABEL_SIZE, PURPLE, "start", True))
    parts.append(text(cV2[0] + 16, cV2[1] + 26, "(0, 1, 0)", VECTOR_LABEL_SIZE, MUTED, "start"))
    # e3: above the top vertex
    parts.append(text(cV3[0], cV3[1] - 28, "e₃", LABEL_SIZE, PURPLE, "middle", True))
    parts.append(text(cV3[0], cV3[1] - 10, "(0, 0, 1)", VECTOR_LABEL_SIZE, MUTED, "middle"))

    def qlabel(x, y, sub, anchor):
        return (f'\n  <text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
                f'font-size="{Q_LABEL_SIZE}" font-style="italic" fill="{TEAL}">'
                f'q<tspan baseline-shift="sub" font-size="0.72em"'
                f' font-style="italic">{sub}</tspan></text>')

    parts.append('\n\n  <!-- Intermediate labels (teal) -->')
    # q_a is interior, left of centre; label it just above the dot.
    parts.append(qlabel(cQA[0] - 2, cQA[1] - 13, "a", "middle"))
    # q_b sits on the e2-e3 edge; label it just outside, to the right.
    parts.append(qlabel(cQB[0] + 12, cQB[1] + 5, "b", "start"))

    parts.append('\n\n  <!-- p0 label (red dot, dark label) -->')
    parts.append(text(cP0[0] + 13, cP0[1] - 4, "p₀", LABEL_SIZE, SIMPLEX_STROKE, "start", True))
    parts.append(text(cP0[0] + 13, cP0[1] + 14, "(⅓, ⅓, ⅓)", VECTOR_LABEL_SIZE, MUTED, "start"))

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "simplex-root-d3.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
