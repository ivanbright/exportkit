"""Public rendering entry points."""

from __future__ import annotations

import os
from typing import Any, Mapping

from .exceptions import UnsupportedFormatError
from .formats import Format
from .model import Report


def render(report: Report, fmt: "Format | str", *, options: Mapping[str, Any] | None = None) -> bytes:
    """Render ``report`` to ``fmt`` and return the file contents as bytes.

    ``options`` is forwarded to the writer (e.g. ``{"accent_color": "58718a"}``
    for XLSX, ``{"font": "path/to.ttf"}`` for PDF).
    """
    target = Format.coerce(fmt)
    opts = dict(options or {})
    raws, displays = report.materialize()

    if target is Format.XLSX:
        from .writers.xlsx import write_xlsx

        return write_xlsx(report, raws, displays, opts)
    if target is Format.DOCX:
        from .writers.docx import write_docx

        return write_docx(report, raws, displays, opts)
    if target is Format.PDF:
        from .writers.pdf import write_pdf

        return write_pdf(report, raws, displays, opts)
    raise UnsupportedFormatError(f"Unsupported format: {target!r}")  # pragma: no cover


def render_to(report: Report, fmt: "Format | str", target, *, options: Mapping[str, Any] | None = None) -> str:
    """Render ``report`` and write it to ``target``.

    ``target`` may be a filesystem path or any binary file-like object. Returns
    the path as a string when one was given, otherwise an empty string.
    """
    data = render(report, fmt, options=options)
    if hasattr(target, "write"):
        target.write(data)
        return ""
    path = os.fspath(target)
    with open(path, "wb") as handle:
        handle.write(data)
    return path
