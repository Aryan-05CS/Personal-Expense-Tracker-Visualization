# Personal Expense Tracker with Data Visualization

A Python project that analyzes manually entered or synthetic expense records stored in CSV files. It cleans the data, summarizes spending by category, month, day, and payment method, saves four charts, and creates CSV/text reports. It does not connect to a bank or require real financial data.

> **Portfolio note:** the included demo data is synthetic. Replace it with your own CSV only if you are comfortable sharing it; never upload account numbers, credentials, or private financial records.

## Project overview

### Problem statement

Expenses written in different places are difficult to total and compare. This tracker provides one repeatable workflow to identify where money goes, compare monthly spending, and prepare a simple budget check.

### Why it is useful

Individuals, students, employees, and families can use the summaries to notice spending patterns, plan savings, and make budgets. Freelancers and small businesses can adapt the same CSV workflow for basic expense categorization (not accounting or tax advice). For a student portfolio, the project demonstrates Python programming, data cleaning, analysis, visualization, reporting, and reproducible automation.

### Simple and technical view

In plain language, add one row for each purchase; run the program to see totals and charts. Technically, pandas reads and validates the CSV, normalizes fields and parses dates, aggregates with group-by operations, then Matplotlib/Seaborn render chart files and pandas exports summary tables.

**Workflow:** expense data entry → CSV storage → data cleaning → category-wise analysis → monthly analysis → visualization → report generation.

## Features

- Create a reproducible synthetic dataset (default: 120 rows).
- Read a custom CSV with required fields: date, category, amount, payment method, and description.
- Parse dates, normalize text, and count invalid records removed.
- Calculate category totals, monthly totals/counts, payment-method totals, daily totals, highest-spending category, total spending, latest-month spending, and average daily spend across the calendar days covered.
- Save category bar, monthly line, payment-method pie, and daily trend charts.
- Export category, month, payment, and daily CSV summaries plus a plain-text report.
- Optionally compare the latest month against a monthly budget.

## Tech stack and options

| Option | Stack | Difficulty | Expected output |
|---|---|---:|---|
| A — Easy (recommended starting point) | Python, CSV, `datetime`, `csv`, terminal | Beginner | Validated records and text totals |
| B — Intermediate (this project) | Python, pandas, NumPy, Matplotlib, Seaborn, CSV | Beginner–intermediate | Repeatable analysis, charts, and reports |
| C — Advanced | Option B plus Streamlit, SQLite, pytest/CI, deployment | Intermediate–advanced | Interactive dashboard, persistent local store, and automated checks |

Option B is a good student portfolio balance: no service or bank API is needed, results are reproducible, and the code shows transferable data skills. This project also includes a Streamlit dashboard as a presentation layer without changing the CSV analysis workflow.

## Phase-wise implementation plan

| Phase | What to do | Why / expected output | Common beginner mistake |
|---|---|---|---|
| 1. Setup | Install Python and create/activate a virtual environment. | Isolated, repeatable Python setup. | Installing packages into a different interpreter. |
| 2. Project folders | Create `data/`, `src/`, `outputs/`, `images/`, `reports/`, `docs/`, and `notebooks/`. | Keep input, source, generated files, and documentation organized. | Mixing generated results with source code. |
| 3. Expense CSV | Define date, category, amount, payment method, and description; generate demo records. | A consistent, safe input dataset. | Mixed currencies or inconsistent column names. |
| 4. Data loading | Read the CSV with pandas and check required columns. | A predictable DataFrame ready for analysis. | Assuming every input file has the expected schema. |
| 5. Data cleaning | Parse dates/amounts, trim text, reject invalid records, and show counts. | Clean, explainable input; rows kept/removed are visible. | Silently dropping bad data or summing strings. |
| 6. Category analysis | Group and sum by category; identify the highest category. | Category totals and ranking. | Forgetting to sort or mishandling category spelling/case. |
| 7. Monthly analysis | Group dates by year-month and sum transaction amounts. | Monthly totals and transaction counts for trend comparisons. | Grouping by month name alone and combining different years. |
| 8. Visualization | Draw category, monthly, payment, and daily charts. | Four readable PNG files under `outputs/charts/`. | Missing labels or unclear time ranges. |
| 9. Report generation | Export summary CSVs and a text insight report; optionally compare a budget. | Portable results in `outputs/reports/`. | Claiming overspending when no budget was provided. |
| 10. GitHub upload | Test, review `.gitignore`, commit source/docs/screenshots, and push. | Public, reproducible portfolio repository. | Uploading private data, secrets, or the virtual environment. |

