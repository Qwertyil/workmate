from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from coffee_reports.loader import FileReadError, load_records
from coffee_reports.renderer import render_report_table
from coffee_reports.reports import (
    get_report_builder,
    list_report_names,
)


def build_parser() -> argparse.ArgumentParser:
    available_reports = list_report_names()
    parser = argparse.ArgumentParser(
        description="Build coffee consumption reports from CSV files.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Path to one or more CSV files with study records.",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=available_reports,
        help=f"Report name to build. Available reports: {', '.join(available_reports)}.",
    )
    return parser


def run_report(file_paths: Sequence[str], report_name: str) -> str:
    report_builder = get_report_builder(report_name)
    records = load_records(file_paths)
    report_table = report_builder(records)
    return render_report_table(report_table)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        rendered_report = run_report(args.files, args.report)
    except FileReadError as error:
        print(str(error), file=sys.stderr)
        return 1

    print(rendered_report)
    return 0
