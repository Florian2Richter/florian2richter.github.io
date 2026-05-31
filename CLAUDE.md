# CLAUDE.md

This is the source for [florian2richter.github.io](https://florian2richter.github.io),
a personal blog built with Quarto. The current focus is one in-flight
post on Clifford channels as finite roots of the depolarizing channel.

## What this repo is

- **Static site, built with Quarto.** Source files are `.qmd`. Generated
  HTML goes to `docs/`, served by GitHub Pages via the `gh-pages`
  branch (deployed by `.github/workflows/publish.yml`).
- **Math rendering** is MathJax (Quarto default).
- **The current post in progress** is `posts/clifford-roots/index.qmd`,
  working title *"How finely can you divide a depolarizing channel?"*.
- **`PROJECT.md`** at the repo root has the original project brief:
  the result being explained, the structure, the source material.
- **`reference/Diplomarbeit_Florian.pdf`** is the source thesis
  (Florian Richter, Diploma Thesis, Hannover 2010). Chapter 5 is the
  primary source for the post.

## How to work on it

```bash
quarto preview     # local server with hot reload
quarto render      # one-shot build to docs/
```

Posts live at `posts/<slug>/index.qmd`. Figures and figure scripts go
in `posts/<slug>/figures/` (see the README in
`posts/clifford-roots/figures/` for the convention).

## Audience and voice

The Clifford post is written for **a stranger from Hacker News learning
the math from scratch**, not a colleague reading in one sitting.
Pedagogy wins over brevity; length is a result, not a target. A
two-post split at the reduction (section 5) is on the table if the
single post grows past about 7000 words.

The voice target is **Matuschak and Nielsen's
[Quantum Country](https://quantum.country/qcvc)**. Specifically:

- Short sentences, short paragraphs, variable rhythm.
- Concrete before abstract: show a specific matrix doing a specific
  thing before naming the category.
- Explicit signposting ("Here's the question that sounds silly until
  you take it seriously"), conversational confusion-acknowledgments
  ("That perhaps sounds strange!").
- First-person plural ("we") for the math journey, first-person
  singular ("I") sparingly for honest asides.
- Italics for emphasis, sparingly, on the conceptually loaded word.
- Equations framed by prose before and after, not displayed in
  isolation.
- Story-first openings; no math in the hook of a section.

## Hard rules

- **NO EM-DASHES.** Never. Use commas, colons, parentheses,
  semicolons, or split into shorter sentences. Applies to all prose
  written for Florian, in the blog or elsewhere.
- **No callout boxes** for prerequisites or asides. Inline as prose
  or as parenthetical remarks. (Florian rejected the
  `::: {.callout-note}` layout.)
- **Don't dismiss substantive questions as "easy" or "trivial"** in
  the prose. If a question has its own literature (e.g. characterising
  channels that converge to a fixed point in the infinite limit), say
  so and point at it.

## Structural plan for the Clifford post

1. **Hook.** Photocopy-of-a-photocopy framing. No math.
2. **The classical setup.** Simplex, stochastic matrices, the
   bistochastic CDC, divisibility, the $d - 1$ bound, $d = 3$ worked
   example.
3. **The quantum upgrade.** Density matrices, channels, the maximally
   mixed state. Bound jumps to $d^2 - 1$. Quantum Country
   recommendation lives at the top of this section.
4. **Clifford channels as the playground.** Weyl operators,
   projective representation,
   $T[\mathbf{w}(\eta)] = \lambda(\eta)\,\mathbf{w}(h(\eta))$. "Two
   pieces of data."
5. **The reduction (pivot).** $T^n$ acts on Weyl labels by $h^n$ with
   a product of $\lambda$'s along the orbit. The channel question
   becomes a question about a linear map on $\mathbb{F}_d^2$.
6. **Ingredient 1: the order of $h$.** Max order $d^2 - 1$ via
   companion matrix of a primitive polynomial. Finite-field sidebar
   at moment of need.
7. **Ingredient 2: orbits and where $\lambda$ vanishes.** Transitive
   action on $\mathbb{F}_d^2 \setminus \{0\}$, $\lambda$ vanishing on
   one inverse pair, bound $\frac{d^2 - 1}{2}$.
8. **Punchline.** The room lives in the orbit structure of $h$, not
   in channel richness.
9. **What's next.** Pointer to the published paper for the general
   $d^2 - 1$ construction.

## Current state

- **Drafted:** all nine sections (1 through 9). Full first draft,
  awaiting Florian's revision pass.
- **Inline expandable asides** (`<details class="aside">`, styled in
  `styles.css`) hide the heavier derivations: the linearity argument,
  the row-sum computation, the $d^2-1$ parameter count, the explicit
  Weyl operators / why $d$ is prime, primitive polynomials, and the
  $\lambda(-\eta)=\overline{\lambda(\eta)}$ derivation. Claim stays in
  the text, derivation one click away. Click-to-expand, not hover
  (hover fails on touch and can't hold display math).
- **No figures yet.** Four placeholders point at files that don't
  exist: `figures/simplex-d3.svg`, `figures/simplex-root-d3.svg`
  (section 2), `figures/bloch-ball.svg` (section 3),
  `figures/orbit-d3.svg` (section 7, the eight-point $d=3$ cycle).
- **Citation TODOs:** mixing-channels footnote in the hook (candidates
  to verify), classical-bound footnote (section 2), the general
  $d^2-1$ construction (section 9, working title only), and confirm
  the exact thesis title + add a PDF link (section 9). The channels
  footnote in section 3 (Nielsen & Chuang ch. 8, Wolf notes) is a real
  citation.
- **Worked example thread:** $d=3$ (qutrit) runs through sections 6-8.
  Primitive polynomial $x^2+x+2$, companion matrix $h=\binom{0\ 1}{1\ 2}$,
  the explicit 8-cycle, mirror-pair zeros at $(1,0)/(2,0)$, root of
  order 4. The three bounds for $d=3$ are 2 / 4 / 8.
- **`draft: true`** is set on the post frontmatter. With
  `draft-mode: unlinked` in `_quarto.yml`, the post renders in full at
  its direct URL but stays out of the blog index, feed, and search.
  Flip to `draft: false` to publish.

## Preview server gotcha

Do NOT run `quarto render` while `quarto preview` is live: they fight
over the `.quarto` cache and wedge the preview's file watcher, which
shows up as "missing chapters" (stale page). Let the preview server do
the rendering; if it goes stale, kill it (the child process is a
`deno`, find it with `ss -ltnp | grep <port>` and `kill -9` the pid)
and restart `quarto preview`.

## Branches

- **`main`:** Quarto site, work-in-progress.
- **`archive/jekyll-site`:** snapshot of the previous Jekyll-based
  site (including the unfinished 1D Symplectic Cellular Automata
  post). Preserved for reference; not used in the current build.
