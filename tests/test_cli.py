import csv
from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from coffee_reports.cli import main


CSV_HEADER = [
    "student",
    "date",
    "coffee_spent",
    "sleep_hours",
    "study_hours",
    "mood",
    "exam",
]


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)


def test_main_returns_zero_and_prints_report_table(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    math_file = tmp_path / "math.csv"
    physics_file = tmp_path / "physics.csv"
    write_csv(
        math_file,
        [
            ["Ivan Kuznetsov", "2024-06-01", "600", "3.0", "15", "tired", "Math"],
            ["Ivan Kuznetsov", "2024-06-02", "700", "2.5", "17", "zombie", "Math"],
        ],
    )
    write_csv(
        physics_file,
        [
            ["Maria Sokolova", "2024-06-01", "100", "8.0", "3", "great", "Physics"],
            ["Maria Sokolova", "2024-06-02", "150", "7.5", "4", "great", "Physics"],
        ],
    )

    exit_code = main(
        [
            "--files",
            str(math_file),
            str(physics_file),
            "--report",
            "median-coffee",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Ivan Kuznetsov" in captured.out
    assert "Maria Sokolova" in captured.out
    assert "650" in captured.out
    assert "125" in captured.out
    assert captured.err == ""


def test_main_exits_for_unknown_report(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    file_path = tmp_path / "math.csv"
    write_csv(
        file_path,
        [
            ["Ivan Kuznetsov", "2024-06-01", "600", "3.0", "15", "tired", "Math"],
        ],
    )

    with pytest.raises(SystemExit) as error:
        main(
            [
                "--files",
                str(file_path),
                "--report",
                "average-coffee",
            ]
        )
    captured = capsys.readouterr()

    assert error.value.code == 2
    assert captured.out == ""
    assert "invalid choice: 'average-coffee'" in captured.err
    assert "median-coffee" in captured.err


def test_main_returns_error_for_missing_file(
    capsys: CaptureFixture[str],
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing.csv"

    exit_code = main(
        [
            "--files",
            str(missing_file),
            "--report",
            "median-coffee",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert f"Cannot read {missing_file}: file does not exist" in captured.err
