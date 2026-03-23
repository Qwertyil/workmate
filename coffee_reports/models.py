from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol, Sequence


@dataclass(frozen=True, slots=True)
class StudyRecord:
    student: str
    date: date
    coffee_spent: int
    sleep_hours: float
    study_hours: int
    mood: str
    exam: str


@dataclass(frozen=True, slots=True)
class ReportTable:
    headers: tuple[str, ...]
    rows: tuple[tuple[object, ...], ...]


class ReportBuilder(Protocol):
    def __call__(self, records: Sequence[StudyRecord]) -> ReportTable:
        ...
