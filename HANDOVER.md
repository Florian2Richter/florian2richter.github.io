# HANDOVER — Clifford-roots blog post

Compact orientation for a fresh chat. Read this first, then review the
pushed state bug by bug.

## 1. Canonical state (where the real work is)
- All work lives on **`origin/main`** and **`origin/claude/quantum-upgrade`**,
  both at commit **`de8b83c`**. `de8b83c` is **deployed**.
- Live page (a `draft`, unlinked, so only reachable by URL):
  https://florian2richter.github.io/posts/clifford-roots/
- Post source: `posts/clifford-roots/index.qmd` (`draft: true`).
- Continue on **`claude/quantum-upgrade`**. (A previous container left a
  stale local checkout on the old branch `claude/blog-post-page-location-1friso`
  @ `cc41eb8`, 15 commits behind. Nothing was lost; everything is on origin.)

## 2. How to work
- Quarto is NOT preinstalled in a fresh container. Install it:
  download `quarto-1.9.38-linux-amd64.tar.gz` from the quarto-cli GitHub
  release, extract under `/tmp`, use `/tmp/quarto-1.9.38/bin/quarto`.
- Self-contained preview render:
  `quarto render posts/clifford-roots/index.qmd --embed-resources --standalone`
  → `docs/posts/clifford-roots/index.html` (`docs/` is gitignored). Send that
  file to read on iPad (JS animations play in Safari; MP4 previews via
  Pillow+imageio if the client won't run JS inline).
- Deploy = fast-forward `main` to `claude/quantum-upgrade` and push:
  `git checkout -B main origin/main && git merge --ff-only claude/quantum-upgrade && git push origin main`
  then `git checkout claude/quantum-upgrade`. GitHub Actions ("Publish to
  GitHub Pages") builds and serves; ~1-2 min.
- Hard rules (`CLAUDE.md`): **NO EM-DASHES**; no callout boxes; do not
  dismiss substantive questions as trivial. Voice target = Quantum Country.
  `CLAUDE.md` is authoritative; `PROJECT.md` is a frozen brief.

## 3. Structure (10 sections in index.qmd)
1. Hook  2. Classical setup  3. The quantum upgrade
4. **Coordinates for the Paulis** (interlude, new)  5. Clifford channels
as the playground  6. The reduction  7. Ingredient 1 (order of h)
8. Ingredient 2 (orbits / where lambda vanishes)  9. Punchline
10. What's next.

## 4. Figures (Quarto numbering)
- Fig 1 `fig-simplex-d3`: classical simplex, static; red/green/blue corners + grey centre.
- Fig 2 `fig-root-d3`: classical root, **animation** (cloud collapse 2D->1D->0D), plays on scroll, tap to replay. No coordinate axes (it is a triangle).
- Fig 3 `fig-bloch`: Bloch ball, **interactive** (click a direction + Purity slider + plain-words "certain question" readout). The **measurement axis (diameter) is drawn only ON CLICK**.
- Fig 4 `fig-bloch-root`: Bloch root, **animation** (cloud -> I/2 in stages z->y->x->0). Background stripped to **silhouette + coordinate axes only** (gridlines + purity field removed).
- Fig 5 `fig-clifford-grid`: continuum-vs-grid panel (Clifford restriction).
- Fig 6 `fig-orbit`: **placeholder, not built** — `figures/orbit-d3.svg` is missing, so it renders as a broken image.
- Conventions: `posts/clifford-roots/figures/README.md` and each figure's own README. Figure files: `*_figure.py` generator -> `.svg` -> inlined into `interactive.qmd` (+ `<style>`/`<script>`).

## 5. To review — the "bug by bug" list
1. **Axes (open user note):** on Fig 3 the measurement axis appears only after a click. Decide whether an axis should show by default; confirm Fig 4's coordinate axes actually render on the live site. (This is the "figure 2 / axes" question that was open when this handover was written.)
2. **Quantum bound not yet migrated:** section 3 still derives `k <= d^2 - 1` with the old "rank-one map / single nilpotent block on dimension D" phrasing. Planned: rewrite it to reuse the `S = P + N`, `S^k = P + N^k` framing from the classical section, for consistency. NOT done.
3. **Possible redundancy:** the honest caveat at the end of section 3 and the opener of section 5 both motivate the Clifford restriction via complete positivity / the huge channel space. Consider trimming section 5's opener.
4. **New interlude (section 4) review:** check the 4x4 Pauli multiplication table renders; that the flow into section 5 reads cleanly after the addresses/Weyl/projective material was relocated here; and the moved "why d must be prime" aside.
5. **Doc nit:** the docstring at the top of `fig3b-bloch-root/bloch_root_figure.py` still says "This figure is static: no interaction" — stale; it is now an animation (the README's Animation-layer section is correct).
6. **Citation TODOs** (see `CLAUDE.md` "Current state"): mixing-channels footnote (hook), classical-bound footnote (section 2), general `d^2-1` construction pointer + thesis title/PDF link (section 10).
7. **Publish:** flip `draft: false` in the frontmatter when ready.

## 6. Recently done (context, newest first)
- New Pauli-group interlude added; Clifford section slimmed to build on it.
- Removed "crush" / "tie our hands" wording (plainer, more scientific).
- Ease into the density matrix in section 3 (density matrix motivated as a classical distribution in disguise) and draw the measurement axis in Fig 3.
- Honest first-person caveat ending section 3 (Jordan block gives the bound, but complete positivity was unclear -> motivates Clifford channels).
- Fig 4 background stripped to silhouette + axes; Fig 4 turned into an animation; Fig 3 made interactive with the "certain question" readout.
- Expanded bit->qubit transition (geometry route), physical anchors (photon polarization, electron spin); Quantum Country pointer demoted to a footnote.
- Classical root derived via `S = P + N`; boxed central equation `S^k = P` with integers made explicit; d=2 matrix/eigenvalue put in display math.
- Classical figures recoloured to red/green/blue corners + grey centre; Fig 2 turned into an animation.
