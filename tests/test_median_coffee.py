from datetime import date

from coffee_reports.models import StudyRecord
from coffee_reports.reports.median_coffee import build_median_coffee_report


def make_record(student: str, coffee_spent: int) -> StudyRecord:
    return StudyRecord(
        student=student,
        date=date(2024, 6, 1),
        coffee_spent=coffee_spent,
        sleep_hours=6.0,
        study_hours=8,
        mood="ok",
        exam="Math",
    )


def test_build_median_coffee_report_returns_sorted_rows() -> None:
    report = build_median_coffee_report(
        [
            make_record("Maria", 150),
            make_record("Ivan", 600),
            make_record("Maria", 100),
            make_record("Ivan", 700),
            make_record("Pavel", 450),
            make_record("Ivan", 650),
        ]
    )

    assert report.headers == ("student", "median_coffee")
    assert report.rows == (
        ("Ivan", 650),
        ("Pavel", 450),
        ("Maria", 125),
    )


def test_build_median_coffee_report_uses_student_name_as_tie_breaker() -> None:
    report = build_median_coffee_report(
        [
            make_record("Boris", 200),
            make_record("Boris", 400),
            make_record("Anna", 100),
            make_record("Anna", 500),
        ]
    )

    assert report.rows == (
        ("Anna", 300),
        ("Boris", 300),
    )


def test_build_median_coffee_report_returns_empty_rows_for_empty_input() -> None:
    report = build_median_coffee_report([])

    assert report.headers == ("student", "median_coffee")
    assert report.rows == ()
