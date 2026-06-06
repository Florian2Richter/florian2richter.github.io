# Handoff: clifford-roots blog post

Status report for a fresh context window. Read this plus `CLAUDE.md`
(repo root) and you have everything. Last updated end of the
blue-grey-palette + amber-sampled-state work.

## What this is

A Quarto blog at <https://florian2richter.github.io>. The one in-flight
piece is a long technical post:

- **File:** `posts/clifford-roots/index.qmd`
- **Title:** "How finely can you divide a depolarizing channel?"
- **Result (from Florian's 2010 diploma thesis, ch. 5):** Clifford
  channels can split the completely depolarising channel into nearly as
  many discrete steps as the full quantum machinery allows. The three
  bounds: classical `d-1`, quantum `d^2-1`, Clifford `(d^2-1)/2`. For a
  qutrit: 2 / 8 / 4. The qubit (`d=2`) is special: Clifford already
  reaches the full bound 3.
- **Live (direct link only):**
  <https://florian2richter.github.io/posts/clifford-roots/>

## Audience and voice (hard constraints)

- Audience: a stranger from Hacker News learning the math from scratch.
  Pedagogy over brevity.
- Voice: Matuschak & Nielsen's Quantum Country. Short sentences,
  concrete before abstract, "we" for the math, story-first section
  openings.
- **NO EM-DASHES, ever, in prose.** Use commas, colons, parens, or split
  sentences. (The `—` used as a UI placeholder inside figure readouts is
  fine; that is not prose.)
- No callout boxes. Heavier derivations go in collapsible
  `<details class="aside">` blocks ("unfoldables").

## Post state: fully drafted

All nine sections are written (hook, classical setup, quantum upgrade,
Clifford channels, the reduction/pivot, ingredient 1 = order of `h`,
ingredient 2 = where `lambda` vanishes, punchline, what's next).

Math review applied: the nilpotent-Jordan-block argument (with the
explicit `(d-1)x(d-1)` block) for the classical bound; Hermiticity vs
complete positivity separated (the mirror-pair symmetry
`lambda(-eta)=conj(lambda(eta))` comes from Hermiticity, which is weaker
than CP); an honest caveat about the existence of a CP `lambda`; and the
`d=2` case reframed as "Clifford already saturates the full bound."

Collapsible asides exist for: linearity, the row-sum computation, the
`d^2-1` parameter count, the explicit Weyl operators / why `d` is prime,
primitive polynomials, the `lambda(-eta)` derivation, and the
Jordan-block argument.

## Figures

Everything lives under `posts/clifford-roots/figures/`, **one folder per
figure**, decoupled from the post. The post only `{{< include >}}`s a
finished figure inside a `::: {#fig-...}` div, and every figure is
cross-referenced from the prose with `@fig-...`. Read
`posts/clifford-roots/figures/README.md` for the system.

| # | id | folder | state |
|---|----|--------|-------|
| 1 | `fig-simplex-d3` | `fig1-state-space` | **done, static** (interaction moved to Fig 2) |
| 2 | `fig-root-d3` | `fig2-simplex-root` | **done, interactive** |
| 3 | `fig-bloch` | `fig3-bloch-ball` | **done, static** (interaction moved to Fig 4) |
| 4 | `fig-bloch-root` | `fig3b-bloch-root` | **done, interactive** (click-to-trace qubit root orbits to I/2) |
| 5 | `fig-orbit` | `fig4-orbit-cycle` | **PLANNED** (broken-image placeholder; README sketches it) |

Figure numbers are auto-assigned by order of appearance, so the orbit
cycle is now Figure 5. Figure 4 (`fig-bloch-root`) sits in "The quantum
upgrade" section, right after Figure 3.

The two chapters now run in parallel: the **state space is a static
sketch** (Fig 1 simplex, Fig 3 Bloch ball) and the **root trajectories
are interactive** (Fig 2 simplex, Fig 4 Bloch ball). The maximally mixed
state is a solid marker in the flat 2D figures (1, 2) and a recessed,
depth-cued grey marker in the two 3D Bloch balls (3, 4), hinting that it
sits inside the sphere. Fig 4's root is the maximal qubit root from the
thesis (eq. 4.19), acting on the Bloch vector as
`(r1,r2,r3) -> (r2/2, r3/2, 0)` (`S^3 = 0`, a cube root of the CDC); the
interactive layer adds a Purity slider that recomputes the orbit live for
mixed-state starts.

Each done folder has: a Python generator (`*_figure.py`), the generated
`*.svg`, the `interactive.qmd` partial the post includes, and a
`README.md`. **The `interactive.qmd` is the source of truth for the
interactive layer** (it inlines the SVG verbatim plus a scoped `<style>`,
a readout, and a `<script>`). Progressive enhancement: JS off => the
unaltered static SVG.

### Colour scheme (blue-grey "scientific" palette, purity-encoded)

The background **field encodes purity**: blue-teal `PURE #2d6f8f` (pure)
fading to soft blue-grey `MIXED #d6e5ea` (maximally mixed, a tinted
centre, never white). Structure: axes/labels `AXIS #233746`, grid lines
`GRID #829aa6`, centre marker a light `CENTER #f5f7f8` ring with a
visible outline. The **interactive sampled state** the reader places (and
every moving object) is a **strong blue `STATE #1565c0`** (dark-blue
`#0d3f8f` stroke); in Figure 2 the whole user trajectory is this blue and
the placed point is a square.

To retune colours: edit `PURE_RGB` / `MIXED_RGB` in the generators (and
the Bloch radial-gradient stops in `bloch_ball_figure.py`), then mirror
the same hex in the `purityColour` helper inside each `interactive.qmd`.
Figure 4 is the label plane `F_d^2`, not a state space, so purity does
NOT apply there.

### Editing a figure (important workflow)

The post uses the **inlined** SVG inside `interactive.qmd`, not the
`.svg` file. So after changing a generator: rerun it to regenerate the
`.svg`, then re-copy the new `<svg>...</svg>` body into `interactive.qmd`
(replacing the old inline SVG). The `<script>` re-reads geometry from the
SVG, so it needs no edits for pure geometry changes (colour changes need
mirroring in `purityColour`).

### Verifying figures visually (headless)

SVG -> PNG with inkscape, then read the PNG. Snap inkscape needs
**absolute paths inside `$HOME`** (it cannot read `/tmp`):

```bash
cd posts/clifford-roots/figures/fig1-state-space
python3 state_space_figure.py state_space.svg
inkscape "$(pwd)/state_space.svg" --export-type=png \
  --export-filename="$(pwd)/_preview.png" -w 720
# read _preview.png, then: rm _preview.png   (do not commit previews)
```

Validate interactive JS with `node --check` after extracting the
`<script>` block.

## Infrastructure and deploy

- Quarto site. `_quarto.yml`: `html-math-method: katex`,
  `draft-mode: unlinked`, explicit `render:` list. Local renders go to
  `docs/` (gitignored).
- The post has `draft: true`. With `draft-mode: unlinked` it renders in
  full at its direct URL but stays out of the blog index, feed, sitemap,
  and search. **Flip to `draft: false` to publish it to the index.**
- **Deploy:** push to `main` => the `.github/workflows/publish.yml`
  Action renders and publishes to the **`gh-pages`** branch, which
  GitHub Pages serves. This is fully automatic now. (One-time setup is
  already done: the `gh-pages` branch was created and the Pages source
  was repointed from `main` to `gh-pages`.)
- After a push, Pages takes a couple of minutes; hard-refresh.

### Polling CI / reading Actions logs

A GitHub PAT is saved at `~/tokens/git.token` (scopes `repo` +
`workflow`). Used to poll the deploy and read CI logs without `gh` (not
installed). Example:

```bash
TOKEN=$(cat ~/tokens/git.token)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/Florian2Richter/florian2richter.github.io/actions/runs?per_page=3" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);[print(r['status'],r['conclusion'],r['head_sha'][:7]) for r in d['workflow_runs']]"
```

**Revoke this token when the project wraps** (github.com/settings/tokens).

## Gotchas (learned the hard way)

- **Do NOT run `quarto render` while `quarto preview` is live.** They
  fight over the `.quarto` cache and wedge the preview's file watcher;
  it shows up as "missing chapters" (stale page). Let the preview do the
  rendering, or kill it first. The preview's child is a `deno` process;
  find it with `ss -ltnp | grep <port>` and `kill -9` the pid.
- The `*.html` `.gitignore` rule will silently skip any `.html` you add
  on purpose; `git add -f` if needed (currently nothing needs this).
- When re-assembling a figure partial by regex, beware: a partial's lead
  comment can contain literal `<style>`/`<script>` text. Strip the lead
  comment before extracting.

## Open TODOs

1. **Figure 5 (orbit cycle).** Not built (folder `fig4-orbit-cycle`,
   id `fig-orbit`; it renders as Figure 5 now). See
   `figures/fig4-orbit-cycle/README.md`: the `d=3` orbit of
   `h = [[0,1],[1,2]]` over `F_3` (companion of `x^2+x+2`), the 8-cycle
   `(1,0)->(0,1)->(1,2)->(2,2)->(2,0)->(0,2)->(2,1)->(1,1)->(1,0)`, with
   the mirror-pair zeros `(1,0)`/`(2,0)` at the poles. Model the build on
   `fig2`. Own colour scheme (not purity).
2. **Citations.** Hook "mixing channels" footnote (TODO); the `§9`
   general-construction paper (working title only); confirm the exact
   thesis title (the `§9` footnote currently guesses "Roots of the
   completely depolarising channel"). The thesis PDF is at
   `reference/Diplomarbeit_Florian.pdf` (use `pdftotext`).
3. **Colour fine-tuning.** Florian said "we adjust the colouring later."
   Retune as above. He also wants the centre to never be pure white
   (already handled, but tune to taste).
4. **Publish.** Flip `draft: true` -> `false` when ready to list it.
5. Minor: `fig1` `interactive.qmd` has a now-unused `.si-fill` CSS rule
   (the p1/p2/p3 bars were removed; readout shows only the vector).
   Harmless.

## How to start next

```bash
cd /home/florian/repos/florian2richter.github.io
quarto render posts/clifford-roots/index.qmd   # one-shot build to docs/
# or: quarto preview   (hot reload; do NOT also run render)
```

1. Read `CLAUDE.md` and this file.
2. Skim `posts/clifford-roots/index.qmd` and the live page.
3. Pick a TODO. The biggest remaining piece of work is Figure 4.
4. Commit + push to `main` to deploy; poll the Action with the token.

Note: the auto-memory at `~/.claude/projects/.../memory/` is
machine-local (won't travel to another machine). The portable handoff is
this file + `CLAUDE.md`, both in the repo.
