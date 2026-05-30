# How to contribute to this website

## Website structure
This repository is a Quarto book. Source files live in `book/`, and the rendered site is written to the tracked `docs/` directory.

## Adding new content
To add a new chapter, create a `.qmd` file in `book/` and add it to the chapter list in `book/_quarto.yml`.

To update an existing chapter, edit the relevant `.qmd` file in `book/`.

## GitHub workflow
* Clone the repository and create your feature branch.
* Edit the book sources in `book/` and commit your changes to that branch.
* Rebuild the book locally from `book/` with `quarto render --to html` and review the affected pages in `docs/`.
* Push the branch and open a pull request. GitHub Actions will render the book to verify that the site still builds.
* If the checks pass, request review.
* After the pull request is merged into `main`, GitHub Actions will render the book again and commit the refreshed `docs/` output automatically.

## Local preview
If you want to review the site locally before opening or updating a pull request, run the following command from `book/`:

```bash
quarto render --to html
```

This writes the rendered site to `docs/`. Open `docs/index.html` in a browser to inspect the result.
