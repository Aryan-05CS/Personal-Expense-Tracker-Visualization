# Project Report: Personal Expense Tracker with Executive Dashboard

**Project type:** Python data analysis and visualization  
**Primary audience:** Student portfolio demonstration; executive-style dashboard presentation  
**Data source:** User-provided or reproducible synthetic CSV  
**Status:** Local-first prototype; does not connect to banking systems

## 1. Executive summary

This project provides a repeatable workflow for turning expense records into management-friendly summaries. A Python command-line tool and a Streamlit dashboard read a CSV, validate its required fields, clean invalid rows, calculate spending metrics, and present category, monthly, payment-method, and daily patterns. The dashboard adds interactive date/category/payment filters, selectable display currency, optional monthly budget comparison, and downloadable filtered records.

The visual design uses a calm, high-contrast palette, readable typography, flexible layout, and labeled charts to make key information legible at a glance. All data processing is local. The project is suitable as a learning and portfolio artifact; it has not been security-reviewed or validated as a regulated finance product and should not be represented as a production corporate finance system.

## 2. Business problem and objectives

Expense records can be hard to interpret when they are scattered across notes or spreadsheets. The project aims to:

1. Consolidate structured expenses in a simple CSV workflow.
2. Reveal where spending is concentrated and how it changes over time.
3. Give users a simple comparison to a monthly spending target when one is provided.
4. Export visual and tabular summaries for review.
5. Demonstrate data preparation, analytics, visualization, testing, and documentation in Python.

### Intended users and value

- **Individuals and families:** review spending mix and monthly patterns.
- **Students and employees:** practice budgeting with a clear summary.
- **Freelancers and small-business learners:** explore expense categorization concepts using non-sensitive sample data.
- **Analysts and reviewers:** inspect the transformations and reproduce outputs.

The tool is not an accounting, tax, investment, or financial-advice system.

## 3. Scope and requirements

### In scope

- Five-field CSV input: `date`, `category`, `amount`, `payment_method`, and `description`.
- Synthetic data generation with deterministic random seed support.
- Date/amount parsing, text cleanup, invalid-row exclusion, and visible row counts.
- Aggregation by category, calendar month, payment method, and date.
- Total spend, highest category, average daily spend, latest-month total, and optional budget comparison.
- Static CLI chart/report generation and interactive local dashboard.
- Dashboard filters and CSV download.

### Out of scope

- Banking integration, credential storage, automated transaction imports.
- Multi-currency conversion, household/user identity management, or shared access.
- Accounting ledger, reconciliations, taxes, investment advice, or verified corporate reporting.
- Hosted deployment, authentication, authorization, encrypted database, or audit trail.

## 4. Architecture

```text
Synthetic generator or user CSV
              |
              v
 CSV schema check and data cleaning
              |
              v
 pandas grouped analytics and metrics
         /                 \
        v                   v
 CLI chart/report export   Streamlit interactive view
        |                   |
        +------ PNG/CSV/text + filtered CSV download
```

### Components

- `src/expense_tracker.py`: synthetic data, input cleaning, aggregations, Matplotlib/Seaborn visualizations, and text/CSV reporting.
- `main.py`: CLI options and batch workflow.
- `dashboard.py`: Streamlit interface, filters, Plotly charts, KPI cards, data table, and export action.
- `.streamlit/config.toml`: light brand theme and chart palette.
- `tests/test_expense_tracker.py`: focused unit tests for deterministic input, cleaning, and key metrics.

## 5. Data and assumptions

Each input file is expected to contain a single currency with positive numeric amounts. The application does not infer a currency or convert between currencies. The dashboard currency selector only formats displayed values; it does not convert amounts.

Rows with an unparseable date, missing/non-numeric/non-positive amount, or empty category/payment method are excluded from analysis and included in a visible cleaning count. Description may be blank. Category and payment labels are trimmed and title-cased.

