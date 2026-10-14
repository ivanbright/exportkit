from exportkit import Column, Report


def test_column_display_plain():
    assert Column("Ticket").display(7) == "7"
    assert Column("Ticket").display(None) == ""


def test_column_display_format():
    column = Column("Joined", format=lambda dt: dt.strftime("%H:%M"))
    assert column.display(__import__("datetime").datetime(2026, 10, 14, 9, 5)) == "09:05"


def test_report_sequence_rows():
    report = Report(
        title="T",
        columns=[Column("A"), Column("B")],
        rows=[[1, 2], [3, 4]],
    )
    raws, displays = report.materialize()
    assert raws == [[1, 2], [3, 4]]
    assert displays == [["1", "2"], ["3", "4"]]


def test_report_mapping_rows():
    report = Report(
        title="T",
        columns=[Column("Ticket", key="number"), Column("Name", key="name")],
        rows=[{"number": 1, "name": "Amina", "ignored": True}],
    )
    raws, displays = report.materialize()
    assert raws == [[1, "Amina"]]
    assert displays == [["1", "Amina"]]


def test_report_short_rows_are_padded():
    report = Report(title="T", columns=[Column("A"), Column("B"), Column("C")], rows=[[1]])
    raws, displays = report.materialize()
    assert raws == [[1, None, None]]
    assert displays == [["1", "", ""]]


def test_report_accepts_generator_rows():
    report = Report(title="T", columns=[Column("N")], rows=([i] for i in range(3)))
    raws, _ = report.materialize()
    assert raws == [[0], [1], [2]]


def test_report_requires_a_column():
    import pytest

    with pytest.raises(ValueError):
        Report(title="T", columns=[])
