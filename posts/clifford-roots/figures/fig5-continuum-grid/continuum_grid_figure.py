"""
Generate the "continuum vs. finite grid" figure for the Clifford section.

Two panels side by side. LEFT: a schematic Bloch ball (the continuum of
qubit states), with three coloured coordinate axes double-labelled by
their Pauli name and their Weyl label, and a grey identity dot at the
centre. RIGHT: the finite label plane F_2^2, four points on a faint
coordinate grid, with the identity (0,0) drawn as a grey dot (matching
the grey identity dot at the centre of the Bloch ball on the left) and
three curved arrows showing one homomorphism h as a
3-cycle of the nonzero points. Each axis on the left shares its colour
with the matching point on the right, so the axis<->point correspondence
is read off by colour.

Companion to the other figure generators: same restrained palette, all
geometry as named constants at the top, SVG layers separated by comment
headers. Static (no interactive layer): it is a conceptual sketch.

Usage:
    python continuum_grid_figure.py [output.svg]

Defaults to ./continuum-grid-d2.svg.
"""

from __future__ import annotations

import math
import sys


# ---------------------------------------------------------------------------
# Knobs — edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (680, 300)        # viewBox width, height

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

# Palette. Neutral structure in the shared blue-grey; three categorical
# colours carry the axis<->point correspondence (the point of the figure).
AXIS = "#233746"        # text, h-arrows (dark blue-grey)
GRID = "#829aa6"        # faint guides
TEAL = "#2d6f8f"        # X = (1,0)   colour 1
PURPLE = "#6f5499"      # Z = (0,1)   colour 2
CORAL = "#c25b4e"       # Y = (1,1)   colour 3
GREY = "#7d8a91"        # identity (0,0) and ball centre (neutral)

# Bloch-ball fill + wireframe, identical in treatment to Figures 3 and 4
# (same projection angles, latitudes, meridians, palette and gradient
# stops), so the mini ball reads as the same object as the big ones.
PURE = "#2d6f8f"        # silhouette boundary (blue-teal, == TEAL)
MIXED = "#d6e5ea"       # gradient centre (soft blue-grey)
OUTLINE = "#829aa6"     # wireframe latitude/longitude lines (muted blue-grey)

ALPHA = math.radians(35.0)   # azimuth (matches Figs 3, 4)
ELEV = math.radians(20.0)    # elevation above the equator
LATITUDES = [0.78, 0.42, 0.0, -0.42, -0.78]
N_MERIDIANS = 8
SAMPLES = 180
SILHOUETTE_W = 2.2
EQUATOR_W = 1.7
WIRE_FRONT_W = 1.15
WIRE_BACK_W = 0.9
WIRE_FRONT_OPACITY = 0.50
WIRE_BACK_OPACITY = 0.22
EQUATOR_FRONT_OPACITY = 0.85
EQUATOR_BACK_OPACITY = 0.30

# --- Left panel: the Bloch ball ---
LCX, LCY, LR = 170.0, 150.0, 72.0   # ball centre and radius
# Axis tips (canvas coords). Standard orientation: Z up, Y to the right,
# X toward the lower-left (toward the viewer).
Z_TIP = (170.0, 64.0)
Y_TIP = (268.0, 140.0)
X_TIP = (96.0, 212.0)
AXIS_W = 2.4

# --- Right panel: the label plane F_2^2 ---
P00 = (440.0, 230.0)   # identity
P10 = (560.0, 230.0)
P01 = (440.0, 110.0)
P11 = (560.0, 110.0)
GRID_PAD = 34.0        # how far the faint guide lines run past the points
PT_R = 7.0             # point radius
H_BOW = 0.62           # how far the h-arrows bow outward (fraction of mid->centroid)
H_PAD = 15.0           # gap between an h-arrow end and its point marker

# --- Shared ---
LABEL_SIZE = 15
SUB_SIZE = 15
DASH = "3,4"

SUB_LEFT = (170.0, 282.0)
SUB_RIGHT = (500.0, 282.0)
DIVIDER_X = 350.0      # faint dashed panel divider


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _unit(dx, dy):
    n = math.hypot(dx, dy)
    return (dx / n, dy / n) if n else (0.0, 0.0)


# --- Bloch-ball wireframe (ported from bloch_ball_figure.py, scaled to the
#     mini ball at (LCX, LCY) with radius LR so the fill and grid lines match
#     Figures 3 and 4 exactly) ---

