from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from datetime import date
from pathlib import Path

from coffee_reports.models import StudyRecord


class FileReadError(ValueError):
    def __init__(self, path: Path, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Cannot read {path}: {reason}")


def load_records(file_paths: Iterable[str | Path]) -> list[StudyRecord]:
    records: list[StudyRecord] = []
    for file_path in file_paths:
        records.extend(load_records_from_file(file_path))
    return records


def load_records_from_file(file_path: str | Path) -> list[StudyRecord]:
    path = Path(file_path)
    try:
        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            return [build_study_record(row) for row in reader]
    except FileNotFoundError as error:
        raise FileReadError(path, "file does not exist") from error
    except PermissionError as error:
        raise FileReadError(path, "file is not readable") from error
    except IsADirectoryError as error:
        raise FileReadError(path, "expected a file, got a directory") from error


def build_study_record(row: Mapping[str, str]) -> StudyRecord:
    return StudyRecord(
        student=row["student"],
        date=date.fromisoformat(row["date"]),
        coffee_spent=int(row["coffee_spent"]),
        sleep_hours=float(row["sleep_hours"]),
        study_hours=int(row["study_hours"]),
        mood=row["mood"],
        exam=row["exam"],
    )
