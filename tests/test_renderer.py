from coffee_reports.models import ReportTable
from coffee_reports.renderer import render_report_table


def test_render_report_table_returns_grid_table() -> None:
    report_table = ReportTable(
        headers=("student", "median_coffee"),
        rows=(
            ("Ivan Kuznetsov", 650),
            ("Pavel Novikov", 450),
        ),
    )

    rendered_table = render_report_table(report_table)

    assert "student" in rendered_table
    assert "median_coffee" in rendered_table
    assert "Ivan Kuznetsov" in rendered_table
    assert "650" in rendered_table
    assert rendered_table.startswith("+")
    assert "| student" in rendered_table
