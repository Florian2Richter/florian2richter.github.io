"""
Generate the "bouquet of sheets" figure for the Clifford section.

One panel. A large, gently irregular convex blob stands for the full
set of unital qubit channels (a nine-parameter continuum). Through its
centre point P (the completely depolarizing channel, drawn as the same
neutral grey dot that marks the maximally mixed state in Figures 1, 3
and 5) runs a small bouquet of thin straight segments: the Clifford
channels. One segment per skeleton h -- finitely many -- and along each
segment the dials vary continuously, so the family is NOT a discrete
set of points but a finite collection of low-dimensional sheets, drawn
here as needles. All needles pass through P, because every skeleton
with all dials zero is P. The identity channel sits at the tip of the
identity-skeleton needle and is marked "id".

The needles are drawn as 1D lines although each sheet is really
three-dimensional (one dial per axis); the figure caption in the .qmd
should carry that caveat.

Companion to the other figure generators: same restrained palette, all
geometry as named constants at the top, SVG layers separated by comment
headers. Static (no interactive layer): it is a conceptual sketch.

Usage:
    python clifford_bouquet_figure.py [output.svg]

Defaults to ./clifford-bouquet-d2.svg.
"""

from __future__ import annotations

import math
import sys


# ---------------------------------------------------------------------------
# Knobs -- edit these to tweak the figure.
# ---------------------------------------------------------------------------

CANVAS = (680, 372)        # viewBox width, height

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

# Palette, shared with the other figures. Neutral structure in the dark
# blue-grey ink; the Clifford needles take the blue-teal that marks
# "quantum structure" throughout (the Bloch silhouette colour); the two
# distinguished channels P and id are a grey dot (the recurring colour of
# the maximally mixed / no-information point) and a teal dot.
AXIS = "#233746"        # text (dark blue-grey ink)
GRID = "#829aa6"        # faint guides, blob outline (muted blue-grey)
TEAL = "#2d6f8f"        # the Clifford needles and the identity tip
GREY = "#7d8a91"        # P, the completely depolarizing channel
MIXED = "#d6e5ea"       # blob interior (soft blue-grey, the "purity core")

# --- The blob: all unital qubit channels ---
BCX, BCY = 340.0, 190.0     # blob centre
BRX, BRY = 268.0, 132.0     # blob semi-axes before modulation
# Gentle radius modulation so the blob reads "generic convex body",
# not "the Bloch ball again". Amplitudes are fractions of the radius.
WOBBLES = [(2, 0.040, 0.8), (3, 0.030, -1.2)]   # (harmonic, amplitude, phase)
BLOB_SAMPLES = 240
BLOB_STROKE_W = 1.6
BLOB_FILL_OPACITY = 0.35

# --- The bouquet: one needle per skeleton h, all through P ---
P_POS = (340.0, 212.0)      # P sits a little below the blob centre so the
                            # title inside the blob top has room to breathe
# Needles as (angle_deg, forward_len, backward_len). Angle is measured
# from +x, screen-y pointing down. Forward = toward positive dials.
# The first entry is the identity skeleton; its forward tip is "id".
NEEDLES = [
    (-18.0, 190.0, 95.0),    # identity skeleton, tip marked "id"
    (-48.0, 92.0, 74.0),
    (-100.0, 74.0, 64.0),
    (-152.0, 150.0, 90.0),
    (168.0, 168.0, 108.0),
    (112.0, 100.0, 72.0),
]
NEEDLE_W = 2.6
NEEDLE_OPACITY = 0.85

P_R = 5.5                   # radius of the P dot
ID_R = 4.5                  # radius of the identity-channel dot

# --- Text ---
LABEL_SIZE = 15
TITLE_POS = (340.0, 96.0)       # "all unital qubit channels"
SUBTITLE_POS = (340.0, 117.0)   # "a nine-parameter continuum"
CAPTION_POS = (340.0, 354.0)    # italic bottom caption
P_LABEL_OFFSET = (14.0, 24.0)   # from P, anchor "start", in the
                                # clear wedge toward lower right
ID_LABEL_OFFSET = (11.0, -4.0)  # from the id tip, anchor "start"

CAPTION = "the Clifford channels: finitely many sheets through P"


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def blob_radius(theta):
    """Radius modulation factor at parameter angle theta."""
    r = 1.0
    for harmonic, amp, phase in WOBBLES:
        r += amp * math.sin(harmonic * theta + phase)
    return r


