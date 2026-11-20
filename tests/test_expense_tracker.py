import io
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.expense_tracker import analyze_expenses, create_synthetic_dataset, load_and_clean_expenses


class ExpenseTrackerTests(unittest.TestCase):
    def test_synthetic_dataset_is_reproducible_and_has_required_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.csv"
            first = create_synthetic_dataset(path, rows=10, seed=5, end_date=pd.Timestamp("2025-03-31"))
            second = create_synthetic_dataset(path, rows=10, seed=5, end_date=pd.Timestamp("2025-03-31"))
            pd.testing.assert_frame_equal(first, second)
            self.assertEqual(len(first), 10)
            self.assertTrue(path.exists())

    def test_cleaning_removes_invalid_amounts_and_normalizes_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.csv"
            pd.DataFrame(
                [
                    ["2025-01-02", " food ", 12, " cash ", " lunch "],
                    ["not-a-date", "Travel", 20, "Card", "invalid date"],
                    ["2025-01-03", "Travel", -1, "Card", "invalid amount"],
                ],
                columns=["date", "category", "amount", "payment_method", "description"],
            ).to_csv(path, index=False)
            clean, stats = load_and_clean_expenses(path)
            self.assertEqual(stats, {"rows_read": 3, "rows_kept": 1, "rows_removed": 2})
            self.assertEqual(clean.iloc[0]["category"], "Food")
            self.assertEqual(clean.iloc[0]["payment_method"], "Cash")

    def test_cleaning_accepts_uploaded_csv_stream(self):
        uploaded_csv = io.BytesIO(
            b"date,category,amount,payment_method,description\n"
            b"2025-02-01,Food,18.5,Card,coffee\n"
        )
        clean, stats = load_and_clean_expenses(uploaded_csv)
        self.assertEqual(len(clean), 1)
        self.assertEqual(clean.iloc[0]["amount"], 18.5)
        self.assertEqual(stats["rows_kept"], 1)

    def test_analysis_calculates_total_category_and_daily_average(self):
        data = pd.DataFrame(
            {
                "date": pd.to_datetime(["2025-01-01", "2025-01-03"]),
                "category": ["Food", "Transport"],
                "amount": [10.0, 30.0],
                "payment_method": ["Cash", "Card"],
                "description": ["lunch", "bus"],
            }
        )
        result = analyze_expenses(data)
        self.assertEqual(result["total"], 40.0)
        self.assertEqual(result["highest_category"], "Transport")
        self.assertEqual(result["latest_month"], "2025-01")
        self.assertEqual(result["average_daily"], 40.0 / 3)


if __name__ == "__main__":
    unittest.main()