## Architecture and data flow

```text
Manual CSV entry / synthetic data generator
                    |
                    v
       CSV input: data/expenses.csv
                    |
                    v
 Load -> validate required columns -> clean dates, text and amounts
                    |
                    v
   Analyze: category | month | payment | day | key metrics
                    |
          +---------+----------+
          v                    v
 Matplotlib/Seaborn       pandas CSV + text
    chart images             reports
          +---------+----------+
                    v
       outputs/charts/ and outputs/reports/
```

### Input, processing, and output

Input fields are date, category, amount, payment method, and description. The program validates the columns, removes rows that cannot be analyzed, and groups valid records by category, calendar month, payment method, and date. Outputs include those summaries, highest category, average daily spending, total/latest-month spending, four charts, and an optional budget comparison. All amounts in a file should use one currency; no currency conversion is performed.

## Repository structure

```text
Personal-Expense-Tracker-Visualization/
├── data/                       # Input CSVs (demo expenses generated on first run)
├── docs/                       # Data dictionary and project documentation
├── images/                     # Portfolio screenshots; add your captures here
├── notebooks/                  # Optional exploratory notebooks
├── outputs/                    # Generated charts and reports (ignored by Git)
├── reports/                    # Detailed project report and curated portfolio reports
├── src/
│   └── expense_tracker.py      # Reusable generation, cleaning, analysis, chart/report functions
├── .streamlit/
│   └── config.toml             # Dashboard theme and chart palette
├── tests/
│   └── test_expense_tracker.py # Focused automated tests
├── .gitignore
├── main.py                     # Command-line entry point
├── dashboard.py                # Interactive Streamlit dashboard
├── README.md
└── requirements.txt
```

## Installation

Python 3.10 or later is recommended. From the project root:

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python` for the install/run commands. If the Windows `pip` launcher reports that it cannot upgrade itself, run `python -m pip install --upgrade pip`, then install requirements with `pip install -r requirements.txt`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` file installs the analysis libraries, Plotly, and Streamlit. Activate the environment before launching commands so the project uses its isolated packages.

## Run the project

The first run creates `data/expenses.csv` with synthetic data if it does not exist:

```bash
python main.py
```

Regenerate demo data, or choose another row count and deterministic seed:

```bash
python main.py --generate-sample --sample-rows 150 --seed 7
```

Analyze a custom CSV and optionally check a monthly budget:

```bash
python main.py --input data/my_expenses.csv --monthly-budget 25000
```

Use `python main.py --help` to see all options. Required CSV columns and invalid-row rules are documented in [docs/data_dictionary.md](docs/data_dictionary.md).

### Executive dashboard

Start the interactive dashboard from the activated virtual environment:

```bash
streamlit run dashboard.py
```

The dashboard provides responsive KPI cards, date/category/payment filters, monthly/category/payment/daily charts, executive highlights, a monthly category matrix, and a filtered CSV download. It defaults to INR display and allows selection of USD/EUR/GBP formatting; that selector changes number formatting only, not the underlying currency or values. Upload a different CSV using the sidebar file uploader. The dashboard generates synthetic default data if `data/expenses.csv` does not yet exist.

The presentation uses a high-contrast light palette, consistent sans-serif type, responsive panels, and direct budget context. See the [detailed project report](reports/project_report.md) for scope, assumptions, privacy considerations, validation, and future production requirements. This student portfolio prototype is not a production finance or accounting system.

### Expected output

