from datetime import date
from pathlib import Path
from typing import Any, IO

import pytest

from coffee_reports.loader import FileReadError, load_records, load_records_from_file
from coffee_reports.models import StudyRecord


CSV_HEADER = "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"


def write_csv(path: Path, rows: list[str]) -> None:
    path.write_text(CSV_HEADER + "".join(rows), encoding="utf-8")


def test_load_records_from_file_parses_csv_rows(tmp_path: Path) -> None:
    file_path = tmp_path / "math.csv"
    write_csv(
        file_path,
        [
            "Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика\n",
            "Дарья Петрова,2024-06-02,250,6.5,8,норм,Математика\n",
        ],
    )

    records = load_records_from_file(file_path)

    assert records == [
        StudyRecord(
            student="Алексей Смирнов",
            date=date(2024, 6, 1),
            coffee_spent=450,
            sleep_hours=4.5,
            study_hours=12,
            mood="норм",
            exam="Математика",
        ),
        StudyRecord(
            student="Дарья Петрова",
            date=date(2024, 6, 2),
            coffee_spent=250,
            sleep_hours=6.5,
            study_hours=8,
            mood="норм",
            exam="Математика",
        ),
    ]


def test_load_records_combines_records_from_multiple_files(tmp_path: Path) -> None:
    math_file = tmp_path / "math.csv"
    physics_file = tmp_path / "physics.csv"
    write_csv(
        math_file,
        ["Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика\n"],
    )
    write_csv(
        physics_file,
        ["Мария Соколова,2024-06-02,120,8.5,2,отл,Физика\n"],
    )

    records = load_records([math_file, physics_file])

    assert [record.student for record in records] == [
        "Иван Кузнецов",
        "Мария Соколова",
    ]


def test_load_records_from_file_raises_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileReadError, match="file does not exist"):
        load_records_from_file(missing_file)


def test_load_records_from_file_raises_for_unreadable_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    file_path = tmp_path / "math.csv"
    write_csv(
        file_path,
        ["Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика\n"],
    )

    original_open = Path.open

    def mocked_open(
        self: Path,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> IO[Any]:
        if self == file_path:
            raise PermissionError("permission denied")
        return original_open(
            self,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    monkeypatch.setattr(Path, "open", mocked_open)

    with pytest.raises(FileReadError, match="file is not readable"):
        load_records_from_file(file_path)



def test_load_records_from_file_raises_for_directory(tmp_path: Path) -> None:
    with pytest.raises(FileReadError, match="expected a file, got a directory"):
        load_records_from_file(tmp_path)
