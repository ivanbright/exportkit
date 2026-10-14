"""Output formats supported by exportkit."""

from __future__ import annotations

from enum import Enum

from .exceptions import UnsupportedFormatError

_CONTENT_TYPES = {
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pdf": "application/pdf",
}

_ALIASES = {
    "xlsx": "xlsx",
    "xls": "xlsx",
    "excel": "xlsx",
    ".xlsx": "xlsx",
    "spreadsheet": "xlsx",
    "docx": "docx",
    "word": "docx",
    "doc": "docx",
    ".docx": "docx",
    "pdf": "pdf",
    ".pdf": "pdf",
}


class Format(str, Enum):
    """A supported output document format."""

    XLSX = "xlsx"
    DOCX = "docx"
    PDF = "pdf"

    @classmethod
    def coerce(cls, value: "Format | str") -> "Format":
        """Return a :class:`Format` from an enum member, name, extension or MIME type."""
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise UnsupportedFormatError(f"Unsupported format: {value!r}")
        candidate = value.strip().lower()
        if candidate in _ALIASES:
            return cls(_ALIASES[candidate])
        for fmt in cls:
            if fmt.content_type == candidate:
                return fmt
        raise UnsupportedFormatError(
            f"Unsupported format: {value!r}. Expected one of: "
            + ", ".join(f.value for f in cls)
        )

    @property
    def content_type(self) -> str:
        return _CONTENT_TYPES[self.value]

    @property
    def extension(self) -> str:
        return f".{self.value}"

    def filename(self, stem: str) -> str:
        """Build a filename such as ``waiting-list.xlsx`` from a stem."""
        return f"{stem}{self.extension}"
