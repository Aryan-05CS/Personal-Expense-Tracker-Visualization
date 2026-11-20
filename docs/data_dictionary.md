# Expense CSV data dictionary

The input CSV must have these columns in any order:

| Column | Meaning | Example |
|---|---|---|
| `date` | Date the expense occurred; pandas-parseable | `2025-05-17` |
| `category` | Expense category | `Food` |
| `amount` | Positive numeric amount; keep one currency per file | `245.50` |
| `payment_method` | How it was paid | `Card` |
| `description` | Short note; may be blank | `Lunch` |

Rows with an invalid date, non-numeric or non-positive amount, or blank category/payment method are excluded and counted in the terminal cleaning summary. The tracker does not connect to banks, store account credentials, or infer a currency.
