"""
Generate the Bloch-ball root-trajectory figure (Figure 3b).

The quantum analogue of the simplex square-root figure (Figure 2): the
maximal qubit root S driving every state to the centre I/2 in stages,
not in one shot. On the Bloch vector S acts as

    (r1, r2, r3)  ->  (r2/2, r3/2, 0).

We draw three pure axis states and their orbits under S. The z-pole is
the hero: it takes the full three steps and so realises the order-3
bound (d^2 - 1 = 3 at d = 2). The x-axis is already in the channel's
kernel and collapses in one step.

    (0,0,1) -> (0,1/2,0) -> (1/4,0,0) -> 0    (3 steps, maximal)
    (0,1,0) -> (1/2,0,0) -> 0                  (2 steps)
    (1,0,0) -> 0                               (1 step)

The sphere, axes, wireframe, palette and projection are shared with
bloch_ball_figure.py (Figure 3). This figure is static: no interaction.

Usage:
    python bloch_root_figure.py [output.svg]

Defaults to ./bloch-root-d2.svg.
"""

from __future__ import annotations

import math
import sys


# ---------------------------------------------------------------------------
# Knobs -- shared with bloch_ball_figure.py (Figure 3).
# ---------------------------------------------------------------------------

CANVAS = (640, 640)
CX, CY = 320.0, 332.0
R = 210.0

ALPHA = math.radians(35.0)   # azimuth
ELEV = math.radians(20.0)    # elevation above the equator

# Blue-grey scientific palette (shared).
OUTLINE = "#829aa6"      # wireframe / grid lines (muted blue-grey)
PURE = "#2d6f8f"         # silhouette boundary + poles (blue-teal)
AXIS = "#233746"         # axes + text labels (dark blue-grey)
MIXED = "#d6e5ea"        # gradient centre (soft blue-grey)
MIXED_RING = "#5e7886"   # the recessed I/2 dot (muted blue-grey)
CENTER = "#f5f7f8"       # centre marker fill

# Purity field endpoints (lerp low -> high), as in Figures 1 and 2.
PURE_RGB = (45, 111, 143)
MIXED_RGB = (214, 229, 234)
DARK_DOT = "#1c4a60"     # dot outlines, so pale (mixed) dots stay visible

# Trajectory colours. The two ordinary orbits are neutral grey (as the
# baked trajectories in Figure 2); the hero z-pole orbit is the strong
# blue used for moving objects across the post.
ARROW_GREY = "#829aa6"
HERO_BLUE = "#1565c0"
HERO_DARK = "#0d3f8f"

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

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

LATITUDES = [0.78, 0.42, 0.0, -0.42, -0.78]
N_MERIDIANS = 8
SAMPLES = 180

AXIS_EXT = 1.18
AXIS_LABEL_EXT = 1.42

KET_SIZE = 21
AXIS_LABEL_SIZE = 20
CENTER_LABEL_SIZE = 20
CENTER_LABEL = "I/2"

# Trajectory dot radii and arrow widths.
DOT_START = 6.0
DOT_MID = 5.0
ARROW_W = 2.0
HERO_ARROW_W = 2.7
SEC_OPACITY = 0.85


# ---------------------------------------------------------------------------
# Projection (shared with Figure 3)
# ---------------------------------------------------------------------------

def project(p):
    x, y, z = p
    u = R * (x * math.cos(ALPHA) - y * math.sin(ALPHA))
    w = x * math.sin(ALPHA) + y * math.cos(ALPHA)
    v = R * (z * math.cos(ELEV) - w * math.sin(ELEV))
    depth = z * math.sin(ELEV) + w * math.cos(ELEV)
    return (CX + u, CY - v, depth)


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


# ---------------------------------------------------------------------------
# Purity -> colour (shared convention: t = r^2, 0 at centre, 1 on surface)
# ---------------------------------------------------------------------------

