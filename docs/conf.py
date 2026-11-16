# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import os


# -- Project information -----------------------------------------------------

project = "Notebook"
copyright = "2026"
author = "Yantao Zhang (yantao.z [at] outlook.com)"
master_doc = "index"
language = "en"
source_encoding = "utf-8-sig"
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}


# -- Options for HTML output -------------------------------------------------

html_title = "Notebook"
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_css_files = ["css/tufte.css"]
html_js_files = ["js/auto-toggle-sidebar.js", "js/site-nav.js"]
html_favicon = "_static/images/logo_square.svg"
html_last_updated_fmt = ""
html_domain_indices = True
html_use_index = True
html_split_index = False
html_show_sourcelink = True
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/zhyantao/getstarted",
    "repository_branch": "master",
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "colab_url": "https://colab.research.google.com/",
        "deepnote_url": "https://deepnote.com/",
        "notebook_interface": "jupyterlab",
        # "thebe": True,  # removed: thebe fetches its kernel from a CDN/cloud service
        # "jupyterhub_url": "https://datahub.berkeley.edu",  # For testing
    },
    "use_edit_page_button": True,
    "use_source_button": True,
    "use_issues_button": True,
    # "use_repository_button": True,
    "use_download_button": True,
    "use_sidenotes": True,
    "show_toc_level": 2,
    # 页脚：去掉默认的 author/copyright 条目，改成与其他页面一致的
    # 联系方式 + 署名风格（icon 链接 + credits 行）
    "footer_content_items": "last-updated.html, extra-footer.html",
    "extra_footer": """
<div class="footer-links">
  <a href="mailto:yantao.z@outlook.com" aria-label="Email"><i class="fa-solid fa-envelope"></i></a>
  <a href="https://github.com/zhyantao" aria-label="GitHub"><i class="fa-brands fa-github"></i></a>
</div>
<p class="credits">© 2026 YANTAO ZHANG &nbsp;·&nbsp; Powered by <a href="https://www.sphinx-doc.org/">Sphinx</a></p>
""",
    # "announcement": (
    #     "WHEN YOU PRAY, MOVE YOUR FEET!"
    # ),
    "icon_links": [
        # {
        #     "name": "Documentation Status",
        #     "url": "https://readthedocs.org/projects/getstarted/builds",
        #     "icon": "_static/images/badges/rtd.svg",
        #     "type": "local",
        # },
        # {
        #     "name": "GitHub Release",
        #     "url": "https://github.com/zhyantao/getstarted/releases",
        #     "icon": "_static/images/badges/release.svg",
        #     "type": "local",
        # },
        # {
        #     "name": "Curriculum Vitae",
        #     "url": "https://zhyantao.github.io/cv/",
        #     "icon": "https://img.shields.io/badge/cv-ongoing-blue",
        #     "type": "url",
        # },
    ],
}


# -- General configuration ------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "default"

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("_exts"))

# Add any Sphinx extension module names here
# WARNING: Do not modify the order unless you know what will happen!!!
extensions = [
    "chinese_search",
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.mermaid",
    "sphinx_last_updated_by_git",
    "sphinxcontrib.plantuml",
]


# -- Options for Extensions -------------------------------------------------

# Setting for sphinx.ext.autosummary to auto-generate single html pages
# Please makesure all api pages are stored in `/reference/api/` directory
# See `Makefile` for more detail.
autosummary_generate = True

# Setting for sphinx.ext.auotdoc
autodoc_default_options = {"member-order": "bysource"}
autoclass_content = "class"
autodoc_docstring_signature = True
autodoc_preserve_defaults = True
autodoc_mock_imports = ["mprop"]

# Setting for sphinx.ext.mathjax
# The path to the JavaScript file to include in the HTML files in order to load MathJax.
# Use the vendored SVG build (docs/_static/vendor/mathjax/) so that no fonts or
# scripts are fetched from a CDN at runtime.
mathjax_path = "vendor/mathjax/tex-mml-svg.js"

# Setting for sphinxcontrib-mermaid
# Vendor the mermaid ESM bundle at docs/_static/vendor/mermaid/ (built with
# esbuild from mermaid@11.12.2) so that nothing is fetched from a CDN at
# runtime; `mermaid_use_local` paths are resolved relative to html_static_path
# and takes precedence over `mermaid_version`.
mermaid_version = "11.12.2"
mermaid_use_local = "vendor/mermaid/mermaid.esm.min.mjs"

# Setting for sphinx.ext.extlinks
# Can use the alias name as a new role, e.g. :issue:`123`
extlinks = {
    "src": ("https://github.com/zhyantao/getstarted/blob/master/%s", "%s"),
    "docs": ("https://github.com/zhyantao/getstarted/blob/master/%s", "%s"),
    "issue": ("https://github.com/zhyantao/getstarted/issues/%s", "Issue #%s"),
    "pull": ("https://github.com/zhyantao/getstarted/pull/%s", "Pull Requset #%s"),
    "duref": (
        "http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#%s",
        "%s",
    ),
}

# Setting for sphinx_autodoc_typehints
typehints_fully_qualified = False

# Setting for sphinx_copybutton
copybutton_prompt_text = (
    r">>> |\.\.\. |(?:\(.*\) )?\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True

# Setting for sphinx_panels
panels_add_bootstrap_css = True

# Setting for myst_nb
suppress_warnings = ["myst.domains"]
numfig = True
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "tasklist",
]
panels_add_bootstrap_css = False

nb_custom_formats = {".Rmd": ["jupytext.reads", {"fmt": "Rmd"}]}

# Setting for sphinxcontrib.bibtex
bibtex_bibfiles = ["references.bib"]

myst_footnote_transition = False

# Setting for sphinx-last-updated-by-git
git_last_updated_timezone = "Asia/Shanghai"

# Setting for PlantUML
CURRENT_DIR = os.path.abspath(".")
# -Dapple.awt.UIElement=true: macOS 上不让每个 JVM 进程在 Dock 中闪现图标（Linux 上无副作用）
plantuml = (
    f"java -Dapple.awt.UIElement=true "
    f"-jar {CURRENT_DIR}/_static/plantuml/plantuml-1.2024.6.jar"
)
plantuml_output_format = "svg"
# 所有图合并为一次 JVM 调用，避免每张图都启动一次 java（图标闪烁）
plantuml_batch_size = 100
