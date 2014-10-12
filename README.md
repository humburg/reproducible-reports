# Creating reproducible reports with knitr and pandoc

These are some examples on how to use Markdown with R and pandoc to create
dynamic documents for multiple output formats. All examples and accompanying text
are contained in example.Rmd.

## Compiling the document
Creating PDF and HTML output from the R/Markdown source file is a two step process.
First `knitr` is used to execute the R code and produce the corresponding Markdown
output. This can be done either by starting an R session and executing 
`knitr("example.Rmd")` or from the command line:

```
Rscript --slave -e "library(knitr);knitr('example.Rmd')" 
```
Either way this generates a Markdown file called 'example.md'. This can then be
converted into PDF and HTML files by using the configuration file 'example.pandoc'
by calling the pandoc function from the `knitr` package.

```
Rscript --slave -e "library(knitr);pandoc('example.md')"
```
The function automatically locates the configuration file and passes the requested
parameters to `pandoc`.

## Required software
In addition to installations of `knitr` and `pandoc` a few external tools 
are required to compile this document. 

[R](http://r-project.org/) is required to run `knitr` as well as other R packages
to support additional functionality.

Additional R packages used:

* [animation](http://cran.r-project.org/web/packages/animation/index.html)
  (for animated figures)
* [pander](http://cran.r-project.org/web/packages/pander/index.html) (for Markdown
  formatting of R objects)

These can be installed via the `install.packages` command from within R.
Animations also require [ffmpeg](https://www.ffmpeg.org/).

As one might expect a working LaTeX tool chain is required to generate
PDF output from LaTeX documents. Several distributions are available
online, including [MiKTeX](http://miktex.org/) and [TeX Live](https://www.tug.org/texlive/). 

[Python](https://www.python.org/) (>= 2.7) is required for `pandoc` the 
filters discussed in the latter parts of this document.
