"""
Generate the d=3 orbit-cycle figure for the higher-dimensions section.

The eight nonzero labels of the plane F_3^2, arranged on a ring in the
order the companion matrix h = [[0,1],[1,2]] (companion of the primitive
polynomial x^2 + x + 2) visits them:

    (1,0) -> (0,1) -> (1,2) -> (2,2) -> (2,0) -> (0,2) -> (2,1) -> (1,1) -> (1,0)

The mirror pair (1,0) / (2,0), where lambda vanishes, sits at opposite
ends of a dashed horizontal diameter (advancing half the cycle is
multiplication by -1), splitting the ring into two arcs of four steps.

Styling follows the other figure generators: same palette, Georgia
serif, geometry as named constants. Point-grid styling (solid dots,
coordinate labels) matches fig5-continuum-grid's right panel, so the
reader meets this ring already knowing how to read it. The purity
colour scheme does NOT apply: this is the label plane, not a state
space. Static (no interactive layer).

Usage:
    python orbit_cycle_figure.py [output.svg]

Defaults to ./orbit-d3.svg.
"""

from __future__ import annotations

import math
import sys


# ---------------------------------------------------------------------------
# Knobs
# ---------------------------------------------------------------------------

CANVAS = (560, 400)
FONT_FAMILY = "Georgia, 'Times New Roman', serif"

# Palette (shared with the other figures).
AXIS = "#233746"        # dark blue-grey: upper-arc arrows, text
TEAL = "#2d6f8f"        # lower-arc arrows
GRID = "#829aa6"        # faint underlay ring
CORAL = "#c25b4e"       # the vanishing mirror pair
GREY = "#7d8a91"        # the dashed mirror diameter

CX, CY, R = 280.0, 190.0, 130.0   # ring centre and radius

# Cycle order of the eight nonzero labels under h, starting at (1,0).
LABELS = ["(1,0)", "(0,1)", "(1,2)", "(2,2)",
          "(2,0)", "(0,2)", "(2,1)", "(1,1)"]
ZERO_IDX = {0, 4}       # where lambda vanishes: (1,0) and its mirror (2,0)

PT_R = 7.0              # point radius (matches fig5's grid points)
HALO_R = 12.5           # highlight ring around the vanishing pair
ARROW_W = 1.8
PAD_DEG = 7.0           # angular trim so arrowheads clear the markers
LABEL_OFF = 26.0        # radial offset of the coordinate labels
LABEL_SIZE = 14
SUB_SIZE = 15
DASH = "3,4"


def pt(theta_deg, radius=R):
    th = math.radians(theta_deg)
    return (CX + radius * math.cos(th), CY - radius * math.sin(th))


def angle_of(k):
    """Label k sits at 180 - 45k degrees: (1,0) leftmost, (2,0) rightmost."""
    return 180.0 - 45.0 * k


# ---------------------------------------------------------------------------
# SVG pieces
# ---------------------------------------------------------------------------

def text(x, y, body, size, fill, anchor="middle", italic=False):
    style = ' font-style="italic"' if italic else ""
    return (f'\n  <text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
            f'font-size="{size}" fill="{fill}"{style}>{body}</text>')


def named_marker(mid, colour):
    return (f'\n    <marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{colour}"/></marker>')


def step_arc(k, colour, marker):
    """Directed arc along the ring from label k to label k+1, trimmed."""
    a1 = angle_of(k) - PAD_DEG
    a2 = angle_of(k) - 45.0 + PAD_DEG
    s, e = pt(a1), pt(a2)
    return (f'\n  <path d="M {s[0]:.2f} {s[1]:.2f} '
            f'A {R:g} {R:g} 0 0 1 {e[0]:.2f} {e[1]:.2f}" '
            f'fill="none" stroke="{colour}" stroke-width="{ARROW_W}" '
            f'stroke-linecap="round" marker-end="url(#{marker})"/>')