def purity_colour(p):
    t = max(0.0, min(1.0, p[0] ** 2 + p[1] ** 2 + p[2] ** 2))
    r = round(MIXED_RGB[0] + t * (PURE_RGB[0] - MIXED_RGB[0]))
    g = round(MIXED_RGB[1] + t * (PURE_RGB[1] - MIXED_RGB[1]))
    b = round(MIXED_RGB[2] + t * (PURE_RGB[2] - MIXED_RGB[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


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


def shorten2d(a, b, ts, te):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    if L < ts + te + 1e-6:
        return a, b
    ux, uy = dx / L, dy / L
    return (a[0] + ts * ux, a[1] + ts * uy), (b[0] - te * ux, b[1] - te * uy)


def build_svg():
    width, height = CANVAS
    parts = []

    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="{FONT_FAMILY}" '
        f'role="img" aria-label="The maximal qubit root S driving Bloch '
        f'vectors to the centre in stages" '
        f'data-cx="{CX:g}" data-cy="{CY:g}" data-r="{R:g}" '
        f'data-alpha-deg="{math.degrees(ALPHA):g}" '
        f'data-elev-deg="{math.degrees(ELEV):g}">'
    )

    parts.append(f'''
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{AXIS}"/>
    </marker>
    <marker id="arrowG" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{ARROW_GREY}"/>
    </marker>
    <marker id="arrowB" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{HERO_BLUE}"/>
    </marker>
  </defs>''')

    # (Background wireframe removed for the animation: no purity field and no
    # latitude/longitude gridlines. Only the silhouette and the coordinate axes
    # survive, mirroring the stripped-down classical state-space sketch.)

    # --- Silhouette ---
    parts.append('\n\n  <!-- Silhouette (pure-state boundary) -->')
    parts.append(f'\n  <circle cx="{CX}" cy="{CY}" r="{R}" fill="none" '
                 f'stroke="{PURE}" stroke-width="{SILHOUETTE_W}"/>')

    # --- Coordinate axes ---
    parts.append('\n\n  <!-- Coordinate axes -->')
    for tgt in ((AXIS_EXT, 0.0, 0.0), (0.0, AXIS_EXT, 0.0)):
        sx0, sy0, _ = project((0.0, 0.0, 0.0))
        sx1, sy1, _ = project(tgt)
        parts.append(f'\n  <line x1="{sx0:.2f}" y1="{sy0:.2f}" '
                     f'x2="{sx1:.2f}" y2="{sy1:.2f}" stroke="{AXIS}" '
                     f'stroke-width="{AXIS_W}" marker-end="url(#arrow)"/>')
    zb = project((0.0, 0.0, -1.0))
    zt = project((0.0, 0.0, AXIS_EXT))
    parts.append(f'\n  <line x1="{zb[0]:.2f}" y1="{zb[1]:.2f}" '
                 f'x2="{zt[0]:.2f}" y2="{zt[1]:.2f}" stroke="{AXIS}" '
                 f'stroke-width="{AXIS_W}" marker-end="url(#arrow)"/>')

    # --- Animated layers, filled by the script ---
    # The resting axis orbits, the collapsing cloud of Bloch vectors, their
    # trails and the highlighted hero orbits are all rebuilt by the script from
    # the map S, so the generator emits only empty layers here. With JS off,
    # the bare ball still renders.
    parts.append('\n\n  <!-- Layers filled by the script (resting orbits, trails, cloud, hero) -->')
    parts.append('\n  <g class="resting"></g>')
    parts.append('\n  <g class="trails"></g>')
    parts.append('\n  <g class="cloud"></g>')
    parts.append('\n  <g class="hl"></g>')

    # --- Centre: maximally mixed state I/2, depth-cued (it sits inside the
    # ball): a muted blue-grey dot, a little transparent, recessed. ---
    parts.append('\n\n  <!-- Maximally mixed state I/2 (recessed, depth-cued) -->')
    parts.append(f'\n  <circle cx="{CX}" cy="{CY}" r="8.5" fill="{CENTER}" '
                 f'fill-opacity="0.5"/>')
    parts.append(f'\n  <circle cx="{CX}" cy="{CY}" r="5.5" fill="{MIXED_RING}" '
                 f'fill-opacity="0.85"/>')

    # --- Labels ---
    parts.append('\n\n  <!-- Labels -->')
    north = project((0.0, 0.0, 1.0))
    south = project((0.0, 0.0, -1.0))

    def ket(sx, sy, text, dx, dy, anchor="middle", fill=AXIS):
        return (f'\n  <text x="{sx + dx:.2f}" y="{sy + dy:.2f}" '
                f'text-anchor="{anchor}" font-size="{KET_SIZE}" '
                f'font-style="italic" fill="{fill}">{text}</text>')

    parts.append(ket(*north[:2], "|0⟩", -20, -10, anchor="end"))
    parts.append(ket(*south[:2], "|1⟩", 0, 34, anchor="middle"))

    xl = project((AXIS_LABEL_EXT, 0.0, 0.0))
    yl = project((0.0, AXIS_LABEL_EXT, 0.0))
    zl = project((0.0, 0.0, 1.32))
    parts.append(f'\n  <text x="{xl[0]:.2f}" y="{xl[1] + 6:.2f}" '
                 f'text-anchor="middle" font-size="{AXIS_LABEL_SIZE}" '
                 f'font-style="italic" fill="{AXIS}">x</text>')
    parts.append(f'\n  <text x="{yl[0] - 4:.2f}" y="{yl[1] + 6:.2f}" '
                 f'text-anchor="end" font-size="{AXIS_LABEL_SIZE}" '
                 f'font-style="italic" fill="{AXIS}">y</text>')
    parts.append(f'\n  <text x="{zl[0] + 8:.2f}" y="{zl[1]:.2f}" '
                 f'text-anchor="start" font-size="{AXIS_LABEL_SIZE}" '
                 f'font-style="italic" fill="{AXIS}">z</text>')

    parts.append(f'\n  <text x="{CX + 14:.2f}" y="{CY - 2:.2f}" '
                 f'text-anchor="start" font-size="{CENTER_LABEL_SIZE}" '
                 f'fill="{MIXED_RING}">{CENTER_LABEL}</text>')

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "bloch-root-d2.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
