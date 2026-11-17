# Makefile for Sphinx documentation
#
SITE_PACKAGES_DIR = $(shell python -c "import site; print(site.getsitepackages()[0]);")

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

.PHONY: help html clean

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html        to make standalone HTML files"
	@echo "  clean       to remove the HTML files"

all: html

html:
	@mkdir -p "docs/_tmp"
	@rm -rf $(BUILDDIR)/html/_sphinx_design_static
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	# Sphinx 8 增量构建在「只有 _static 下文件变更」时会跳过整个写出阶段
	# （提示 "no targets are out of date"），静态文件不会同步到输出目录。
	# 这里额外同步一次，保证只改 CSS/JS 等静态资源也能生效。
	@cp -R docs/_static/. $(BUILDDIR)/html/_static/
	@python docs/_static/scripts/custom_secondary_sidebar.py $(BUILDDIR)/html
	@echo
	@echo "Build finished."

clean:
	@rm -rf $(BUILDDIR)/*
	@rm -rf docs/_tmp
	@echo "Clean finished."

format:
	@python formatter.py
	find . -type f \( -name "*.cpp" -o -name "*.c" -o -name "*.cc" -o -name "*.h" -o -name "*.hpp" \) \
	-not -path "./.git/*" \
	-not -path "./.svn/*" \
	-not -path "./.github/*" \
	-not -path "./node_modules/*" \
	-not -path "./doc/_static/*" \
	-not -path "./.venv/*" \
	-not -path "./build/*" \
	-exec $(SITE_PACKAGES_DIR)/clang_format/data/bin/clang-format -i {} +
	npx prettier . --write

resume:
	@mkdir -p "docs/_static/pdf"
	@cd docs/_static/resume && latexmk -pdf cv.tex
	@echo "Build finished."
