# florian2richter.github.io

Source for [florian2richter.github.io](https://florian2richter.github.io),
built with [Quarto](https://quarto.org).

## Local preview

```bash
quarto preview
```

## Build

```bash
quarto render
```

Output goes to `docs/`. The GitHub Actions workflow in
`.github/workflows/publish.yml` renders and deploys on every push to `main`.

## Project layout

- `_quarto.yml` — site config
- `index.qmd` — blog listing
- `about.qmd` — about page
- `posts/<slug>/index.qmd` — individual posts
- `posts/<slug>/figures/` — post-specific figures and (when applicable)
  scripts that generate them
- `reference/` — source PDFs and reference material (gitignored)
