"""Skip mermaid client-side assets on pages that contain no mermaid diagrams.

sphinxcontrib-mermaid already skips pages whose doctree has no ``mermaid``
node, but for generated pages (search, genindex, ...) the doctree is ``None``
and the ~2.6 MB vendored ESM bundle is still emitted.  This handler must run
*after* sphinxcontrib-mermaid's own ``html-page-context`` handler, so list
this extension after ``sphinxcontrib.mermaid`` in ``extensions``.
"""
from __future__ import annotations

from sphinx.application import Sphinx
from sphinxcontrib.mermaid import mermaid


def _is_mermaid_asset(js) -> bool:
    """True for the mermaid ESM bundle / its inline importer script."""
    if "mermaid" in (getattr(js, "filename", "") or ""):
        return True
    body = (getattr(js, "attributes", None) or {}).get("body", "") or ""
    return "mermaid" in body


def drop_mermaid_assets(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree,
) -> None:
    if app.builder.format != "html":
        return
    has_mermaid = doctree is not None and doctree.next_node(mermaid) is not None
    if not has_mermaid:
        app.builder.script_files[:] = [
            js for js in app.builder.script_files if not _is_mermaid_asset(js)
        ]


def setup(app: Sphinx):
    app.connect("html-page-context", drop_mermaid_assets)
    return {"version": "0.1", "parallel_read_safe": True}
