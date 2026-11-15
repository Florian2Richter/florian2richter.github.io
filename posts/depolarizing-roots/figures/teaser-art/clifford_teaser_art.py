"""
Generate the teaser artwork for the clifford-roots post.

Not a schematic: a simulation. N random pure states on the Bloch sphere
are iterated under a stylized root-channel step -- rotate about an axis
that walks X -> Y -> Z (the skeleton walk) and contract by a constant
factor (the dials) -- and every trajectory is drawn as faint straight
chords (the steps are discrete). Thousands of overlaid chords braid into
a glowing vortex that collapses into a soft grey core: the completely
depolarizing channel P, divided into as many steps as the drawing has
chords.

Palette matches the blog figures: teal #2d6f8f filaments, pale #d6e5ea
highlights, grey #7d8a91 core, on a near-black petrol ground derived
from the ink #233746. Projection angles are the same as Figures 3-5.

Usage:
    python clifford_teaser_art.py [basename]

Writes {basename}-og.png (1200x630), {basename}-square.png
(1080x1080), and {basename}-card.png (1200x652, the aspect of the
image box in the blog's overview card). Defaults to clifford-teaser.
"""

from __future__ import annotations

import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap


# ---------------------------------------------------------------------------
# Knobs -- edit these to tweak the artwork.
# ---------------------------------------------------------------------------

SEED = 11

SEED_RINGS = [0.0, 0.45, -0.45]   # z-heights of the seed rings
N_PER_RING = 34        # seeds per ring, evenly spaced
N_STEPS = 110          # steps per trajectory (chords drawn per state)
ANGLE = 2 * np.pi / 5 + 0.045   # near-resonant: precessing star polygons
CONTRACT = 0.967       # dial contraction per step
WOBBLE = 0.05          # small x-tilt per step: braids the shells in 3D

ALPHA_HI, ALPHA_LO = 0.30, 0.06     # chord alpha, front vs back (depth cue)
LW_START, LW_END = 0.65, 0.35       # chord linewidth, outer vs inner

# Same camera as the blog's Bloch figures.
CAM_ALPHA = np.radians(35.0)
CAM_ELEV = np.radians(20.0)

BG = "#0b141b"          # near-black petrol, darkened from the ink #233746
SIL = "#2d6f8f"         # faint sphere silhouette
GREY = "#7d8a91"        # the core: P
# Trail colormap, outside -> inside: pale highlight -> blog teal -> grey.
TRAIL_STOPS = ["#1b4a63", "#2d6f8f", "#7fb3c9", "#d6e5ea"]

CORE_CUTOFF = 0.03      # trajectories stop rendering below this radius,
                        # so the collapse ends in ONE point, not a residual
                        # cluster of final chords
CORE_GLOW_LAYERS = 42   # concentric discs building the soft glow around P
CORE_GLOW_R = 0.16      # outer radius of the glow (sphere radius = 1)
SIL_ALPHA = 0.35

FORMATS = {"og": (12.0, 6.30), "square": (10.8, 10.8),
           "card": (12.0, 6.52)}   # inches at DPI
DPI = 100


# ---------------------------------------------------------------------------
# Simulation: the skeleton walk with contracting dials
# ---------------------------------------------------------------------------

