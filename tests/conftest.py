import csv
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

import pytest


CSV_HEADER = (
    "student",
    "date",
    "coffee_spent",
    "sleep_hours",
    "study_hours",
    "mood",
    "exam",
)


@pytest.fixture
def write_csv() -> Callable[[Path, Iterable[Sequence[object]]], None]:
    def _write_csv(path: Path, rows: Iterable[Sequence[object]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(CSV_HEADER)
            writer.writerows(rows)

    return _write_csv
