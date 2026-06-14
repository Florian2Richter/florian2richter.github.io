# Blog Post Project: Finite Roots of the Depolarizing Channel

> **Status: frozen brief.** This is the original project brief, kept
> for the result, the angle, and the source material. For how to work,
> voice, the post's structure, hard rules, and current state, see
> `CLAUDE.md`, which is authoritative and kept current. Where the two
> overlap, `CLAUDE.md` wins.

This document is the shared context for writing a technical blog post.
The post is based on unpublished work from my 2010 diploma thesis at
Leibniz Universität Hannover under Prof. R. F. Werner. The thesis is
included in this project as reference material. The full result was
published separately in "How long can it take for a quantum channel to
forget everything?"; what's covered here is a smaller result from
Chapter 5 that didn't make it into the paper because the general
construction in Chapter 6 subsumed it.

## The angle

The result worth telling: Clifford channels, a highly structured,
low-parameter class of quantum channels, can divide the completely
depolarizing channel into as many discrete steps as the *general*
quantum machinery allows (asymptotically). The Clifford bound is
$\frac{d^2-1}{2}$; the general bound is $d^2 - 1$. So the toy model
already saturates the general bound up to a factor of 2.

This is surprising because Clifford channels are parametrised by very
little data (a homomorphism $h \in GL(2, \mathbb{F}_d)$ and a function
$\lambda: \mathbb{F}_d^2 \to \mathbb{C}$), while general channels have
the full Choi-matrix freedom. The "room" in the divisibility problem
turns out to live in the orbit structure of $h$ on the phase space
$\mathbb{F}_d^2$, not in the richness of the channel class.

The post sells this as a pedagogical playground: **Clifford channels
are the cleanest place to see how finite-field representation theory
shows up in quantum information**, and the depolarizing-root problem
is the cleanest toy example for that pedagogy.

## Prerequisite reading

The post links to Andy Matuschak and Michael Nielsen's
[Quantum Country](https://quantum.country/) as the recommended primer
for readers who need qubits, gates, and circuits before starting.
Specifically:

- ["Quantum computing for the very curious"](https://quantum.country/qcvc):
  the main essay, covering qubits, single- and multi-qubit gates.
- ["How quantum teleportation works"](https://quantum.country/teleportation):
  useful but optional.

## Audience

The reader is an undergraduate in physics, math, or engineering: the
"very curious" reader Quantum Country addresses. They are comfortable
with the basics, matrices, vectors, eigenvalues, probability
distributions, having worked with these objects before, and aren't
fazed by an equation involving them. They are not yet specialists:
quantum channels, Weyl operators, and finite fields are new to them.

What we *briefly introduce* in the post itself:

- **Mixed states.** Density matrices. The Bloch ball as the qubit
  state space. Roughly one short section.
- **Quantum channels (CPTP maps).** Just enough to make the
  depolarizing channel and Clifford channels well-defined. We do not
  develop the full Heisenberg/Schrödinger duality, Stinespring, or
  Kraus theory; we cite them and move on.

Anyone who has done Quantum Country and has standard mathematical
fluency can read this post.

What we do NOT assume:

- Detailed knowledge of finite fields, Galois theory, or
  representation theory
- Familiarity with Clifford channels, Weyl operators, or the
  Heisenberg picture
- Prior exposure to the divisibility literature on quantum channels

## Structure of the post

Working title: **How finely can you divide a depolarizing channel?**

The early seven-point sketch that once lived here is superseded. See
the **"Structural plan for the Clifford post"** in `CLAUDE.md` for the
authoritative section-by-section outline (nine sections, matching the
actual draft), and its **"Current state"** for what is drafted.

## Voice and style

See the **"Audience and voice"** section of `CLAUDE.md`, which is
authoritative. In short: imitate Matuschak and Nielsen's expository
voice from Quantum Country, and avoid thesis-prose crutches.

## Technical setup

The blog lives at <https://florian2richter.github.io/>. The
infrastructure is:

- A single GitHub repository named `florian2richter.github.io`
  (the repo name must match the user's GitHub username plus
  `.github.io` for personal sites).
- The site is built with **Quarto** (https://quarto.org), a static
  site generator with first-class support for math, code, and
  technical content.
- Quarto outputs to a `docs/` folder, which GitHub Pages serves at
  the root URL. A GitHub Actions workflow runs `quarto render` on
  pushes to main.
- Math rendering is MathJax via Quarto's default.
- SVGs are embedded with standard markdown `![Caption.](path.svg)`
  syntax.

Key paths once scaffolded:

- `posts/clifford-roots/index.qmd`, this post
- `posts/clifford-roots/figures/`, Python scripts and generated SVGs
- `reference/Diplomarbeit_Florian.pdf`, the thesis (gitignored)
- `_quarto.yml`, site config
- `.github/workflows/publish.yml`, deployment

## Open questions / things to decide later

- **Length target.** Governed by `CLAUDE.md` (split into two posts if
  the single post grows past about 7000 words).
- **Whether to include code snippets.** Maybe a small Python block
  showing the matrix multiplication $T \cdot T = P$ for the
  3×3 case, for hands-on readers. Quarto can execute these live at
  build time.
- **Title.** "How finely can you divide a depolarizing channel?" is
  the working title but not locked in.
- **A possible sidebar on the sampling-the-simplex question** (uniform
  sampling on the simplex, why naive normalisation fails). It's a
  nice mathematical aside that fits the post's spirit but adds length.

## What NOT to do

- Don't lose the Nielsen voice. If a section starts to read like a
  textbook chapter, rewrite it.
- Don't pad. Every paragraph should earn its place. A 3500-word
  Nielsen-style post is much denser than a 3500-word thesis chapter.
- Don't lecture about finite fields or representation theory in the
  main thread. Sidebars are fine; main thread stays focused on the
  channel-divisibility narrative.
- Don't claim things that aren't in the thesis or aren't immediately
  verifiable. If something is "well-known" but tricky to state
  precisely, either state it precisely or replace with what *is*
  precisely known.
- Don't include the full Chapter 6 perturbation construction in the
  post. That's the punchline of the *paper*, not this post. Mention
  it and link to the paper.
