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
`posts/clifford-roots/figures/` for the convention).

## Audience and voice

The Clifford post is written for **an undergraduate in physics, math,
or engineering**, not a colleague reading in one sitting. That is the
"very curious" reader Quantum Country addresses: comfortable with
linear algebra and probability, but meeting quantum channels, Weyl
operators, and finite fields here for the first time. Pedagogy wins
over brevity; length is a result, not a target, and the depth and
worked-example density of Quantum Country is the model to aim for. A
two-post split at the reduction (section 5) is on the table only if
the single post grows well past about 12000 to 15000 words.

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

Avoid thesis-prose crutches: "Furthermore," "We observe that," "In
what follows," "It turns out that." If a paragraph starts reading like
a textbook chapter, rewrite it.

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

## Structural plan for the Clifford post

The plan below is the original arc; it is now realized in six
partials included by `index.qmd`: `_01-hook` (1), `_02-classical-setup`
(2), `_03-quantum-upgrade` (3), `_04-paulis` "Rebuilding the qubit
from the bit" (4, 5, 6 at the qubit level, restructured bottom-up:
$\mathbb{Z}_2 \to \mathbb{Z}_2^2$, the forced phase, the Clifford
family at $d = 2$, the design-first root), `_05-clifford-higher-dimensions`
(4 through 9 at general prime $d$), `_06-whats-next` (10).

1. **Hook.** Photocopy-of-a-photocopy framing. No math.
2. **The classical setup.** Simplex, stochastic matrices, the
   bistochastic CDC, divisibility, the $d - 1$ bound, $d = 3$ worked
   example.
3. **The quantum upgrade.** Density matrices, channels, the maximally
   mixed state. Bound jumps to $d^2 - 1$. The section is self-contained
   at the "shape" level (no bra-ket algebra), so the Quantum Country
   recommendation is a footnote on the first qubit, not a gating
   prerequisite at the top. Ends on the honest caveat: the bound comes
   from a Jordan block, but whether it is completely positive was unclear
   (first person), which motivates the Clifford restriction.
4. **Coordinates for the Paulis (interlude).** Hands-on: the Pauli group
   (16 elements + multiplication table), the addresses $(a,b)$,
   multiplying = adding mod $d$, the trailing phase that makes it a
   *projective* representation, Weyl operators / $\mathbb{F}_d^2$, why $d$
   prime (aside). The trailing phase is the seam that becomes $\lambda$.
5. **Clifford channels as the playground.** The "axes to axes" geometric
   restriction, CP/Choi tractability, and the channel as two pieces of
   data, $T[\mathbf{w}(\eta)] = \lambda(\eta)\,\mathbf{w}(h(\eta))$:
   relabelling $h$ + amplitude/phase $\lambda$.
6. **The reduction (pivot).** $T^n$ acts on Weyl labels by $h^n$ with
   a product of $\lambda$'s along the orbit. The channel question
   becomes a question about a linear map on $\mathbb{F}_d^2$.
7. **Ingredient 1: the order of $h$.** Max order $d^2 - 1$ via
   companion matrix of a primitive polynomial. Finite-field sidebar
   at moment of need.
8. **Ingredient 2: orbits and where $\lambda$ vanishes.** Transitive
   action on $\mathbb{F}_d^2 \setminus \{0\}$, $\lambda$ vanishing on
   one inverse pair, bound $\frac{d^2 - 1}{2}$.
9. **Punchline.** The room lives in the orbit structure of $h$, not
   in channel richness.
10. **What's next.** Pointer to the published paper for the general
   $d^2 - 1$ construction.

## Current state

- **Prose complete: all six partials.** Full first draft end to end,
  awaiting Florian's revision pass. `_04` rebuilds the qubit bottom-up
  and ends with the CP resolution as a coin flip among three
  rotations; `_05` delivers the $(d^2-1)/2$ theorem self-contained:
  the $\tau$-groomed Weyl operators, the mirror rule, the
  companion-matrix grand cycle, antipodal mirror-pair zeros, an
  $\varepsilon$/Choi legality aside, and a two-case proof that no
  Clifford channel beats one half. `_06` closes the memory-device
  loop from the hook.
- **Inline expandable asides** (`<details class="aside">`, styled in
  `styles.css`): claim in the text, derivation one click away.
  `_04` has two (the forced-phase proof, the three-rotation
  decomposition); `_05` has five (the Weyl basis, the mirror rule,
  primitive polynomials / cyclicity, the CP criterion with the
  Gershgorin loudness budget $\sum_{\eta\neq 0}|\lambda(\eta)| \le 1$,
  why nothing beats one half). Click-to-expand, not hover.
- **Figures: all built and wired.** fig1 (classical simplex,
  interactive), fig2 (classical square root, animated), fig3 (Bloch
  ball, interactive), fig3b (qubit root collapsing a Bloch cloud in
  stages z->y->x->0, animated), fig5 (continuum vs. finite label
  grid, static, in `_04`; its example $h$ is exactly the root's
  3-cycle), fig4 (the $d=3$ orbit ring with the antipodal vanishing
  pair, static, in `_05`). See `figures/README.md` for ids and the
  progressive-enhancement conventions.
- **Citation TODOs (the remaining work):** the mixing-channels
  footnote in the hook (candidates listed inline, need verifying),
  and the published paper for the general $d^2-1$ construction,
  described but not yet cited in `_06`. The thesis is now cited in
  full in `_06` (F. Richter, *Finite Roots of Completely
  Depolarizing Channels*, Diploma thesis, Hannover 2010); a public
  PDF link is still to be added. `_04` and `_05` footnotes point at
  its chapter 5 (Lemma 5.1, §§5.2.1, 5.4.1). The channels footnote
  in `_03` (Nielsen & Chuang ch. 8, Wolf notes) is real.
- **Worked example thread:** $d=3$ (qutrit) runs through `_05`.
  Primitive polynomial $x^2+x+2$, $g^2 = 2g+1$, $g^4 = -1$, companion
  matrix $h=\binom{0\ 1}{1\ 2}$, the explicit 8-cycle, mirror-pair
  zeros at $(1,0)/(2,0)$, root of order 4. The three bounds for
  $d=3$, stated at the end of `_05`: 2 / 4 / 8.
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
