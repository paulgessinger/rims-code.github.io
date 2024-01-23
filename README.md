# RIMS Code website generator

This repo serves the RIMS-Code website,
hosted at
https://rims-code.github.io.

The website is based on [`mkdocs`](https://www.mkdocs.org/)
and uses the [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/) theme.

The `docs` folder contains all website files.
Note that the `schemes` folder in `docs` is automatically generated
by the python package that is also hosted in this repo.

## RIMS schemes database

The database for RIMS schemes is hosted in the `schemes` folder.
It is a collection of `.json` files, one for each scheme.

When a pull request is created,
the `schemes` folder is automatically read and
the website with the updated scheme is created.

Upon successful merge, 
the website is automatically deployed.

**Note**: For the python package to be able to read the schemes,
the folder structure of the whole repo must be preserved.
