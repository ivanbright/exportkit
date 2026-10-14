import pytest

from exportkit import Format
from exportkit.exceptions import UnsupportedFormatError


@pytest.mark.parametrize(
    "value,expected",
    [
        ("xlsx", Format.XLSX),
        ("Excel", Format.XLSX),
        (".PDF", Format.PDF),
        ("word", Format.DOCX),
        ("application/pdf", Format.PDF),
        (Format.DOCX, Format.DOCX),
        (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            Format.XLSX,
        ),
    ],
)
def test_coerce(value, expected):
    assert Format.coerce(value) is expected


def test_unsupported_format():
    with pytest.raises(UnsupportedFormatError):
        Format.coerce("csv")
    with pytest.raises(UnsupportedFormatError):
        Format.coerce(123)


def test_metadata_helpers():
    assert Format.XLSX.extension == ".xlsx"
    assert Format.PDF.content_type == "application/pdf"
    assert Format.DOCX.filename("report") == "report.docx"
