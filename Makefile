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

.PHONY: help html pdf clean-html clean-pdf

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html        to make standalone HTML files"
	@echo "  pdf         to make LaTeX files and run them through pdflatex"
	@echo "  clean-html  to remove the HTML files"
	@echo "  clean-pdf   to remove the LaTeX files"

all: pdf html

html:
	@mkdir -p "docs/_tmp"
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished."

pdf:
	@mkdir -p "docs/_static/resume"
	@cd docs/resume && latexmk -pdf cv.tex
	@echo "Build finished."

clean-html:
	@rm -rf $(BUILDDIR)/*
	@rm -rf docs/_tmp
	@echo "Clean finished."

clean-pdf:
	@cd docs/resume && latexmk -c -C cv.tex
	@echo "Clean finished."