def blob_points(samples=BLOB_SAMPLES):
    pts = []
    for i in range(samples):
        theta = 2.0 * math.pi * i / samples
        r = blob_radius(theta)
        pts.append((BCX + BRX * r * math.cos(theta),
                    BCY + BRY * r * math.sin(theta)))
    return pts


def needle_endpoints(angle_deg, fwd, bwd):
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    px, py = P_POS
    return ((px - bwd * ux, py - bwd * uy),
            (px + fwd * ux, py + fwd * uy))


# ---------------------------------------------------------------------------
# SVG emission
# ---------------------------------------------------------------------------

def text(x, y, body, size, fill, anchor="middle", italic=False):
    style = ' font-style="italic"' if italic else ""
    return (
        f'\n  <text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
        f'font-size="{size}" fill="{fill}"{style}>{body}</text>'
    )


def build_svg():
    width, height = CANVAS
    parts = []

    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="{FONT_FAMILY}" '
        f'role="img" aria-label="A large convex blob, the nine-parameter '
        f'continuum of unital qubit channels. Through the grey point P at '
        f'its centre, the completely depolarizing channel, runs a bouquet '
        f'of six thin straight needles, the Clifford channels: one sheet '
        f'per skeleton, dials varying along each, all sheets meeting at P. '
        f'The identity channel sits at the tip of one needle, marked id.">'
    )

    # ================== The blob: all unital qubit channels ==================
    parts.append('\n\n  <!-- The ambient space: all unital qubit channels, '
                 'a gently irregular convex blob -->')
    pts = blob_points()
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"
    parts.append(
        f'\n  <path d="{d}" fill="{MIXED}" fill-opacity="{BLOB_FILL_OPACITY}" '
        f'stroke="{GRID}" stroke-width="{BLOB_STROKE_W}" '
        f'stroke-linejoin="round"/>'
    )

    parts.append(text(*TITLE_POS, "all unital qubit channels",
                      LABEL_SIZE, AXIS))
    parts.append(text(*SUBTITLE_POS, "a nine-parameter continuum",
                      LABEL_SIZE, GREY))

    # ============ The bouquet: one needle per skeleton, through P ============
    parts.append('\n\n  <!-- The Clifford channels: one needle per skeleton '
                 'h, dials varying along each, all through P -->')
    id_tip = None
    for i, (angle, fwd, bwd) in enumerate(NEEDLES):
        (x1, y1), (x2, y2) = needle_endpoints(angle, fwd, bwd)
        parts.append(
            f'\n  <line x1="{x1:.2f}" y1="{y1:.2f}" '
            f'x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{TEAL}" stroke-width="{NEEDLE_W}" '
            f'stroke-opacity="{NEEDLE_OPACITY}" stroke-linecap="round"/>'
        )
        if i == 0:
            id_tip = (x2, y2)

    # ==================== The two distinguished channels ====================
    parts.append('\n\n  <!-- P (the CDC, shared grey of the maximally mixed '
                 'point) and the identity channel at one needle tip -->')
    parts.append(
        f'\n  <circle cx="{id_tip[0]:.2f}" cy="{id_tip[1]:.2f}" '
        f'r="{ID_R}" fill="{TEAL}"/>'
    )
    parts.append(
        f'\n  <circle cx="{P_POS[0]:.2f}" cy="{P_POS[1]:.2f}" '
        f'r="{P_R}" fill="{GREY}"/>'
    )

    parts.append(text(P_POS[0] + P_LABEL_OFFSET[0],
                      P_POS[1] + P_LABEL_OFFSET[1],
                      "P", LABEL_SIZE, GREY, anchor="start", italic=True))
    parts.append(text(id_tip[0] + ID_LABEL_OFFSET[0],
                      id_tip[1] + ID_LABEL_OFFSET[1],
                      "id", LABEL_SIZE, TEAL, anchor="start", italic=True))

    # ============================== Caption ==============================
    parts.append(text(*CAPTION_POS, CAPTION, LABEL_SIZE, AXIS, italic=True))

    parts.append('\n</svg>\n')
    return "".join(parts)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "clifford-bouquet-d2.svg"
    svg = build_svg()
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
