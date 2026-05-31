"""
Generate the qubit state space figure: the Bloch ball.

A wireframe sphere (latitude + longitude lines) drawn with a fixed
orthographic projection, z-axis vertical, viewed from slightly above
the equator. Pure states live on the surface, mixed states inside; the
maximally mixed state 1/2 sits at the centre. Three coordinate axes
(x, y, z) emerge from the centre.

Companion to state_space_figure.py (Figure 1). Same restrained blue
palette and the same code conventions: all geometry as named constants
at the top, SVG layers separated by comment headers.

Usage:
    python bloch_ball_figure.py [output.svg]

Defaults to ./bloch_ball.svg.
"""

from __future__ import annotations

import math
import sys


# ---------------------------------------------------------------------------
# Knobs — edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (640, 640)        # viewBox width, height
CX, CY = 320.0, 332.0      # centre of the ball, in canvas coordinates
R = 210.0                  # projected radius (orthographic => silhouette is a circle)

# Viewing angles. Azimuth turns the sphere about its polar (z) axis;
# elevation lifts the viewer above the equatorial plane. These define the
# whole projection and (later) the click-to-Bloch-vector inversion.
ALPHA = math.radians(35.0)  # azimuth
ELEV = math.radians(20.0)   # elevation above the equator

# Palette. Structure stays navy; STATE colour encodes purity, exactly as
# Figure 1. Purity tr(rho^2) = (1 + r^2)/2 runs from 1/2 at the centre
# (maximally mixed) to 1 on the surface (pure), so the ball is filled with
# a green shell fading to a pale core, and the poles are green.
OUTLINE = "#1a3550"
MUTED = "#3a5a72"
GREEN = "#1f7a50"        # pure states (the surface, the poles)
PALE = "#e4eeea"         # the maximally mixed core
MIXED_RING = "#5f7d70"   # the faint ring at I/2

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

# Wireframe styling.
SILHOUETTE_W = 2.2
EQUATOR_W = 1.7
WIRE_FRONT_W = 1.15
WIRE_BACK_W = 0.9
WIRE_FRONT_OPACITY = 0.50
WIRE_BACK_OPACITY = 0.22
EQUATOR_FRONT_OPACITY = 0.85
EQUATOR_BACK_OPACITY = 0.30
DASH = "3,4"
AXIS_W = 1.8

# Which latitude circles to draw (z values). 0.0 is the equator.
LATITUDES = [0.78, 0.42, 0.0, -0.42, -0.78]
N_MERIDIANS = 8            # longitude lines, evenly spaced in azimuth
SAMPLES = 180              # samples per circle (smoothness of the wireframe)

# How far the axis arrows extend past the surface (in sphere radii).
AXIS_EXT = 1.18
AXIS_LABEL_EXT = 1.42

# Label sizes.
KET_SIZE = 21
AXIS_LABEL_SIZE = 20
CENTER_LABEL_SIZE = 20

# Centre label. The maximally mixed state, identity over two.
CENTER_LABEL = "I/2"


# ---------------------------------------------------------------------------
# Projection
# ---------------------------------------------------------------------------

def project(p):
    """Orthographic projection of a 3D point to canvas coordinates.

    Returns (sx, sy, depth) where (sx, sy) are SVG coordinates and `depth`
    is the signed distance toward the viewer (depth > 0 => front hemisphere,
    i.e. the surface point faces the camera and is drawn solid).
    """
    x, y, z = p
    u = R * (x * math.cos(ALPHA) - y * math.sin(ALPHA))
    w = x * math.sin(ALPHA) + y * math.cos(ALPHA)
    v = R * (z * math.cos(ELEV) - w * math.sin(ELEV))
    depth = z * math.sin(ELEV) + w * math.cos(ELEV)
    return (CX + u, CY - v, depth)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def latitude_points(z, samples=SAMPLES):
    rho = math.sqrt(max(0.0, 1.0 - z * z))
    pts = []
    for i in range(samples + 1):
        t = 2.0 * math.pi * i / samples
        pts.append((rho * math.cos(t), rho * math.sin(t), z))
    return pts


def meridian_points(phi, samples=SAMPLES):
    pts = []
    for i in range(samples + 1):
        psi = math.pi * i / samples  # north pole (psi=0) to south pole (psi=pi)
        pts.append((math.sin(psi) * math.cos(phi),
                    math.sin(psi) * math.sin(phi),
                    math.cos(psi)))
    return pts


