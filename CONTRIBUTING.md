# How to contribute to this website

## Website structure
This repository is a Quarto book. Source files live in `book/`, and GitHub Actions publishes the rendered site to the `gh-pages` branch.

## Adding new content
To add a new chapter, create a `.qmd` file in `book/` and add it to the chapter list in `book/_quarto.yml`.

To update an existing chapter, edit the relevant `.qmd` file in `book/`.

## GitHub workflow
* Clone the repository and create your feature branch.
* Edit the book sources in `book/` and commit your changes to that branch.
* Rebuild the book locally from `book/` with `quarto render --to html` and review the affected pages in `book/_site/`.
* Push the branch and open a pull request.
* Request review once you have checked the rendered output locally.
* After the pull request is merged into `main`, GitHub Actions will render the book and publish the refreshed site to `gh-pages` automatically.

## Local preview
If you want to review the site locally before opening or updating a pull request, run the following command from `book/`:

```bash
quarto render --to html
```

This writes the rendered site to `book/_site/`. Open `book/_site/index.html` in a browser to inspect the result.
