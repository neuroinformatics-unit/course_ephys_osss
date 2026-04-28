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

# Style

Some things I have included, we can discuss if they are useful and worth including them across all chapters:
- During the course we will walk them through the key code sections. Then after each natural section, we
can have a 'things to try' box. We'll give them some time to play around and try these things out on their own.
- 'Concept Notes' is a page that contains expanded definitions / explanations of concepts. For example in the introduction
chapter, we mention data streams, or the fact data is stored in int16 unitless. It's a bit much to go into it in the middle
of the chapter, but can link to a longer explanation. We link internally including a little 💡 by the link.

Currently this is the default quarto book style, maybe we can jazz it up as we go along.


