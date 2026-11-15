# CLAUDE.md

This is the source for [florian2richter.github.io](https://florian2richter.github.io),
a personal blog built with Quarto. The current focus is a two-part
series on finite roots of the completely depolarizing channel.

## What this repo is

- **Static site, built with Quarto.** Source files are `.qmd`. Generated
  HTML goes to `docs/`, served by GitHub Pages via the `gh-pages`
  branch (deployed by `.github/workflows/publish.yml`).
- **Math rendering** is KaTeX (`html-math-method: katex` in
  `_quarto.yml`).
- **The series in progress** has two posts:
  - Part 1, `posts/depolarizing-roots/index.qmd`, *"How finely can you
    divide a depolarizing channel?"*: preface, hook, the classical
    bound $d - 1$, the general quantum bound $d^2 - 1$. This is the
    launch post and is worked on first.
  - Part 2, `posts/clifford-roots/index.qmd` (`draft: true`): Pauli
    and Weyl labels, Clifford channels, the bound $(d^2 - 1)/2$.
  Part 2 links to part 1's figures `#fig-bloch` and `#fig-bloch-root`
  by URL. Open edits are marked `TODO(Florian)` in the sources.
- **Part 1 is in skeleton mode.** Its chapters hold English keyword
  boxes (`::: {.skeleton}`, styled in `styles.css`) between the fixed
  math, figures, asides and footnotes. Florian replaces each box with
  his own prose. The previous LLM text is kept unrendered in
  `posts/depolarizing-roots/_llm-text/`.
- **The English prose is to be rewritten by Florian himself.** The
  plan and the list of passages to rewrite are in
  `posts/depolarizing-roots/REWRITE-OUTLINE.md` (German). Do not
  write or polish blog prose unless he explicitly asks for it.
- **`PROJECT.md`** at the repo root is the original project brief:
  the result being explained, the angle, the source material, and what
  not to do. It is a frozen snapshot from the start of the project.
  This file, `CLAUDE.md`, is the authoritative living source for how to
  work, voice, structure, hard rules, and current state. Where the two
  overlap, `CLAUDE.md` wins.
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
`posts/depolarizing-roots/figures/` for the convention).

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

## Expandable asides (math derivations)

These are the click-to-expand `<details class="aside">` blocks, a
different thing from the inline parenthetical asides in the Hard rules
above. The rule:

- An aside holds a self-contained mathematical derivation or proof:
  the "why this is true" behind a claim. The claim always stays in the
  main text; only its justification moves into the aside.
- Reaching for one should feel natural. Whenever the math deserves a
  fuller, more rigorous treatment than the narrative itself needs, it
  belongs in an aside, not in the main thread.
- Worked examples that build intuition stay in the main flowing text,
  Quantum Country style. Asides are for proofs and derivations, not
  for the illustrative examples that carry the pedagogy.
- Asides do not count toward the post's target length. The length
  budget (the split threshold above) is measured on the visible
  main-text prose; asides are optional depth layered on top.
- Click-to-expand, not hover (hover fails on touch and cannot hold
  display math).

## Branches

- **`main`:** Quarto site, work-in-progress.
- **`archive/jekyll-site`:** snapshot of the previous Jekyll-based
  site (including the unfinished 1D Symplectic Cellular Automata
  post). Preserved for reference; not used in the current build.
