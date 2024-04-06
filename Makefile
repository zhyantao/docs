# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = build

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) docs
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) docs

.PHONY: help clean html pdf

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  clean      to clean the whole porject output"
	@echo "  pdf        to generate LaTeX pdf files"

all: pdf html

html:
	@mkdir -p "docs/_tmp"
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

pdf:
	@cd docs/cheatsheet && latexmk -pdf java.tex
	@cd docs/cheatsheet && latexmk -pdf cpp.tex
	@cd docs/cheatsheet && latexmk -pdf c.tex
	@cd docs/resume && latexmk -pdf cv.tex
	@echo "Build finished; the LaTeX files are in docs/_static/cheatsheet."

clean:
	@rm -rf $(BUILDDIR)/*
	@rm -rf docs/_tmp
	@cd docs/cheatsheet && latexmk -c -C java.tex
	@cd docs/cheatsheet && latexmk -c -C cpp.tex
	@cd docs/cheatsheet && latexmk -c -C c.tex
	@cd docs/resume && latexmk -c -C cv.tex
	@echo "Clean finished."
