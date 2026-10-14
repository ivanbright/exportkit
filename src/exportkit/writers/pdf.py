"""PDF writer built on fpdf2.

Core PDF fonts cover Latin-1 only, so text is normalised to Latin-1 unless a
Unicode TTF is supplied through ``options={"font": "/path/to/font.ttf"}``.
"""

from __future__ import annotations

from typing import Any

from ..exceptions import MissingDependencyError

_TRANSLATE = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u2022": "*",
        "\u00a0": " ",
    }
)


def _latin1(value: Any) -> str:
    text = str(value).translate(_TRANSLATE)
    return text.encode("latin-1", "replace").decode("latin-1")


def write_pdf(report, raws: list[list[Any]], displays: list[list[str]], options: dict) -> bytes:
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos
    except ImportError as exc:  # pragma: no cover - depends on install extras
        raise MissingDependencyError(
            "PDF export needs fpdf2. Install it with: pip install exportkit[pdf]"
        ) from exc

    generated = report.created_at.strftime("%Y-%m-%d %H:%M")
    footer_text = " · ".join(part for part in [report.footer, f"Generated {generated}"] if part)

    class _Pdf(FPDF):
        family = "Helvetica"
        footer_text = ""

        def footer(self) -> None:  # called automatically on every page
            self.set_y(-13)
            self.set_font(self.family, size=8)
            self.set_text_color(130, 130, 140)
            half = self.epw / 2
            self.cell(half, 6, _latin1(self.footer_text), align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.cell(half, 6, f"Page {self.page_no()}/{{nb}}", align="R")

    pdf = _Pdf(orientation="L" if report.landscape else "P", unit="mm", format="A4")

    font_path = options.get("font")
    if font_path:
        pdf.add_font("Report", "", font_path)
        family = "Report"
    else:
        family = "Helvetica"
    pdf.family = family
    pdf.footer_text = footer_text
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    def line(text: Any, height: float) -> None:
        pdf.multi_cell(0, height, _latin1(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(family, size=16)
    pdf.set_text_color(36, 36, 38)
    line(report.title, 9)

    if report.subtitle:
        pdf.set_font(family, size=11)
        pdf.set_text_color(77, 79, 87)
        line(report.subtitle, 6)

    if report.meta:
        pdf.ln(1)
        pdf.set_font(family, size=10)
        pdf.set_text_color(77, 79, 87)
        for key, value in report.meta.items():
            line(f"{key}: {value}", 6)

    pdf.ln(3)
    pdf.set_text_color(36, 36, 38)
    pdf.set_font(family, size=10)

    aligns = tuple(column.align.upper() for column in report.columns)
    widths = [column.width for column in report.columns]
    table_kwargs: dict[str, Any] = {"text_align": aligns, "line_height": 6, "padding": 2}
    if all(widths):
        table_kwargs["col_widths"] = widths

    with pdf.table(**table_kwargs) as table:
        header = table.row()
        for column in report.columns:
            header.cell(_latin1(column.header))
        for display in displays:
            row = table.row()
            for value in display:
                row.cell(_latin1(value))

    if report.summary:
        pdf.ln(3)
        pdf.set_font(family, size=10)
        for key, value in report.summary.items():
            line(f"{key}: {value}", 6)

    return bytes(pdf.output())