def split_runs(points3d, closed):
    """Project a sequence of 3D points and split into maximal runs of equal
    visibility (front vs back). Returns a list of (is_front, [(sx, sy), ...]).
    Transition points are shared between adjacent runs so arcs stay connected.
    """
    proj = [project(p) for p in points3d]
    runs = []
    cur = []
    cur_front = None
    for (sx, sy, d) in proj:
        front = d >= 0.0
        if cur_front is None:
            cur_front = front
            cur = [(sx, sy)]
        elif front == cur_front:
            cur.append((sx, sy))
        else:
            cur.append((sx, sy))          # share the boundary point
            runs.append((cur_front, cur))
            cur = [(sx, sy)]
            cur_front = front
    if cur:
        runs.append((cur_front, cur))

    # For a closed curve, merge the wrap-around seam if endpoints match.
    if closed and len(runs) > 1 and runs[0][0] == runs[-1][0]:
        first_front, first_pts = runs[0]
        last_front, last_pts = runs.pop()
        runs[0] = (first_front, last_pts[:-1] + first_pts)
    return runs


# ---------------------------------------------------------------------------
# SVG emission
# ---------------------------------------------------------------------------

def polyline(points, stroke, width, opacity, dash=None):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'\n    <polyline points="{pts}" fill="none" '
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


