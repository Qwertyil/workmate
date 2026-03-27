from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any, IO

import pytest

from coffee_reports.loader import FileReadError, load_records, load_records_from_file
from coffee_reports.models import StudyRecord


def test_load_records_from_file_parses_csv_rows(
    tmp_path: Path,
    write_csv: Callable[[Path, list[list[object]]], None],
) -> None:
    file_path = tmp_path / "math.csv"
    write_csv(
        file_path,
        [
            ["Алексей Смирнов", "2024-06-01", 450, 4.5, 12, "норм", "Математика"],
            ["Дарья Петрова", "2024-06-02", 250, 6.5, 8, "норм", "Математика"],
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


def test_load_records_combines_records_from_multiple_files(
    tmp_path: Path,
    write_csv: Callable[[Path, list[list[object]]], None],
) -> None:
    math_file = tmp_path / "math.csv"
    physics_file = tmp_path / "physics.csv"
    write_csv(
        math_file,
        [["Иван Кузнецов", "2024-06-01", 600, 3.0, 15, "зомби", "Математика"]],
    )
    write_csv(
        physics_file,
        [["Мария Соколова", "2024-06-02", 120, 8.5, 2, "отл", "Физика"]],
    )

    records = load_records([math_file, physics_file])

    assert [record.student for record in records] == [
        "Иван Кузнецов",
        "Мария Соколова",
    ]


@pytest.mark.parametrize(
    ("path_name", "path_kind", "expected_message"),
    [
        pytest.param("missing.csv", "missing", "file does not exist", id="missing-file"),
        pytest.param("records", "directory", "expected a file, got a directory", id="directory"),
    ],
)
def test_load_records_from_file_raises_for_invalid_path(
    tmp_path: Path,
    path_name: str,
    path_kind: str,
    expected_message: str,
) -> None:
    path = tmp_path / path_name
    if path_kind == "directory":
        path.mkdir()

    with pytest.raises(FileReadError, match=expected_message):
        load_records_from_file(path)


def test_load_records_from_file_raises_for_unreadable_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    write_csv: Callable[[Path, list[list[object]]], None],
) -> None:
    file_path = tmp_path / "math.csv"
    write_csv(
        file_path,
        [["Иван Кузнецов", "2024-06-01", 600, 3.0, 15, "зомби", "Математика"]],
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
