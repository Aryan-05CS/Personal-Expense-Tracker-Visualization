"""Command-line entry point for the Personal Expense Tracker."""

import argparse
from pathlib import Path

from src.expense_tracker import (
    analyze_expenses,
    create_charts,
    create_synthetic_dataset,
    load_and_clean_expenses,
    print_summary,
    write_reports,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze personal expenses from a CSV file.")
    parser.add_argument("--input", type=Path, default=None, help="Path to the expense CSV (default: data/expenses.csv).")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Folder for reports and charts.")
    parser.add_argument(
        "--generate-sample",
        action="store_true",
        help="Create a reproducible synthetic CSV at --input before analysis.",
    )
    parser.add_argument("--sample-rows", type=int, default=120, help="Number of synthetic rows to create.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for synthetic data.")
    parser.add_argument(
        "--monthly-budget",
        type=float,
        default=None,
        help="Optional budget to compare with the latest month's spending.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input or Path("data/expenses.csv")
    if args.monthly_budget is not None and args.monthly_budget <= 0:
        raise ValueError("--monthly-budget must be greater than zero.")
    if args.generate_sample or (args.input is None and not input_path.exists()):
        print(f"Creating {args.sample_rows} synthetic expense records at {input_path}...")
        create_synthetic_dataset(input_path, rows=args.sample_rows, seed=args.seed)
    elif not input_path.is_file():
        raise FileNotFoundError(f"Expense CSV not found: {input_path}")

    expenses, cleaning = load_and_clean_expenses(input_path)
    print(
        f"Loaded {cleaning['rows_read']} rows; kept {cleaning['rows_kept']} "
        f"and removed {cleaning['rows_removed']} invalid rows."
    )
    analysis = analyze_expenses(expenses)
    charts_dir = args.output_dir / "charts"
    reports_dir = args.output_dir / "reports"
    charts = create_charts(analysis, charts_dir)
    reports = write_reports(analysis, reports_dir, monthly_budget=args.monthly_budget)
    print_summary(analysis, reports, charts)
    print("Chart files:")
    for chart in charts:
        print(f"  - {chart}")
    print("Report files:")
    for report in reports:
        print(f"  - {report}")


if __name__ == "__main__":
    main()
