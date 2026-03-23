from __future__ import annotations

from tabulate import tabulate

from coffee_reports.models import ReportTable


def render_report_table(report_table: ReportTable) -> str:
    return tabulate(
        report_table.rows,
        headers=report_table.headers,
        tablefmt="grid",
    )
