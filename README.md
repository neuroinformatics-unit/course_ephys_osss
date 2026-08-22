# [OSSS](https://neuroinformatics.dev/open-software-summer-school/index.html) Extracellular Electrophysiology Course

This is the repository for the 2026 Extracellular Electrophysiology 2026 course [website](https://neuroinformatics.dev/course_ephys_osss/), taught at the [Neuroinformatics Unit's Open Software Summer School](https://neuroinformatics.dev/open-software-summer-school/index.html).

To work through the course, see the [set up instructions](https://neuroinformatics.dev/course_ephys_osss/setup.html) to get started.

# Contributing
The website is a Quarto book. GitHub Actions rebuilds it from `main` when changes are merged, and publishes the rendered site to the `gh-pages` branch for GitHub Pages to serve.

First, install [Quarto](https://quarto.org/docs/get-started/).

To preview the website locally, run from the `book` folder:

```
python -m pip install -r requirements.txt
quarto render --to html
```
(requires [Quarto](https://quarto.org/docs/get-started/) to be installed).

This generates the website in `book/_site`. After a PR is merged into `main`, CI rebuilds the site and publishes it to `gh-pages` automatically.

## Releasing a new version

The package version is not set manually: it is derived from git tags via `setuptools-scm` (see `pyproject.toml`). To cut a new release:

```
git tag vX.Y.Z
git push origin vX.Y.Z
```

Pushing the tag triggers the same GitHub Actions workflow, which rebuilds and publishes the site to `gh-pages`, and `setuptools-scm` picks up `vX.Y.Z` as the new package version.

