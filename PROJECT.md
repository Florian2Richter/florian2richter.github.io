# Blog Post Project: Finite Roots of the Depolarizing Channel

This document is the shared context for writing a technical blog post.
The post is based on unpublished work from my 2010 diploma thesis at
Leibniz Universität Hannover under Prof. R. F. Werner. The thesis is
included in this project as reference material. The full result was
published separately in "How long can it take for a quantum channel to
forget everything?"; what's covered here is a smaller result from
Chapter 5 that didn't make it into the paper because the general
construction in Chapter 6 subsumed it.

## The angle

The result worth telling: Clifford channels — a highly structured,
low-parameter class of quantum channels — can divide the completely
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

- ["Quantum computing for the very curious"](https://quantum.country/qcvc)
  — the main essay, covering qubits, single- and multi-qubit gates.
- ["How quantum teleportation works"](https://quantum.country/teleportation)
  — useful but optional.

## Audience

The reader is comfortable with the basics: matrices, vectors,
eigenvalues, probability distributions. They've worked with these
objects before and aren't fazed by an equation involving them.

What we *briefly introduce* in the post itself:

- **Mixed states.** Density matrices. The Bloch ball as the qubit
  state space. Roughly one short section.
- **Quantum channels (CPTP maps).** Just enough to make the
  depolarizing channel and Clifford channels well-defined. We do not
  develop the full Heisenberg/Schrödinger duality, Stinespring, or
  Kraus theory — we cite them and move on.

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

1. **Hook + classical depolarization.** Stochastic process collapsing
   the simplex to a point. The divisibility question $S^k = P$.
   Classical bound $d - 1$. Concrete: build a square root of the 3D
   bistochastic CDC and visualise its trajectories.

2. **Quantum upgrade.** Density matrices, channels, the Bloch ball
   collapsing to its centre. The bound jumps to $d^2 - 1$ via Jordan.
   State the puzzle: can it actually be achieved?

3. **Clifford channels as the playground.** Weyl operators, projective
   representation structure, Clifford channel definition as
   $T(W(\eta)) = \lambda(\eta) W(h(\eta))$. Two pieces of data.

4. **The reduction.** Concatenation $T^n$ acts on Weyl labels by $h^n$
   and multiplies by a product of $\lambda$'s along the orbit. Channel
   question becomes a question about a linear map on $\mathbb{F}_d^2$.

5. **The two ingredients.**
   - Group order of $h \in GL(2, \mathbb{F}_d)$. Max order $d^2 - 1$
     via companion matrix of a primitive polynomial. Sidebar on why
     primitive polynomials exist (extension fields).
   - Single orbit covers everything. Max-order $h$ acts transitively
     on $\mathbb{F}_d^2 \setminus \{0\}$. With $\lambda$ vanishing on
     a single inverse pair, this gives the bound $\frac{d^2 - 1}{2}$.

6. **Punchline.** The orbit structure on the phase space is where the
   room lives, not the richness of the channel class.

7. **Closing.** Pointer to the published paper for the general
   construction (perturbation of the Jordan block). Note that the
   Clifford story didn't make it in because the general result
   subsumes it — but it's the cleanest place to *see* what's going on.

## Voice and style

Imitate Michael Nielsen's expository voice from Quantum Country.
The hallmarks:

- Short sentences, short paragraphs
- Concrete before abstract — show a specific matrix doing a specific
  thing before naming the category
- Explicit signposting: "Let's work through an example," "Here's the
  surprising thing," "It's worth pausing here"
- Conversational about confusion: "This seems strange. Why should it
  be true?" then answers
- Italics for emphasis, sparingly, on the conceptually-loaded word
- Formulas integrated into prose, not displayed in isolation when
  inline works
- First-person plural for the math journey, first-person singular
  sparingly for personal asides ("I find this surprising because...")

Avoid thesis-prose patterns: "Furthermore," "We observe that," "In
what follows," "It turns out that" used as crutch. If we catch
ourselves writing in that register, rewrite.

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

- `posts/clifford-roots/index.qmd` — this post
- `posts/clifford-roots/figures/` — Python scripts and generated SVGs
- `reference/Diplomarbeit_Florian.pdf` — the thesis (gitignored)
- `_quarto.yml` — site config
- `.github/workflows/publish.yml` — deployment

**Open infrastructure question:** the existing
`florian2richter.github.io` repo may have content from an earlier
unfinished project. First task is to inspect it and decide whether
to add to it, archive it, or start fresh.

## Open questions / things to decide later

- **Length target.** Current aim: 3500-4500 words. May need a split
  into two posts if it grows past 5000.
- **Whether to include code snippets.** Maybe a small Python block
  showing the matrix multiplication $T \cdot T = P$ for the
  3×3 case, for hands-on readers. Quarto can execute these live at
  build time.
- **Title.** "How finely can you divide a depolarizing channel?" is
  the working title but not locked in.
- **A possible sidebar on the sampling-the-simplex question** (uniform
  sampling on the simplex, why naive normalisation fails). It's a
  nice mathematical aside that fits the post's spirit but adds length.
- **Integration with existing `florian2richter.github.io` content.**
  Add to it, archive and replace, or co-exist?

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
