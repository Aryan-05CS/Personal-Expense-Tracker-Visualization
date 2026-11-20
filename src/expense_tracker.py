"""Core data generation, cleaning, analysis, charting, and reporting."""

from pathlib import Path
from typing import IO, Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

REQUIRED_COLUMNS = ["date", "category", "amount", "payment_method", "description"]
CATEGORIES = ["Food", "Transport", "Housing", "Utilities", "Shopping", "Health", "Education", "Entertainment"]
PAYMENT_METHODS = ["Cash", "Card", "Bank Transfer", "Mobile Wallet"]


def create_synthetic_dataset(
    path: Path, rows: int = 120, seed: int = 42, end_date: pd.Timestamp | None = None
) -> pd.DataFrame:
    """Create reproducible fictional expenses spanning the 90 days before end_date."""
    if rows < 1:
        raise ValueError("rows must be greater than zero")

    rng = np.random.default_rng(seed)
    last_day = pd.Timestamp(end_date or pd.Timestamp.today()).normalize()
    dates = last_day - pd.to_timedelta(rng.integers(0, 90, size=rows), unit="D")
    categories = rng.choice(CATEGORIES, size=rows, p=[0.25, 0.15, 0.12, 0.1, 0.14, 0.07, 0.08, 0.09])
    amounts = np.maximum(50, np.round(rng.lognormal(mean=6.2, sigma=0.8, size=rows), 2))
    data = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "category": categories,
            "amount": amounts,
            "payment_method": rng.choice(PAYMENT_METHODS, size=rows, p=[0.2, 0.3, 0.2, 0.3]),
            "description": [f"Synthetic {category.lower()} expense" for category in categories],
        }
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)
    return data


def load_and_clean_expenses(path: Path | IO[bytes]) -> tuple[pd.DataFrame, dict[str, int]]:
    """Load a CSV, normalize text, and remove rows with unusable values."""
    raw = pd.read_csv(path)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(raw.columns))
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}")

    data = raw[REQUIRED_COLUMNS].copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
    for column in ("category", "payment_method", "description"):
        data[column] = data[column].astype("string").str.strip()

    invalid_date = data["date"].isna()
    invalid_amount = data["amount"].isna() | (data["amount"] <= 0)
    invalid_text = data[["category", "payment_method"]].isna().any(axis=1)
    invalid_text |= data["category"].eq("") | data["payment_method"].eq("")
    invalid_rows = invalid_date | invalid_amount | invalid_text
    clean = data.loc[~invalid_rows].copy()
    if clean.empty:
        raise ValueError("No valid expense rows remain after cleaning.")

    clean["category"] = clean["category"].str.title()
    clean["payment_method"] = clean["payment_method"].str.title()
    clean["description"] = clean["description"].fillna("")
    clean = clean.sort_values("date").reset_index(drop=True)
    stats = {
        "rows_read": len(raw),
        "rows_kept": len(clean),
        "rows_removed": int(invalid_rows.sum()),
    }
    return clean, stats


