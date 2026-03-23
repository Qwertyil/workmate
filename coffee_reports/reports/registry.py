from __future__ import annotations

from coffee_reports.models import ReportBuilder
from coffee_reports.reports.median_coffee import (
    REPORT_NAME as MEDIAN_COFFEE_REPORT_NAME,
    build_median_coffee_report,
)


class UnknownReportError(ValueError):
    def __init__(self, report_name: str) -> None:
        self.report_name = report_name
        super().__init__(f"Unknown report: {report_name}")


REPORT_BUILDERS: dict[str, ReportBuilder] = {
    MEDIAN_COFFEE_REPORT_NAME: build_median_coffee_report,
}


def get_report_builder(report_name: str) -> ReportBuilder:
    try:
        return REPORT_BUILDERS[report_name]
    except KeyError as error:
        raise UnknownReportError(report_name) from error


def list_report_names() -> tuple[str, ...]:
    return tuple(sorted(REPORT_BUILDERS))