def build_svg():
    width, height = CANVAS
    parts = []

    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="{FONT_FAMILY}" '
        f'role="img" aria-label="Bloch ball: the qubit state space" '
        f'data-cx="{CX:g}" data-cy="{CY:g}" data-r="{R:g}" '
        f'data-alpha-deg="{math.degrees(ALPHA):g}" '
        f'data-elev-deg="{math.degrees(ELEV):g}">'
    )

    # Arrowhead marker plus the purity gradient (green shell, pale core).
    parts.append(f'''
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{OUTLINE}"/>
    </marker>
    <radialGradient id="purity" cx="{CX:g}" cy="{CY:g}" r="{R:g}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{PALE}" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="#6fae8e" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="{GREEN}" stop-opacity="0.5"/>
    </radialGradient>
  </defs>''')

    # --- Layer 1: interior purity field (green shell -> pale core) ---
    parts.append('\n\n  <!-- Ball interior: purity field -->')
    parts.append(
        f'\n  <circle cx="{CX}" cy="{CY}" r="{R}" '
        f'fill="url(#purity)" stroke="none"/>'
    )

    # --- Layer 2: back wireframe (dashed, hidden hemisphere) ---
    # Split happens per-line; we draw both hemispheres here grouped, with the
    # back portions dashed and the front portions solid. Group for clarity.
    parts.append('\n\n  <!-- Latitude circles -->')
    parts.append('\n  <g>')
    for z in LATITUDES:
        is_equator = abs(z) < 1e-9
        if is_equator:
            parts.append(wire_runs(latitude_points(z), True,
                                    EQUATOR_W, WIRE_BACK_W,
                                    EQUATOR_FRONT_OPACITY, EQUATOR_BACK_OPACITY))
        else:
            parts.append(wire_runs(latitude_points(z), True,
                                    WIRE_FRONT_W, WIRE_BACK_W,
                                    WIRE_FRONT_OPACITY, WIRE_BACK_OPACITY))
    parts.append('\n  </g>')

    parts.append('\n\n  <!-- Longitude meridians -->')
    parts.append('\n  <g>')
    for k in range(N_MERIDIANS):
        phi = 2.0 * math.pi * k / N_MERIDIANS
        parts.append(wire_runs(meridian_points(phi), False,
                                WIRE_FRONT_W, WIRE_BACK_W,
                                WIRE_FRONT_OPACITY, WIRE_BACK_OPACITY))
    parts.append('\n  </g>')

    # --- Layer 3: silhouette (crisp outer boundary on top of the wireframe) ---
    parts.append('\n\n  <!-- Silhouette (pure-state boundary) -->')
    parts.append(
        f'\n  <circle cx="{CX}" cy="{CY}" r="{R}" '
        f'fill="none" stroke="{OUTLINE}" stroke-width="{SILHOUETTE_W}"/>'
    )

    # --- Layer 4: coordinate axes ---
    parts.append('\n\n  <!-- Coordinate axes -->')
    axis_targets = [
        ((AXIS_EXT, 0.0, 0.0),),    # +x
        ((0.0, AXIS_EXT, 0.0),),    # +y
    ]
    # x and y: from centre outward, arrowhead at the tip.
    for (tx, ty, tz), in axis_targets:
        sx0, sy0, _ = project((0.0, 0.0, 0.0))
        sx1, sy1, _ = project((tx, ty, tz))
        parts.append(
            f'\n  <line x1="{sx0:.2f}" y1="{sy0:.2f}" x2="{sx1:.2f}" y2="{sy1:.2f}" '
            f'stroke="{OUTLINE}" stroke-width="{AXIS_W}" marker-end="url(#arrow)"/>'
        )
    # z: polar axis from the south pole up through the top, arrowhead at +z.
    zb = project((0.0, 0.0, -1.0))
    zt = project((0.0, 0.0, AXIS_EXT))
    parts.append(
        f'\n  <line x1="{zb[0]:.2f}" y1="{zb[1]:.2f}" x2="{zt[0]:.2f}" y2="{zt[1]:.2f}" '
        f'stroke="{OUTLINE}" stroke-width="{AXIS_W}" marker-end="url(#arrow)"/>'
    )

    # --- Layer 5: state markers ---
    parts.append('\n\n  <!-- State markers -->')
    north = project((0.0, 0.0, 1.0))
    south = project((0.0, 0.0, -1.0))
    # The poles are pure states: green.
    for (sx, sy, _) in (north, south):
        parts.append(
            f'\n  <circle cx="{sx:.2f}" cy="{sy:.2f}" r="5.5" fill="{GREEN}"/>'
        )
    # Centre: the maximally mixed state I/2, a faint hollow ring.
    parts.append(
        f'\n  <circle cx="{CX}" cy="{CY}" r="7.5" '
        f'fill="#f7faf8" fill-opacity="0.55" stroke="{MIXED_RING}" '
        f'stroke-width="1.6" stroke-opacity="0.6"/>'
    )

    # --- Layer 6: labels ---
    parts.append('\n\n  <!-- Labels -->')

    def ket(sx, sy, text, dx, dy, anchor="middle", fill=OUTLINE):
        return (
            f'\n  <text x="{sx + dx:.2f}" y="{sy + dy:.2f}" text-anchor="{anchor}" '
            f'font-size="{KET_SIZE}" font-style="italic" fill="{fill}">{text}</text>'
        )

    # Pole kets are pure states: green, matching their dots.
    parts.append(ket(*north[:2], "|0\u27e9", -20, -10, anchor="end", fill=GREEN))
    parts.append(ket(*south[:2], "|1\u27e9", 0, 34, anchor="middle", fill=GREEN))

    # Axis labels at the arrow tips.
    xl = project((AXIS_LABEL_EXT, 0.0, 0.0))
    yl = project((0.0, AXIS_LABEL_EXT, 0.0))
    zl = project((0.0, 0.0, 1.32))
    parts.append(
        f'\n  <text x="{xl[0]:.2f}" y="{xl[1] + 6:.2f}" text-anchor="middle" '
        f'font-size="{AXIS_LABEL_SIZE}" font-style="italic" fill="{OUTLINE}">x</text>'
    )
    parts.append(
        f'\n  <text x="{yl[0] - 4:.2f}" y="{yl[1] + 6:.2f}" text-anchor="end" '
        f'font-size="{AXIS_LABEL_SIZE}" font-style="italic" fill="{OUTLINE}">y</text>'
    )
    parts.append(
        f'\n  <text x="{zl[0] + 8:.2f}" y="{zl[1]:.2f}" text-anchor="start" '
        f'font-size="{AXIS_LABEL_SIZE}" font-style="italic" fill="{OUTLINE}">z</text>'
    )

    # Centre label, de-emphasised like the ring.
    parts.append(
        f'\n  <text x="{CX + 14:.2f}" y="{CY - 2:.2f}" text-anchor="start" '
        f'font-size="{CENTER_LABEL_SIZE}" fill="{MIXED_RING}">{CENTER_LABEL}</text>'
    )

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "bloch_ball.svg"
    svg = build_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
