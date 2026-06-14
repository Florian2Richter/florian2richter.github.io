"""
Generate the two-step trajectories figure (Figure 2 of the clifford-roots
post): a concrete square root of the 3-outcome bistochastic completely
depolarising channel, visualised by tracing what it does to the three
pure states.

We use the specific bistochastic matrix

    T = [ 1/2  1/2   0  ]
        [ 1/6  1/6  2/3 ]
        [ 1/3  1/3  1/3 ]

which satisfies T^2 = P. The trajectories are computed directly from T,
so the picture is mathematically transparent.

    e1 -> q_a -> p0
    e2 -> q_a -> p0        (e1 and e2 MERGE at q_a)
    e3 -> q_b -> p0

Colour does two jobs, the same scheme as Figure 1. The simplex fill
encodes PURITY (blue-teal and saturated at the pure corners, fading to a
pale glow at the maximally mixed centre p0). The three starting corners
e1, e2, e3 carry their own identity colours, red, green, and blue, and
the intermediate points q_a, q_b are coloured by their purity, so they
read pale as the channel mixes them toward the grey centre. The arrows
are neutral grey (they carry the dynamics; colour carries identity and
purity). q_a, the merge, is the most mixed intermediate point and reads
palest.

Usage:
    python trajectories_figure.py [output.svg]

Defaults to ./simplex-root-d3.svg.
"""

from __future__ import annotations

import sys


# ---------------------------------------------------------------------------
# Knobs -- edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (640, 620)

# Simplex vertices, IDENTICAL to Figure 1 so the figures register.
VERTEX_E1 = (140.0, 510.0)
VERTEX_E2 = (540.0, 430.0)
VERTEX_E3 = (310.0, 130.0)
VERTICES = (VERTEX_E1, VERTEX_E2, VERTEX_E3)

# Coordinate axes (positive octant of R^3), IDENTICAL to Figure 1.
ORIGIN = (310.0, 430.0)
AXIS_E1_END = (95.0, 530.0)
AXIS_E2_END = (590.0, 430.0)
AXIS_E3_END = (310.0, 75.0)

# The root. T^2 = P.
T = [
    [1.0 / 2, 1.0 / 2, 0.0],
    [1.0 / 6, 1.0 / 6, 2.0 / 3],
    [1.0 / 3, 1.0 / 3, 1.0 / 3],
]

# Blue-grey scientific palette, shared with Figure 1. Colour encodes
# purity (blue-teal -> soft blue-grey); arrows neutral blue-grey.
OUTLINE = "#233746"        # text labels (dark blue-grey)
MUTED = "#829aa6"          # grid lines (medians) + muted sublabels
PURE = "#2d6f8f"           # boundary + pure-state dots (blue-teal)
PURE_RGB = (45, 111, 143)  # field high end (pure)
MIXED_RGB = (214, 229, 234)  # field low end (maximally mixed, soft blue-grey)
DARK_DOT = "#1c4a60"       # dot outlines, so pale (mixed) dots stay visible
MIXED_RING = "#5e7886"     # the faint ring at p0
CENTER = "#f5f7f8"         # centre marker halo
GREY_CENTER = "#8a8f94"    # centre marker dot (neutral grey, the "grey noise")
ARROW_GREY = "#829aa6"

# Identity colours for the three pure-state corners (e1, e2, e3),
# shared with Figure 1. These say *which* pure state, not how pure;
# the q_a/q_b intermediate dots stay purity-coloured.
CORNER_COLOURS = ("#cc3b3b", "#2e9e5b", "#3b6fb0")  # e1 red, e2 green, e3 blue

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

SIMPLEX_FILL_OPACITY = 0.9
MESH_N = 26
SIMPLEX_STROKE_W = 2.2
MEDIAN_STROKE_W = 0.9
MEDIAN_OPACITY = 0.22
ARROW_W = 2.0

DOT_START = 6.0
DOT_QA = 7.0
DOT_QB = 5.5
RING_P0 = 7.5

LABEL_SIZE = 21
VECTOR_LABEL_SIZE = 13
Q_LABEL_SIZE = 15

TRIM_START = 11.0
TRIM_END = 13.0


# ---------------------------------------------------------------------------
# Purity -> colour
# ---------------------------------------------------------------------------

def purity_t(p):
    s = sum(x * x for x in p)
    return max(0.0, min(1.0, (s - 1.0 / 3) / (2.0 / 3)))


