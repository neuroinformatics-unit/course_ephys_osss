# OSSS Extracellular Ephys 2026 Course

The [website](https://neuroinformatics.dev/course-ephys-osss/) of the 2026 OSSS course. Currently in development, includes the [working plan](https://neuroinformatics.dev/course-ephys-osss/planning.html).

# Contributing to the book
The website is a quarto book. It is published directly from the `docs` folder on the repo by GitHub pages.

To build the website, run from the `book` folder:

```
quarto render --to html
```
(requires [Quarto](https://quarto.org/docs/get-started/) to be installed).

This will generate the website in the `docs` folder (and when on `main`, it will be the website).

The easiest way to contribute chapters will be to make a new branch and open a PR to add a new chapter
(I have been pushing to main, but will stop now).

To add a  new chapter it should be sufficient to create the `qmd` file in the root and add the file to
the `index.qmd`.