def project(p):
    """Orthographic projection of a 3D unit-sphere point onto the mini ball.

    Returns (sx, sy, depth); depth > 0 is the front (camera-facing) hemisphere.
    """
    x, y, z = p
    u = LR * (x * math.cos(ALPHA) - y * math.sin(ALPHA))
    w = x * math.sin(ALPHA) + y * math.cos(ALPHA)
    v = LR * (z * math.cos(ELEV) - w * math.sin(ELEV))
    depth = z * math.sin(ELEV) + w * math.cos(ELEV)
    return (LCX + u, LCY - v, depth)


def latitude_points(z, samples=SAMPLES):
    rho = math.sqrt(max(0.0, 1.0 - z * z))
    return [(rho * math.cos(2.0 * math.pi * i / samples),
             rho * math.sin(2.0 * math.pi * i / samples), z)
            for i in range(samples + 1)]


def meridian_points(phi, samples=SAMPLES):
    pts = []
    for i in range(samples + 1):
        psi = math.pi * i / samples
        pts.append((math.sin(psi) * math.cos(phi),
                    math.sin(psi) * math.sin(phi),
                    math.cos(psi)))
    return pts


def split_runs(points3d, closed):
    """Project and split into maximal runs of equal visibility (front vs back),
    sharing boundary points so arcs stay connected."""
    proj = [project(p) for p in points3d]
    runs, cur, cur_front = [], [], None
    for (sx, sy, d) in proj:
        front = d >= 0.0
        if cur_front is None:
            cur_front, cur = front, [(sx, sy)]
        elif front == cur_front:
            cur.append((sx, sy))
        else:
            cur.append((sx, sy))
            runs.append((cur_front, cur))
            cur, cur_front = [(sx, sy)], front
    if cur:
        runs.append((cur_front, cur))
    if closed and len(runs) > 1 and runs[0][0] == runs[-1][0]:
        first_front, first_pts = runs[0]
        _, last_pts = runs.pop()
        runs[0] = (first_front, last_pts[:-1] + first_pts)
    return runs


def polyline(points, stroke, width, opacity, dash=None):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'\n  <polyline points="{pts}" fill="none" '
            f'stroke="{stroke}" stroke-width="{width}" '
            f'stroke-opacity="{opacity}"{dash_attr} '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def wire_runs(points3d, closed, front_w, back_w, front_op, back_op):
    out = []
    for is_front, pts in split_runs(points3d, closed):
        if len(pts) < 2:
            continue
        if is_front:
            out.append(polyline(pts, OUTLINE, front_w, front_op))
        else:
            out.append(polyline(pts, OUTLINE, back_w, back_op, dash=DASH))
    return "".join(out)


def axis_line(tip, colour, marker):
    """A coordinate axis from the ball centre out to `tip`, arrowhead at the tip."""
    return (
        f'\n  <line x1="{LCX:.2f}" y1="{LCY:.2f}" x2="{tip[0]:.2f}" y2="{tip[1]:.2f}" '
        f'stroke="{colour}" stroke-width="{AXIS_W}" stroke-linecap="round" '
        f'marker-end="url(#{marker})"/>'
    )