def label_anchor(k):
    c = math.cos(math.radians(angle_of(k)))
    if c > 0.35:
        return "start"
    if c < -0.35:
        return "end"
    return "middle"


def build_svg():
    width, height = CANVAS
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="{FONT_FAMILY}" role="img" '
        f'aria-label="The eight nonzero labels of the plane F_3^2 on a ring, '
        f'stepped around a single cycle by the matrix h. The mirror pair (1,0) '
        f'and (2,0), where lambda vanishes, sits at opposite ends of a dashed '
        f'diameter, splitting the ring into two arcs of four steps each.">'
    )

    parts.append('\n  <defs>')
    parts.append(named_marker("arrowOcA", AXIS))
    parts.append(named_marker("arrowOcT", TEAL))
    parts.append('\n  </defs>')

    # Faint underlay ring (continuity beneath the trimmed arrow gaps).
    parts.append(
        f'\n  <circle cx="{CX:g}" cy="{CY:g}" r="{R:g}" fill="none" '
        f'stroke="{GRID}" stroke-width="1" stroke-opacity="0.18"/>'
    )

    # The dashed mirror diameter between the two vanishing labels.
    left, right = pt(180.0), pt(0.0)
    trim = 20.0
    parts.append('\n\n  <!-- mirror diameter: advancing half the cycle is multiplication by -1 -->')
    parts.append(
        f'\n  <line x1="{left[0] + trim:.2f}" y1="{left[1]:.2f}" '
        f'x2="{right[0] - trim:.2f}" y2="{right[1]:.2f}" '
        f'stroke="{GREY}" stroke-width="1.2" stroke-dasharray="{DASH}" '
        f'stroke-opacity="0.6"/>'
    )
    parts.append(text(CX, CY - 10, '&#951; &#8614; &#8722;&#951;', 13, GREY,
                      anchor="middle", italic=True))

    # The eight directed steps: upper arc dark, lower arc teal.
    parts.append('\n\n  <!-- the grand cycle of h: upper arc, then lower arc -->')
    for k in range(4):
        parts.append(step_arc(k, AXIS, "arrowOcA"))
    for k in range(4, 8):
        parts.append(step_arc(k, TEAL, "arrowOcT"))

    # "h" tag beside the (1,2) -> (2,2) step on the upper arc.
    hx, hy = pt(67.5, R + 26.0)
    parts.append(text(hx, hy + 5, "h", 18, AXIS, anchor="middle", italic=True))

    # Points, halos on the vanishing pair, coordinate labels.
    parts.append('\n\n  <!-- the eight labels -->')
    for k, lab in enumerate(LABELS):
        x, y = pt(angle_of(k))
        if k in ZERO_IDX:
            parts.append(
                f'\n  <circle cx="{x:.2f}" cy="{y:.2f}" r="{HALO_R:g}" '
                f'fill="none" stroke="{CORAL}" stroke-width="1.6" '
                f'stroke-opacity="0.55"/>'
            )
            colour = CORAL
        else:
            colour = AXIS
        parts.append(
            f'\n  <circle cx="{x:.2f}" cy="{y:.2f}" r="{PT_R:g}" fill="{colour}"/>'
        )
        lx, ly = pt(angle_of(k), R + LABEL_OFF)
        parts.append(text(lx, ly + 5, lab, LABEL_SIZE, colour,
                          anchor=label_anchor(k)))

    # "lambda = 0" tags beneath the two vanishing labels.
    lx, ly = pt(180.0, R + LABEL_OFF)
    parts.append(text(lx, ly + 27, '&#955; = 0', 13, CORAL,
                      anchor="end", italic=True))
    rx, ry = pt(0.0, R + LABEL_OFF)
    parts.append(text(rx, ry + 27, '&#955; = 0', 13, CORAL,
                      anchor="start", italic=True))

    # Sub-label.
    parts.append(text(CX, height - 15,
                      "the grand cycle of h on the labels, d = 3",
                      SUB_SIZE, AXIS, anchor="middle", italic=True))

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "orbit-d3.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
