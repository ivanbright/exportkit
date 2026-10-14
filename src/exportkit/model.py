"""The declarative data model: :class:`Column` and :class:`Report`."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, Sequence


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


@dataclass
class Column:
    """One column of a report.

    ``key`` selects the field from mapping rows; ``format`` optionally turns a
    raw value into display text; ``align`` is one of ``left``/``center``/``right``.
    """

    header: str
    key: str | None = None
    align: str = "left"
    width: float | None = None
    format: Callable[[Any], str] | None = None

    def display(self, value: Any) -> str:
        if self.format is not None:
            return _to_text(self.format(value))
        return _to_text(value)


@dataclass
class Report:
    """A title, a set of columns, and rows of data.

    Rows may be sequences (positional) or mappings (selected by each column's
    ``key``). ``rows`` is iterated exactly once at render time, so generators
    are accepted.
    """

    title: str
    columns: Sequence[Column]
    rows: Iterable[Any] = field(default_factory=list)
    subtitle: str = ""
    meta: Mapping[str, Any] = field(default_factory=dict)
    summary: Mapping[str, Any] = field(default_factory=dict)
    footer: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    landscape: bool = False
    sheet_name: str = "Report"

    def __post_init__(self) -> None:
        self.columns = list(self.columns)
        if not self.columns:
            raise ValueError("A report needs at least one column.")

    def materialize(self) -> tuple[list[list[Any]], list[list[str]]]:
        """Return ``(raw_rows, display_rows)`` aligned to the columns."""
        raws: list[list[Any]] = []
        displays: list[list[str]] = []
        width = len(self.columns)
        for row in self.rows:
            if isinstance(row, Mapping):
                raw = [row.get(column.key) for column in self.columns]
            else:
                values = list(row)
                raw = [values[i] if i < len(values) else None for i in range(width)]
            raws.append(raw)
            displays.append([column.display(value) for column, value in zip(self.columns, raw)])
        return raws, displays
