# Figure 6: the Clifford bouquet

**What it shows.** One static panel. A large, gently irregular convex
blob stands for the full set of unital qubit channels (a
nine-parameter continuum). Through the point $P$ inside it (the
completely depolarizing channel, drawn in the same neutral grey as
the maximally mixed dot in Figures 1, 3 and 5) runs a bouquet of six
thin teal needles: the Clifford channels, one sheet per skeleton
$h$, scale factors varying continuously along each. All needles pass through
$P$ because every skeleton with all scale factors zero is $P$. The identity
channel sits at the tip of the identity-skeleton needle, marked
"id". Needles are longer toward positive scale factors than negative ones
(all scale factors $+1$ is the lawful identity; all scale factors $-1$ is not
completely positive).

**Deliberate idealizations** (both carried by the post's caption):
each sheet is drawn as a 1D needle but is really three-dimensional
(one scale factor per axis), and distinct sheets really intersect in more
than $P$ (once a scale factor is zero, more than one skeleton describes the
same channel).

**Build.**

```
python3 clifford_bouquet_figure.py        # writes clifford-bouquet-d2.svg
```

All geometry (blob centre and wobble, needle angles and lengths,
label offsets) lives as named constants at the top of the script.
`interactive.qmd` is the partial the post includes: a scoped
`{=html}` wrapper with a visually-hidden description and the SVG
inlined verbatim minus the XML prolog. Static on purpose, no
interactive layer: it is a conceptual sketch. After editing the
script, regenerate the SVG and re-splice it into `interactive.qmd`
(everything between the `<div class="clifford-bouquet">` line and the
closing `</div>`).

**Wired in.** `_04-paulis.qmd`, div `#fig-clifford-bouquet`, placed
directly after "Nothing was lost by retreating into the small room."
