from collections.abc import Callable
from datetime import date

import pytest

from coffee_reports.models import StudyRecord
from coffee_reports.reports.median_coffee import build_median_coffee_report


@pytest.fixture
def make_record() -> Callable[[str, int], StudyRecord]:
    def _make_record(student: str, coffee_spent: int) -> StudyRecord:
        return StudyRecord(
            student=student,
            date=date(2024, 6, 1),
            coffee_spent=coffee_spent,
            sleep_hours=6.0,
            study_hours=8,
            mood="ok",
            exam="Math",
        )

    return _make_record


@pytest.mark.parametrize(
    ("raw_records", "expected_rows"),
    [
        pytest.param(
            [
                ("Maria", 150),
                ("Ivan", 600),
                ("Maria", 100),
                ("Ivan", 700),
                ("Pavel", 450),
                ("Ivan", 650),
            ],
            (
                ("Ivan", 650),
                ("Pavel", 450),
                ("Maria", 125),
            ),
            id="sorted-by-median-desc",
        ),
        pytest.param(
            [
                ("Boris", 200),
                ("Boris", 400),
                ("Anna", 100),
                ("Anna", 500),
            ],
            (
                ("Anna", 300),
                ("Boris", 300),
            ),
            id="student-name-tie-breaker",
        ),
        pytest.param([], (), id="empty-input"),
    ],
)
def test_build_median_coffee_report(
    make_record: Callable[[str, int], StudyRecord],
    raw_records: list[tuple[str, int]],
    expected_rows: tuple[tuple[str, int], ...],
) -> None:
    report = build_median_coffee_report(
        [
            make_record(student, coffee_spent)
            for student, coffee_spent in raw_records
        ]
    )

    assert report.headers == ("student", "median_coffee")
    assert report.rows == expected_rows