def h_curve(start, end, centroid):
    """A gently bowed quadratic arc from `start` to `end`, pushed away from
    `centroid`, trimmed at both ends so the arrowhead clears the point markers."""
    mx, my = (start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0
    cx = mx + H_BOW * (mx - centroid[0])
    cy = my + H_BOW * (my - centroid[1])
    # Trim: nudge the endpoints toward the control point by H_PAD.
    sux, suy = _unit(cx - start[0], cy - start[1])
    eux, euy = _unit(cx - end[0], cy - end[1])
    s = (start[0] + H_PAD * sux, start[1] + H_PAD * suy)
    e = (end[0] + H_PAD * eux, end[1] + H_PAD * euy)
    return (
        f'\n  <path d="M {s[0]:.2f} {s[1]:.2f} Q {cx:.2f} {cy:.2f} {e[0]:.2f} {e[1]:.2f}" '
        f'fill="none" stroke="{AXIS}" stroke-width="1.8" stroke-linecap="round" '
        f'marker-end="url(#arrowH)"/>'
    )


# ---------------------------------------------------------------------------
# SVG emission
# ---------------------------------------------------------------------------

def text(x, y, body, size, fill, anchor="middle", italic=False):
    style = ' font-style="italic"' if italic else ""
    return (
        f'\n  <text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
        f'font-size="{size}" fill="{fill}"{style}>{body}</text>'
    )


def named_marker(mid, colour):
    return (
        f'\n    <marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{colour}"/></marker>'
    )


def build_svg():
    width, height = CANVAS
    parts = []

    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="{FONT_FAMILY}" '
        f'role="img" aria-label="Left: the continuum of qubit states with three '
        f'coloured Bloch axes. Right: the finite plane of labels, four points, '
        f'with the identity fixed and the other three permuted by h.">'
    )

    # --- Markers: one arrowhead per axis colour, plus a dark one for h.
    #     Plus the purity radial gradient, identical stops to Figs 3 and 4. ---
    parts.append('\n  <defs>')
    parts.append(named_marker("arrowX", TEAL))
    parts.append(named_marker("arrowZ", PURPLE))
    parts.append(named_marker("arrowY", CORAL))
    parts.append(named_marker("arrowH", AXIS))
    # Unique id (the post inlines several SVGs that each define a "purity"
    # gradient; a shared id would collide and the mini ball would sample the
    # first figure's gradient instead of its own).
    parts.append(
        f'\n    <radialGradient id="purity-cg" cx="{LCX:g}" cy="{LCY:g}" r="{LR:g}" '
        f'gradientUnits="userSpaceOnUse">'
        f'\n      <stop offset="0%" stop-color="{MIXED}" stop-opacity="0.30"/>'
        f'\n      <stop offset="60%" stop-color="#5f93ad" stop-opacity="0.35"/>'
        f'\n      <stop offset="100%" stop-color="{PURE}" stop-opacity="0.40"/>'
        f'\n    </radialGradient>'
    )
    parts.append('\n  </defs>')

    # ======================= LEFT PANEL: the Bloch ball =======================
    parts.append('\n\n  <!-- Left panel: Bloch ball (the continuum), fill + '
                 'wireframe identical to Figures 3 and 4 -->')
    # Interior purity field (blue-teal shell -> pale core).
    parts.append(
        f'\n  <circle cx="{LCX}" cy="{LCY}" r="{LR}" fill="url(#purity-cg)" stroke="none"/>'
    )
    # Latitude circles (equator heavier; back portions dashed).
    parts.append('\n  <g>')
    for z in LATITUDES:
        if abs(z) < 1e-9:
            parts.append(wire_runs(latitude_points(z), True, EQUATOR_W,
                                   WIRE_BACK_W, EQUATOR_FRONT_OPACITY,
                                   EQUATOR_BACK_OPACITY))
        else:
            parts.append(wire_runs(latitude_points(z), True, WIRE_FRONT_W,
                                   WIRE_BACK_W, WIRE_FRONT_OPACITY,
                                   WIRE_BACK_OPACITY))
    parts.append('\n  </g>')
    # Longitude meridians.
    parts.append('\n  <g>')
    for k in range(N_MERIDIANS):
        phi = 2.0 * math.pi * k / N_MERIDIANS
        parts.append(wire_runs(meridian_points(phi), False, WIRE_FRONT_W,
                               WIRE_BACK_W, WIRE_FRONT_OPACITY, WIRE_BACK_OPACITY))
    parts.append('\n  </g>')
    # Silhouette (crisp pure-state boundary on top of the wireframe).
    parts.append(
        f'\n  <circle cx="{LCX}" cy="{LCY}" r="{LR}" fill="none" '
        f'stroke="{PURE}" stroke-width="{SILHOUETTE_W}"/>'
    )

    # Three coloured axes from the centre.
    parts.append(axis_line(Z_TIP, PURPLE, "arrowZ"))
    parts.append(axis_line(Y_TIP, CORAL, "arrowY"))
    parts.append(axis_line(X_TIP, TEAL, "arrowX"))

    # Grey identity dot at the centre, with a grey (0,0) caption matching the
    # identity point on the right panel. Placed lower-right of the dot, the
    # one quadrant no axis runs through.
    parts.append(
        f'\n  <circle cx="{LCX}" cy="{LCY}" r="5" fill="{GREY}"/>'
    )
    parts.append(text(LCX + 9, LCY + 19, "(0,0)", LABEL_SIZE, GREY, anchor="start"))

    # Axis double-labels (Pauli name italic, Weyl label plain), at the tips.
    parts.append(text(Z_TIP[0], Z_TIP[1] - 12,
                      '<tspan font-style="italic">Z</tspan> = (0,1)',
                      LABEL_SIZE, PURPLE, anchor="middle"))
    parts.append(text(Y_TIP[0] + 10, Y_TIP[1] + 1,
                      '<tspan font-style="italic">Y</tspan> = (1,1)',
                      LABEL_SIZE, CORAL, anchor="start"))
    parts.append(text(X_TIP[0] - 8, X_TIP[1] + 14,
                      '<tspan font-style="italic">X</tspan> = (1,0)',
                      LABEL_SIZE, TEAL, anchor="end"))

    # Sub-label.
    parts.append(text(SUB_LEFT[0], SUB_LEFT[1], "qubit states: a continuum",
                      SUB_SIZE, AXIS, anchor="middle", italic=True))

    # ===================== RIGHT PANEL: the label plane =====================
    parts.append('\n\n  <!-- Right panel: the finite label plane F_2^2 -->')
    # Faint coordinate guides through the origin (0,0).
    parts.append(
        f'\n  <line x1="{P00[0] - GRID_PAD:.2f}" y1="{P00[1]:.2f}" '
        f'x2="{P10[0] + GRID_PAD:.2f}" y2="{P00[1]:.2f}" '
        f'stroke="{GRID}" stroke-width="1" stroke-opacity="0.45"/>'
    )
    parts.append(
        f'\n  <line x1="{P00[0]:.2f}" y1="{P00[1] + GRID_PAD:.2f}" '
        f'x2="{P01[0]:.2f}" y2="{P01[1] - GRID_PAD:.2f}" '
        f'stroke="{GRID}" stroke-width="1" stroke-opacity="0.45"/>'
    )

    # The h 3-cycle: (1,0) -> (0,1) -> (1,1) -> (1,0), bowed away from the
    # centroid of the three nonzero points, leaving (0,0) untouched.
    cyc = [P10, P01, P11]
    centroid = (sum(p[0] for p in cyc) / 3.0, sum(p[1] for p in cyc) / 3.0)
    parts.append('\n  <!-- one example homomorphism h, a 3-cycle of the nonzero points -->')
    parts.append(h_curve(P10, P01, centroid))
    parts.append(h_curve(P01, P11, centroid))
    parts.append(h_curve(P11, P10, centroid))
    parts.append(text(centroid[0], centroid[1] + 5, "h", LABEL_SIZE + 3,
                      AXIS, anchor="middle", italic=True))

    # The four points. Identity (0,0) is a grey dot, matching the grey
    # identity dot at the centre of the Bloch ball on the left; the other
    # three are solid, each in the colour of its matching Bloch axis.
    parts.append(
        f'\n  <circle cx="{P00[0]}" cy="{P00[1]}" r="{PT_R}" fill="{GREY}"/>'
    )
    for p, colour in ((P10, TEAL), (P01, PURPLE), (P11, CORAL)):
        parts.append(
            f'\n  <circle cx="{p[0]}" cy="{p[1]}" r="{PT_R}" fill="{colour}"/>'
        )

    # Coordinate labels, offset outward from the 2x2 block.
    parts.append(text(P00[0] - 12, P00[1] + 18, "(0,0)", LABEL_SIZE, GREY, anchor="end"))
    parts.append(text(P10[0] + 12, P10[1] + 18, "(1,0)", LABEL_SIZE, TEAL, anchor="start"))
    parts.append(text(P01[0] - 12, P01[1] - 10, "(0,1)", LABEL_SIZE, PURPLE, anchor="end"))
    parts.append(text(P11[0] + 12, P11[1] - 10, "(1,1)", LABEL_SIZE, CORAL, anchor="start"))

    # Sub-label. ("labels", not "Weyl labels": the figure appears in the post
    # before the Weyl operators are introduced.)
    parts.append(text(SUB_RIGHT[0], SUB_RIGHT[1], "labels: a finite grid",
                      SUB_SIZE, AXIS, anchor="middle", italic=True))

    # ----- Panel divider (faint) -----
    parts.append('\n\n  <!-- faint divider between the two panels -->')
    parts.append(
        f'\n  <line x1="{DIVIDER_X}" y1="40" x2="{DIVIDER_X}" y2="258" '
        f'stroke="{GRID}" stroke-width="1" stroke-dasharray="{DASH}" '
        f'stroke-opacity="0.35"/>'
    )

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "continuum-grid-d2.svg"
    svg = build_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