Average daily spending is total spending divided by inclusive calendar days between the first and last selected valid expense. The daily chart displays days with transactions, not inserted zero-spend dates. Monthly budget comparison is only enabled when the user explicitly enters a positive budget and compares the latest calendar month represented after filters.

## 6. Dashboard design and usability

The dashboard follows an executive-summary hierarchy:

1. **Context:** report title, date coverage, and data-quality counts.
2. **At-a-glance KPIs:** selected-period spending, latest month, transaction count, and average daily spend.
3. **Trend and composition:** monthly spend, ranked category totals, payment method mix, and daily spend.
4. **Decision support:** concise highlights, monthly category matrix, optional budget status.
5. **Drill-down:** expandable filtered transactions and CSV download.

The light theme uses deep navy text (`#17324D`), blue primary (`#2878B5`), teal (`#26A69A`), amber accents, pale background, white panels, and subtle borders. System sans-serif font fallbacks are used for compatibility; the layout uses responsive columns, scalable heading sizes, and readable chart labels. Filters live in the sidebar and apply consistently across KPIs and charts.

## 7. Implementation and runbook

### Environment setup — Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

If the Windows `pip` launcher says it cannot upgrade itself, use `python -m pip install --upgrade pip` for that upgrade step, then continue with `pip install -r requirements.txt`.

### Generate demo data and run the CLI

```powershell
python main.py --generate-sample --sample-rows 120 --seed 42
```

### Launch the dashboard

```powershell
streamlit run dashboard.py
```

Open the local URL printed by Streamlit. The dashboard creates its synthetic default CSV if one is not already present. To analyze a different dataset in the web view, upload a CSV with the required fields in the sidebar.

### Run tests

```powershell
python -m unittest discover -s tests -v
```

### Outputs

- `outputs/charts/`: four static PNGs from the CLI.
- `outputs/reports/`: category, month, payment, and daily summaries plus `summary_report.txt`.
- Dashboard: interactive charts/table and a filtered CSV download.

Generated data and outputs are not intended to be committed by default; inspect `.gitignore` before adding any generated artifacts. Commit only synthetic/anonymized data and screenshots.

## 8. Validation and quality

Focused unit tests cover deterministic synthetic generation, invalid-row removal and text normalization, total/category/month metrics, and daily average. The workflow should be checked with:

- A valid sample CSV.
- A CSV containing an invalid date and invalid amount.
- A missing required column.
- A custom CSV upload.
- Filters that return no rows.
- Budget comparison enabled and disabled.
- Narrow/mobile and desktop browser widths.

## 9. Privacy and risk considerations

- Never upload banking credentials, account identifiers, or private transaction exports to a public repository.
- Synthetic data is the recommended demo and screenshot source.
- The default dashboard is local-first, but a user who hosts or shares it must add appropriate access controls and review the hosting provider's data handling.
- CSV upload data is processed in memory for the active dashboard session; users should still avoid untrusted files and private datasets on shared machines.
- Display-currency selection changes formatting only. It does not change numeric values or perform conversion.
- Synthetic numbers must not be presented as company financial results.

## 10. Limitations and future enhancements

1. Add explicit schema validation, configurable categories, and duplicate detection.
2. Store currency as structured metadata and validate currency consistency.
3. Add budgets per category and compare equivalent complete periods.
4. Add safe synthetic sample records checked into the repository.
5. Improve dashboard accessibility validation (keyboard, contrast, screen readers) and add visual regression tests.
6. Add broader tests for dashboard filters and exports.
7. For real organization use, introduce authentication, role-based access, encryption, data retention controls, audit logs, secure storage, and a formal privacy/security review before deployment.
8. Add CI and a deployment guide after the target hosting environment and security requirements are selected.

## 11. Conclusion

The project combines a transparent pandas analysis pipeline with a responsive executive-style dashboard. It is intentionally designed as an educational, local-first prototype with reproducible data and visible assumptions. It demonstrates transferable analytics and software-engineering skills while clearly identifying what would be required before handling actual organizational finance data.
