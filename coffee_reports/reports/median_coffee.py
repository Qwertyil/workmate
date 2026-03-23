from __future__ import annotations

from collections import defaultdict
from statistics import median
from typing import Sequence

from coffee_reports.models import ReportTable, StudyRecord


REPORT_NAME = "median-coffee"


def build_median_coffee_report(records: Sequence[StudyRecord]) -> ReportTable:
    """Build the median coffee spending report for all provided records."""
    spent_by_student: dict[str, list[int]] = defaultdict(list)
    for record in records:
        spent_by_student[record.student].append(record.coffee_spent)

    rows = []
    for student, spending_values in spent_by_student.items():
        student_median = median(spending_values)
        if isinstance(student_median, float) and student_median.is_integer():
            student_median = int(student_median)
        rows.append((student, student_median))

    rows.sort(key=lambda row: (-row[1], row[0]))
    return ReportTable(
        headers=("student", "median_coffee"),
        rows=tuple(rows),
    )