Terminal output reports rows read/kept/removed, transaction count, total spend, average daily spend, highest category, latest-month total, and output paths. The actual totals depend on the generated dates and the run date.

Generated files:

```text
outputs/
├── charts/
│   ├── category_spending.png
│   ├── monthly_spending.png
│   ├── payment_method_spending.png
│   └── daily_spending.png
└── reports/
    ├── category_summary.csv
    ├── monthly_summary.csv
    ├── payment_method_summary.csv
    ├── daily_summary.csv
    └── summary_report.txt
```

Sample insight format: “Highest spending category: Food (…); latest month (YYYY-MM): …; average daily spending: …”. The tracker only flags overspending when `--monthly-budget` is supplied.

### Test

```bash
python -m unittest discover -s tests -v
```

## Virtual simulation

1. The generator creates fictional dated purchases with categories, amounts, payment methods, and descriptions; use `--seed` to repeat the same records.
2. Cleaning parses dates/numbers, trims text, and reports invalid rows removed.
3. Grouping sums amounts by category/month/payment/day. Month totals expose trend changes; daily totals show days with recorded expenses.
4. To identify overspending, compare the latest month with `--monthly-budget`; without a budget, the program deliberately makes no over-budget claim.
5. The program saves charts and a text/CSV report for review and sharing.

For a portfolio, capture the terminal, open each PNG, and inspect `summary_report.txt`. Put screenshots you create in `images/`; the `outputs/` folder is ignored by Git, so selectively copy non-sensitive final charts/reports into `images/` or `reports/` if you want to commit them. Never publish real personal transactions.

## Build plan and proof of work

| Day / phase | Work and why | Expected output / commit idea | Common beginner mistakes |
|---|---|---|---|
| 1 — Setup & folders | Create the virtual environment, install dependencies, and add project folders so work is reproducible. | `chore: set up expense tracker project`; screenshot folder tree. | Installing outside the venv; committing `.venv/`. |
| 2 — Dataset | Define the five-column CSV and generate fictional sample records. | `feat: add reproducible synthetic expense data`; screenshot CSV preview. | Inconsistent columns, dates, or currency; confusing real and synthetic data. |
| 3 — Cleaning & analysis | Parse dates and amounts, handle invalid rows, calculate category/month/day/payment metrics. | `feat: clean and summarize expense data`; capture terminal summary. | Summing text, silently keeping invalid rows, off-by-one date averages. |
| 4 — Category chart | Create and review the category bar chart. | `feat: visualize category spending`; capture bar chart. | Unsorted bars, missing labels, unreadable text. |
| 5 — Trends | Add monthly and daily lines plus payment-method chart. | `feat: add monthly daily and payment charts`; capture all charts. | Treating missing dates as zero without explaining it; pie chart for too many groups. |
| 6 — Reports & GitHub docs | Generate summaries, add README/data dictionary, run tests, and curate safe screenshots. | `docs: document usage and portfolio outputs`; capture report and repository. | Uploading private data, generated clutter, or secrets. |

Suggested professional commit messages:

```text
chore: initialize expense tracker project
feat: generate reproducible synthetic expenses
feat: clean and analyze CSV expense data
feat: add spending visualizations
feat: export summaries and budget insights
test: cover cleaning and expense metrics
docs: add setup guide and portfolio documentation
```

## Screenshots and portfolio outputs

Capture these after running the project:

1. Project folder tree in VS Code/File Explorer.
2. `data/expenses.csv` opened as a table (synthetic data only).
3. Terminal run showing cleaning and summary metrics.
4. `outputs/charts/category_spending.png`.
5. `outputs/charts/monthly_spending.png`.
6. `outputs/charts/payment_method_spending.png`.
7. `outputs/charts/daily_spending.png`.
8. `outputs/reports/summary_report.txt`.
9. GitHub repository landing page with README and curated images.

Use readable crops, avoid exposing your Windows username or private filesystem paths, and save selected images under `images/`. GitHub cannot capture screenshots for you; capture them locally after running the code.

## GitHub upload