def rot(axis: str, theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def simulate() -> np.ndarray:
    """Return trajectories, shape (n_seeds, N_STEPS + 1, 3)."""
    seeds = []
    for z0 in SEED_RINGS:
        rho = np.sqrt(1.0 - z0 * z0)
        for i in range(N_PER_RING):
            phi = 2 * np.pi * i / N_PER_RING
            seeds.append([rho * np.cos(phi), rho * np.sin(phi), z0])
    v = np.array(seeds)

    m = rot("x", WOBBLE) @ rot("z", ANGLE) * CONTRACT
    steps = [m] * N_STEPS

    out = np.empty((len(v), N_STEPS + 1, 3))
    out[:, 0] = v
    for k, m in enumerate(steps):
        out[:, k + 1] = out[:, k] @ m.T
    return out


def project(p: np.ndarray):
    """Orthographic projection with the blog camera. p is (..., 3).

    Returns (screen_xy, depth); depth > 0 faces the camera.
    """
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    u = x * np.cos(CAM_ALPHA) - y * np.sin(CAM_ALPHA)
    w = x * np.sin(CAM_ALPHA) + y * np.cos(CAM_ALPHA)
    v = z * np.cos(CAM_ELEV) - w * np.sin(CAM_ELEV)
    depth = z * np.sin(CAM_ELEV) + w * np.cos(CAM_ELEV)
    return np.stack([u, v], axis=-1), depth


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(traj: np.ndarray, figsize, out_path: str) -> None:
    xy, depth = project(traj)

    # One chord per (trajectory, step): segments (M, 2, 2).
    seg = np.stack([xy[:, :-1], xy[:, 1:]], axis=2).reshape(-1, 2, 2)
    seg_depth = 0.5 * (depth[:, :-1] + depth[:, 1:]).reshape(-1)
    n_traj = traj.shape[0]
    step_frac = np.broadcast_to(
        np.linspace(0.0, 1.0, N_STEPS), (n_traj, N_STEPS)).reshape(-1)

    # Cut the render just outside the core: the final chords would otherwise
    # pile up into visible specks next to the glow. Below the cutoff, the
    # glow alone stands for P.
    mid_r = 0.5 * (np.linalg.norm(traj[:, :-1], axis=-1)
                   + np.linalg.norm(traj[:, 1:], axis=-1)).reshape(-1)
    keep = mid_r > CORE_CUTOFF
    seg, seg_depth, step_frac = seg[keep], seg_depth[keep], step_frac[keep]

    cmap = LinearSegmentedColormap.from_list("trail", TRAIL_STOPS)
    rgba = cmap(step_frac)
    d01 = (seg_depth - seg_depth.min()) / (np.ptp(seg_depth) + 1e-12)
    rgba[:, 3] = ALPHA_LO + (ALPHA_HI - ALPHA_LO) * d01
    lw = LW_START + (LW_END - LW_START) * step_frac

    # Back-to-front so front chords glow on top.
    order = np.argsort(seg_depth)

    fig = plt.figure(figsize=figsize, dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    ax.add_collection(LineCollection(
        seg[order], colors=rgba[order], linewidths=lw[order],
        capstyle="round"))

    # Faint silhouette of the sphere.
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=SIL, lw=1.4, alpha=SIL_ALPHA)

    # The core: P, a soft grey glow built from concentric discs.
    for i in range(CORE_GLOW_LAYERS, 0, -1):
        r = CORE_GLOW_R * i / CORE_GLOW_LAYERS
        a = 0.10 * (1 - i / (CORE_GLOW_LAYERS + 1)) ** 2
        ax.add_patch(plt.Circle((0, 0), r, color=GREY, alpha=a, lw=0))
    ax.add_patch(plt.Circle((0, 0), 0.042, color="#dfe8ec", alpha=0.92, lw=0))
    ax.add_patch(plt.Circle((0, 0), 0.014, color="#f2f6f8", alpha=0.95, lw=0))

    aspect = figsize[0] / figsize[1]
    if aspect >= 1:
        half_h = 1.18
        ax.set_ylim(-half_h, half_h)
        ax.set_xlim(-half_h * aspect, half_h * aspect)
    else:
        half_w = 1.18
        ax.set_xlim(-half_w, half_w)
        ax.set_ylim(-half_w / aspect, half_w / aspect)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.savefig(out_path, dpi=DPI, facecolor=BG)
    plt.close(fig)
    print(f"wrote {out_path}")


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "clifford-teaser"
    traj = simulate()
    for name, figsize in FORMATS.items():
        render(traj, figsize, f"{base}-{name}.png")


if __name__ == "__main__":
    main()