def purity_colour(t):
    r = round(MIXED_RGB[0] + t * (PURE_RGB[0] - MIXED_RGB[0]))
    g = round(MIXED_RGB[1] + t * (PURE_RGB[1] - MIXED_RGB[1]))
    b = round(MIXED_RGB[2] + t * (PURE_RGB[2] - MIXED_RGB[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


def barycentric_to_canvas(p):
    x = sum(p[i] * VERTICES[i][0] for i in range(3))
    y = sum(p[i] * VERTICES[i][1] for i in range(3))
    return (x, y)


def apply_T(p):
    return [sum(T[i][j] * p[j] for j in range(3)) for i in range(3)]


def shorten(a, b, trim_start=TRIM_START, trim_end=TRIM_END):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = (dx * dx + dy * dy) ** 0.5
    if length < trim_start + trim_end + 1e-9:
        return a, b
    ux, uy = dx / length, dy / length
    return ((a[0] + trim_start * ux, a[1] + trim_start * uy),
            (b[0] - trim_end * ux, b[1] - trim_end * uy))


def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def bary_grid(a, b, n):
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
        f'viewBox="0 0 {width} {height}" font-family="{FONT_FAMILY}">'
    )

    parts.append(f'''
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{OUTLINE}"/>
    </marker>
    <marker id="arrowG" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{ARROW_GREY}"/>
    </marker>
  </defs>''')

    e1, e2, e3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    qa = apply_T(e1)
    qb = apply_T(e3)
    p0 = apply_T(qa)
    cV1, cV2, cV3 = (barycentric_to_canvas(e) for e in (e1, e2, e3))
    cQA, cQB, cP0 = (barycentric_to_canvas(p) for p in (qa, qb, p0))

    # --- Coordinate axes behind the simplex (matches Figure 1) ---
    parts.append('\n\n  <!-- Coordinate axes -->')
    for end in (AXIS_E1_END, AXIS_E2_END, AXIS_E3_END):
        parts.append(
            f'\n  <line x1="{ORIGIN[0]}" y1="{ORIGIN[1]}" '
            f'x2="{end[0]}" y2="{end[1]}" stroke="{OUTLINE}" '
            f'stroke-width="1.8" marker-end="url(#arrow)"/>'
        )

    # --- Purity field (triangular mesh) ---
    parts.append('\n\n  <!-- Purity field -->')
    parts.append('\n  <g stroke-linejoin="round">')
    n = MESH_N

    def tile(corners):
        cen = tuple(sum(c[k] for c in corners) / 3 for k in range(3))
        col = purity_colour(purity_t(cen))
        pts = " ".join("%.2f,%.2f" % barycentric_to_canvas(c) for c in corners)
        return (f'\n    <polygon points="{pts}" fill="{col}" '
                f'fill-opacity="{SIMPLEX_FILL_OPACITY}" stroke="{col}" '
                f'stroke-width="0.6" stroke-opacity="{SIMPLEX_FILL_OPACITY}"/>')

    for a in range(n):
        for b in range(n - a):
            parts.append(tile((bary_grid(a, b, n), bary_grid(a + 1, b, n),
                               bary_grid(a, b + 1, n))))
            if a + b < n - 1:
                parts.append(tile((bary_grid(a + 1, b, n), bary_grid(a, b + 1, n),
                                   bary_grid(a + 1, b + 1, n))))
    parts.append('\n  </g>')

    # --- Simplex outline ---
    pts = " ".join(f"{x},{y}" for x, y in VERTICES)
    parts.append('\n\n  <!-- Simplex outline -->')
    parts.append(f'\n  <polygon points="{pts}" fill="none" stroke="{PURE}" '
                 f'stroke-width="{SIMPLEX_STROKE_W}" stroke-linejoin="round"/>')

    # --- Medians ---
    parts.append('\n\n  <!-- Medians -->')
    parts.append(f'\n  <g stroke="{MUTED}" stroke-width="{MEDIAN_STROKE_W}" '
                 f'stroke-opacity="{MEDIAN_OPACITY}" stroke-dasharray="4,5">')
    for v, opp in ((cV1, midpoint(cV2, cV3)), (cV2, midpoint(cV1, cV3)),
                   (cV3, midpoint(cV1, cV2))):
        parts.append(f'\n    <line x1="{v[0]:.1f}" y1="{v[1]:.1f}" '
                     f'x2="{opp[0]:.1f}" y2="{opp[1]:.1f}"/>')
    parts.append('\n  </g>')

    # --- Arrows (neutral grey): step 1 then step 2 ---
    def arrow(a, b):
        s, e = shorten(a, b)
        return (f'\n  <line x1="{s[0]:.1f}" y1="{s[1]:.1f}" '
                f'x2="{e[0]:.1f}" y2="{e[1]:.1f}" stroke="{ARROW_GREY}" '
                f'stroke-width="{ARROW_W}" stroke-linecap="round" '
                f'marker-end="url(#arrowG)"/>')

    # The three default (pure-state) trajectories live in a toggleable
    # group: the interactive layer hides them once the reader picks a point.
    parts.append('\n\n  <!-- Default trajectories: arrows (toggled off on click) -->')
    parts.append('\n  <g class="default-traj">')
    parts.append('\n  <!-- Step-1 arrows: two converge at q_a -->')
    parts.append(arrow(cV1, cQA)); parts.append(arrow(cV2, cQA)); parts.append(arrow(cV3, cQB))
    parts.append('\n  <!-- Step-2 arrows: only two leave -->')
    parts.append(arrow(cQA, cP0)); parts.append(arrow(cQB, cP0))
    parts.append('\n  </g>')

    # --- Dots, coloured by purity ---
    def dot(c, r, p, stroke=True):
        col = purity_colour(purity_t(p))
        st = f' stroke="{DARK_DOT}" stroke-width="1.3"' if stroke else ''
        return f'\n  <circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r}" fill="{col}"{st}/>'

    parts.append('\n\n  <!-- Intermediate points (purity-coloured, toggled off on click) -->')
    parts.append('\n  <g class="default-traj">')
    parts.append(dot(cQA, DOT_QA, qa))   # q_a: most mixed, reads pale
    parts.append(dot(cQB, DOT_QB, qb))
    parts.append('\n  </g>')
    parts.append('\n\n  <!-- Starting points e1, e2, e3 (identity colours: red, green, blue) -->')
    for c, colour in ((cV1, CORNER_COLOURS[0]), (cV2, CORNER_COLOURS[1]), (cV3, CORNER_COLOURS[2])):
        parts.append(f'\n  <circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{DOT_START}" fill="{colour}"/>')

    parts.append('\n\n  <!-- Maximally mixed state p0 (solid grey marker, fully visible) -->')
    parts.append(f'\n  <circle cx="{cP0[0]:.1f}" cy="{cP0[1]:.1f}" r="9" fill="{CENTER}"/>')
    parts.append(f'\n  <circle cx="{cP0[0]:.1f}" cy="{cP0[1]:.1f}" r="6" fill="{GREY_CENTER}"/>')

    # --- Labels ---
    def text(x, y, s, size, fill, anchor="start", italic=False):
        st = ' font-style="italic"' if italic else ''
        return (f'\n  <text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
                f'font-size="{size}"{st} fill="{fill}">{s}</text>')

    parts.append('\n\n  <!-- Vertex labels (identity colours) + vectors (muted) -->')
    parts.append(text(cV1[0] - 8, cV1[1] + 26, "e₁", LABEL_SIZE, CORNER_COLOURS[0],"end", True))
    parts.append(text(cV1[0] - 8, cV1[1] + 44, "(1, 0, 0)", VECTOR_LABEL_SIZE, MUTED, "end"))
    parts.append(text(cV2[0] + 16, cV2[1] + 8, "e₂", LABEL_SIZE, CORNER_COLOURS[1],"start", True))
    parts.append(text(cV2[0] + 16, cV2[1] + 26, "(0, 1, 0)", VECTOR_LABEL_SIZE, MUTED, "start"))
    parts.append(text(cV3[0], cV3[1] - 28, "e₃", LABEL_SIZE, CORNER_COLOURS[2],"middle", True))
    parts.append(text(cV3[0], cV3[1] - 10, "(0, 0, 1)", VECTOR_LABEL_SIZE, MUTED, "middle"))

    # The intermediate points ARE the images of the pure states under the
    # root S. q_b = S e3; q_a is where e1 and e2 land together, so it is
    # labelled by the equality S e1 = S e2 (the merge is the headline).
    def slabel(x, y, content, anchor):
        return (f'\n  <text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
                f'font-size="{Q_LABEL_SIZE}" fill="{MUTED}">{content}</text>')

    SE = '<tspan font-style="italic">Se</tspan>'
    parts.append('\n\n  <!-- Intermediate labels = images under S (toggled off on click) -->')
    parts.append('\n  <g class="default-traj">')
    parts.append(slabel(cQA[0], cQA[1] - 14, f'{SE}₁ = {SE}₂', "middle"))
    parts.append(slabel(cQB[0] + 12, cQB[1] + 5, f'{SE}₃', "start"))
    parts.append('\n  </g>')

    parts.append('\n\n  <!-- p0 label (full strength) -->')
    parts.append(text(cP0[0] + 16, cP0[1] - 4, "p₀", LABEL_SIZE, OUTLINE, "start", True))
    parts.append(text(cP0[0] + 16, cP0[1] + 14, "(⅓, ⅓, ⅓)", VECTOR_LABEL_SIZE, OUTLINE, "start"))

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "simplex-root-d3.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