def analyze_expenses(data: pd.DataFrame) -> dict[str, Any]:
    """Calculate category, month, payment-method, and daily spending summaries."""
    if data.empty:
        raise ValueError("Cannot analyze an empty expense dataset.")

    category = (
        data.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .reset_index(drop=True)
    )
    monthly = data.assign(month=data["date"].dt.to_period("M").astype(str)).groupby("month", as_index=False).agg(
        total_spending=("amount", "sum"),
        transaction_count=("amount", "size"),
    )
    payment = (
        data.groupby("payment_method", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .reset_index(drop=True)
    )
    daily = data.groupby(data["date"].dt.normalize())["amount"].sum().rename_axis("date").reset_index()
    total = float(data["amount"].sum())
    first_date = data["date"].min().normalize()
    last_date = data["date"].max().normalize()
    days_inclusive = (last_date - first_date).days + 1
    latest_month = last_date.strftime("%Y-%m")
    current_month_total = float(
        monthly.loc[monthly["month"] == latest_month, "total_spending"].iloc[0]
    )
    return {
        "category": category,
        "monthly": monthly,
        "payment": payment,
        "daily": daily,
        "total": total,
        "highest_category": str(category.iloc[0]["category"]),
        "highest_category_total": float(category.iloc[0]["amount"]),
        "average_daily": total / days_inclusive,
        "latest_month": latest_month,
        "latest_month_total": current_month_total,
        "transaction_count": len(data),
        "date_range": (first_date, last_date),
    }


def create_charts(analysis: dict[str, Any], output_dir: Path) -> list[Path]:
    """Save four labeled charts and return their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    chart_paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=analysis["category"], x="amount", y="category", ax=ax, color="#4472C4")
    ax.set(title="Spending by Category", xlabel="Total spending", ylabel="")
    fig.tight_layout()
    path = output_dir / "category_spending.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=analysis["monthly"], x="month", y="total_spending", marker="o", ax=ax, color="#ED7D31")
    ax.set(title="Monthly Spending Trend", xlabel="Month", ylabel="Total spending")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    path = output_dir / "monthly_spending.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        analysis["payment"]["amount"],
        labels=analysis["payment"]["payment_method"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Spending by Payment Method")
    fig.tight_layout()
    path = output_dir / "payment_method_spending.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=analysis["daily"], x="date", y="amount", marker=".", ax=ax, color="#70AD47")
    ax.set(title="Daily Spending Trend (days with expenses)", xlabel="Date", ylabel="Daily total")
    fig.tight_layout()
    path = output_dir / "daily_spending.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)
    return chart_paths


def write_reports(analysis: dict[str, Any], output_dir: Path, monthly_budget: float | None = None) -> list[Path]:
    """Write machine-readable summaries and a plain-text insight report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    csvs = {
        "category_summary.csv": analysis["category"],
        "monthly_summary.csv": analysis["monthly"],
        "payment_method_summary.csv": analysis["payment"],
        "daily_summary.csv": analysis["daily"],
    }
    paths: list[Path] = []
    for filename, frame in csvs.items():
        path = output_dir / filename
        frame.to_csv(path, index=False)
        paths.append(path)

    first_date, last_date = analysis["date_range"]
    lines = [
        "PERSONAL EXPENSE TRACKER - SUMMARY",
        f"Period covered: {first_date:%Y-%m-%d} to {last_date:%Y-%m-%d}",
        f"Transactions analyzed: {analysis['transaction_count']}",
        f"Total spending: {analysis['total']:.2f}",
        f"Average daily spending (calendar days in period): {analysis['average_daily']:.2f}",
        f"Highest spending category: {analysis['highest_category']} ({analysis['highest_category_total']:.2f})",
        f"Spending in latest month ({analysis['latest_month']}): {analysis['latest_month_total']:.2f}",
    ]
    if monthly_budget is not None:
        if monthly_budget <= 0:
            raise ValueError("monthly_budget must be greater than zero")
        difference = analysis["latest_month_total"] - monthly_budget
        if difference > 0:
            lines.append(f"Budget status: over budget by {difference:.2f} for {analysis['latest_month']}.")
        else:
            lines.append(f"Budget status: {abs(difference):.2f} under budget for {analysis['latest_month']}.")
    else:
        lines.append("Budget status: not assessed (run with --monthly-budget to compare).")

    path = output_dir / "summary_report.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths.append(path)
    return paths


def print_summary(analysis: dict[str, Any], reports: list[Path], charts: list[Path]) -> None:
    """Print a concise run summary for the terminal."""
    print("\nExpense analysis complete")
    print(f"Transactions analyzed: {analysis['transaction_count']}")
    print(f"Total spending: {analysis['total']:.2f}")
    print(f"Average daily spending: {analysis['average_daily']:.2f}")
    print(
        f"Highest spending category: {analysis['highest_category']} "
        f"({analysis['highest_category_total']:.2f})"
    )
    print(f"Latest month ({analysis['latest_month']}): {analysis['latest_month_total']:.2f}")
    print(f"Reports: {reports[0].parent.resolve()}")
    print(f"Charts: {charts[0].parent.resolve()}")