1. Create a public GitHub repository named **`personal-expense-tracker-visualization`**. Description: “A Python and pandas project that analyzes synthetic or manually entered expenses and exports spending charts and reports.” Suggested topics: `python`, `pandas`, `data-analysis`, `data-visualization`, `matplotlib`, `seaborn`, `personal-finance`, `beginner-project`.
2. In the project folder, initialize and push (replace the URL with your repository URL):

```bash
git init
git add .
git commit -m "chore: initialize expense tracker project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/personal-expense-tracker-visualization.git
git push -u origin main
```

3. For later work, run `git add <specific-files>`, `git commit -m "feat: describe the change"`, and `git push`. Review `git status` before each commit. The provided `.gitignore` excludes virtual environments, generated output, and the default data CSV; add only synthetic sample rows if you intentionally want a committed data preview.
4. Upload chosen screenshots to `images/` and link them in this README after they exist. Add curated reports only if they contain synthetic or anonymized data.

## Learning outcomes and industry relevance

- Python modules, functions, CLI arguments, and filesystem paths.
- CSV ingestion, type conversion, validation, and data-quality accounting.
- pandas grouping and NumPy-based reproducible synthetic data.
- Matplotlib/Seaborn chart design and automated file output.
- Report generation, unit tests, Git, and documentation.
- A foundation that can be extended with a Streamlit dashboard, database, budget settings, or automated CI.

## Interview preparation

1. **Explain your project.**  
   “I built a Python expense-analysis tool that reads a structured CSV or creates reproducible synthetic data. It validates and cleans dates, amounts, and text; calculates spending by category, month, day, and payment method; and exports four visualizations plus CSV and text reports. It can compare the latest month against a user-provided budget. It is local-only and does not connect to financial accounts.”

2. **Why did you use pandas?**  
   “Pandas provides convenient CSV loading, type conversion, missing-value handling, and group-by aggregations. That keeps the analysis readable and makes it easy to export summary tables.”

3. **How do you clean the data?**  
   “I check for required columns, parse dates and numeric amounts, trim labels, and remove records with invalid dates, non-positive amounts, or blank category/payment method. I print kept and removed counts rather than hiding data quality issues.”

4. **How is monthly spending calculated?**  
   “Each valid date is converted to a year-month period. I group by that month and sum the amount, while also counting transactions.”

5. **How do you calculate average daily spending?**  
   “I divide total spending by the inclusive number of calendar days between the earliest and latest valid dates. This treats dates without recorded purchases as days in the observed period.”

6. **How do you handle overspending?**  
   “There is no assumed budget. If the user passes a positive `--monthly-budget`, I compare it with spending in the latest month represented in the data and report the difference.”

7. **Why use synthetic data?**  
   “It lets anyone run and test the project without banking access and avoids sharing sensitive transactions. A fixed random seed makes generated examples reproducible.”

8. **How would you make this production-ready?**  
   “I would add stricter schemas and currency handling, configurable category/budget rules, persistent storage with migrations, authentication and privacy controls for a hosted app, logging, broader tests, and automated CI. I would not store banking credentials in this tool.”

9. **How did you test the project?**  
   “The unit tests cover deterministic sample generation, invalid-row cleaning and text normalization, plus key totals, highest category, month selection, and daily-average calculations.”

10. **What would you improve next?**  
    “I would add a Streamlit dashboard with date/category filters, user-managed budgets, and downloadable reports, while keeping the analysis functions reusable and adding tests for those features.”

### HR explanation

“This project shows that I can take an unstructured everyday problem and turn it into a documented, testable Python workflow. I chose synthetic/sample CSV data to protect privacy, and I can explain the design decisions, limitations, and next steps.”

### Technical explanation

“The CLI calls reusable functions in `src/expense_tracker.py`. The loader validates required columns and cleans typed values. The analysis layer returns pandas aggregates for category, month, payment method, and day, plus derived metrics. The visualization/report layers consume those results and write PNG, CSV, and text artifacts. Unit tests verify core data and metric behavior.”
