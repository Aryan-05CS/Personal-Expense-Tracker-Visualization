"""Executive-style, interactive Streamlit dashboard for expense data."""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.expense_tracker import create_synthetic_dataset, load_and_clean_expenses

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "data" / "expenses.csv"
NAVY = "#17324D"
BLUE = "#2878B5"
TEAL = "#26A69A"
GOLD = "#E6A23C"
PALETTE = ["#2878B5", "#26A69A", "#E6A23C", "#7768AE", "#D66B5D", "#5A8F7B", "#7496C2", "#B07AA1"]
FONT = "Inter, Segoe UI, Arial, sans-serif"

st.set_page_config(
    page_title="Expense Intelligence | Executive Overview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #17324D;
        --muted: #65758B;
        --line: #E3EAF1;
        --canvas: #F4F7FB;
        --accent: #2878B5;
    }
    html, body, [class*="css"] {
        font-family: Inter, "Segoe UI", Arial, sans-serif;
        font-size: 16px;
    }
    .stApp { background: var(--canvas); }
    .block-container {
        max-width: 1540px;
        padding: 2rem clamp(1rem, 3vw, 3rem) 3rem;
    }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: var(--ink); }
    h1, h2, h3 { color: var(--ink); letter-spacing: -0.025em; }
    h1 { font-size: clamp(1.8rem, 3vw, 2.45rem) !important; }
    h2 { font-size: 1.35rem !important; }
    .eyebrow {
        color: var(--accent);
        font-size: .78rem;
        font-weight: 750;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: .35rem;
    }
    .dashboard-subtitle { color: var(--muted); font-size: 1rem; }
    .section-note { color: var(--muted); font-size: .9rem; margin-top: -.5rem; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        box-shadow: 0 2px 8px rgba(23, 50, 77, .035);
    }
    [data-testid="stMetricLabel"] p {
        color: var(--muted);
        font-size: .83rem;
        font-weight: 650;
    }
    [data-testid="stMetricValue"] {
        color: var(--ink);
        font-size: clamp(1.05rem, 1.55vw, 1.5rem);
        font-weight: 750;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border-color: var(--line);
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(23, 50, 77, .025);
    }
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        border-radius: 8px;
        font-weight: 650;
    }
    .data-quality {
        border-left: 3px solid var(--accent);
        padding: .55rem .8rem;
        background: #EEF5FA;
        border-radius: 0 8px 8px 0;
        color: var(--ink);
        font-size: .9rem;
    }
    @media (max-width: 640px) {
        .block-container { padding: 1.25rem 1rem 2rem; }
        [data-testid="stMetric"] { padding: .8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_default_data(file_path: str, modified_time: float) -> tuple[pd.DataFrame, dict[str, int]]:
    """Cache disk data until the file changes."""
    del modified_time
    return load_and_clean_expenses(Path(file_path))


def money(value: float, symbol: str) -> str:
    return f"{symbol}{value:,.2f}"


def apply_chart_style(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        font={"family": FONT, "color": NAVY, "size": 13},
        title={"font": {"size": 17, "color": NAVY}, "x": 0.02, "xanchor": "left"},
        height=height,
        margin={"l": 18, "r": 18, "t": 55, "b": 22},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hoverlabel={"bgcolor": "#17324D", "font": {"color": "#FFFFFF", "family": FONT}},
        legend={"font": {"size": 12}, "orientation": "h", "y": -0.2},
    )
    fig.update_xaxes(showgrid=False, linecolor="#E3EAF1", automargin=True)
    fig.update_yaxes(gridcolor="#E9EEF4", zerolinecolor="#E3EAF1", automargin=True)
    return fig


def render_sidebar() -> tuple[pd.DataFrame, dict[str, int], str, float | None, str]:
    st.sidebar.markdown("## Expense Intelligence")
    st.sidebar.caption("Executive spending overview")
    uploaded_file = st.sidebar.file_uploader(
        "Upload expense CSV",
        type=["csv"],
        help="Required fields: date, category, amount, payment_method, description.",
    )
    if uploaded_file is not None:
        source_label = f"Uploaded CSV: {uploaded_file.name}"
        try:
            data, cleaning = load_and_clean_expenses(io.BytesIO(uploaded_file.getvalue()))
        except (ValueError, OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
            st.sidebar.error(f"Could not use this CSV: {error}")
            st.stop()
    else:
        generated_demo = not DEFAULT_DATA.exists()
        if generated_demo:
            try:
                create_synthetic_dataset(DEFAULT_DATA)
            except OSError as error:
                st.error(f"Could not create the demo dataset: {error}")
                st.stop()
        try:
            data, cleaning = load_default_data(str(DEFAULT_DATA), DEFAULT_DATA.stat().st_mtime)
        except (ValueError, OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
            st.error(f"Could not load {DEFAULT_DATA.name}: {error}")
            st.stop()
        source_label = "Synthetic demo data" if generated_demo else f"Local CSV: {DEFAULT_DATA.name}"

    currency_options = {
        "INR — Indian Rupee (₹)": "₹",
        "USD — US Dollar ($)": "$",
        "EUR — Euro (€)": "€",
        "GBP — Pound Sterling (£)": "£",
    }
    currency_label = st.sidebar.selectbox(
        "Display currency",
        list(currency_options),
        index=0,
        help="Choose the currency already used by your CSV. This changes formatting only; no conversion is performed.",
    )

    categories = sorted(data["category"].dropna().unique().tolist())
    methods = sorted(data["payment_method"].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect("Categories", categories, default=categories)
    selected_methods = st.sidebar.multiselect("Payment methods", methods, default=methods)

    min_date = data["date"].min().date()
    max_date = data["date"].max().date()
    date_values = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Choose the reporting period to filter every KPI and chart.",
    )
    if isinstance(date_values, (tuple, list)):
        if len(date_values) == 2:
            start_date, end_date = date_values
        elif len(date_values) == 1:
            start_date = end_date = date_values[0]
        else:
            start_date, end_date = min_date, max_date
    else:
        start_date = end_date = date_values

    budget_enabled = st.sidebar.checkbox("Compare with monthly budget", value=False)
    budget = None
    if budget_enabled:
        budget = st.sidebar.number_input(
            "Monthly budget",
            min_value=1.0,
            value=50000.0,
            step=5000.0,
            help="Compared with the latest calendar month represented in the filtered data.",
        )

    filtered = data.loc[
        data["category"].isin(selected_categories)
        & data["payment_method"].isin(selected_methods)
        & data["date"].dt.date.between(start_date, end_date)
    ].copy()
    return filtered, cleaning, currency_options[currency_label], budget, source_label


def render_dashboard() -> None:
    data, cleaning, currency_symbol, monthly_budget, source_label = render_sidebar()
    st.markdown('<div class="eyebrow">Personal finance analytics</div>', unsafe_allow_html=True)
    st.title("Expense Intelligence")
    st.markdown(
        '<p class="dashboard-subtitle">A clear, decision-ready view of spend patterns, '
        "category mix, and monthly budget performance.</p>",
        unsafe_allow_html=True,
    )
    st.caption(f"Data source: {source_label} · Reporting period: {data['date'].min():%d %b %Y} – {data['date'].max():%d %b %Y}"
               if not data.empty else "No records match the selected filters.")
    st.markdown(
        f'<div class="data-quality">Source data quality: {cleaning["rows_kept"]:,} valid rows · '
        f'{cleaning["rows_removed"]:,} invalid rows excluded</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if data.empty:
        st.info("No expense records match these filters. Expand the date range or select more categories/payment methods.")
        return

    total_spend = float(data["amount"].sum())
    transaction_count = len(data)
    first_date = data["date"].min().normalize()
    last_date = data["date"].max().normalize()
    day_count = max((last_date - first_date).days + 1, 1)
    daily_average = total_spend / day_count
    category_totals = data.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
    monthly_totals = data.assign(month=data["date"].dt.to_period("M").astype(str)).groupby(
        "month", as_index=False
    ).agg(total_spending=("amount", "sum"), transaction_count=("amount", "size"))
    payment_totals = data.groupby("payment_method", as_index=False)["amount"].sum().sort_values(
        "amount", ascending=False
    )
    latest_month = monthly_totals.iloc[-1]
    latest_month_spend = float(latest_month["total_spending"])
    top_category = category_totals.iloc[0]
    category_share = float(top_category["amount"]) / total_spend if total_spend else 0

    previous_month = float(monthly_totals.iloc[-2]["total_spending"]) if len(monthly_totals) > 1 else None
    spend_delta = None
    if previous_month is not None:
        difference = latest_month_spend - previous_month
        spend_delta = f"{difference / previous_month:+.1%} vs prior month" if previous_month else None

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Spend in period", money(total_spend, currency_symbol))
    kpi2.metric(
        "Latest month",
        money(latest_month_spend, currency_symbol),
        spend_delta.replace("vs prior month", "MoM") if spend_delta else None,
    )
    kpi3.metric("Transactions", f"{transaction_count:,}")
    kpi4.metric("Daily average", money(daily_average, currency_symbol))

    st.write("")
    left, right = st.columns([1.55, 1], gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Monthly spending trend")
            st.caption("Monthly totals within the selected filters")
            fig = px.line(
                monthly_totals,
                x="month",
                y="total_spending",
                markers=True,
                color_discrete_sequence=[BLUE],
                custom_data=["transaction_count"],
            )
            fig.update_traces(
                line={"width": 3},
                marker={"size": 8, "color": TEAL, "line": {"width": 2, "color": "#FFFFFF"}},
                hovertemplate="%{x}<br>Spend: %{y:,.2f}<br>Transactions: %{customdata[0]}<extra></extra>",
            )
            fig.update_yaxes(tickprefix=currency_symbol, separatethousands=True, title="Spend")
            fig.update_xaxes(title=None)
            st.plotly_chart(apply_chart_style(fig, 350), width="stretch", config={"displaylogo": False})

    with right:
        with st.container(border=True):
            st.subheader("Spend by category")
            st.caption("Ranked category contribution")
            category_fig = px.bar(
                category_totals.sort_values("amount"),
                x="amount",
                y="category",
                orientation="h",
                color="amount",
                color_continuous_scale=["#B8D7EA", BLUE],
                labels={"amount": "Spend", "category": ""},
            )
            category_fig.update_traces(
                hovertemplate="%{y}<br>Spend: %{x:,.2f}<extra></extra>",
                marker_line_width=0,
            )
            category_fig.update_layout(coloraxis_showscale=False)
            category_fig.update_xaxes(tickprefix=currency_symbol, separatethousands=True, title="Spend")
            st.plotly_chart(apply_chart_style(category_fig, 350), width="stretch", config={"displaylogo": False})

    st.write("")
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Payment method mix")
            st.caption("Share of the selected period's spend")
            payment_fig = px.pie(
                payment_totals,
                names="payment_method",
                values="amount",
                hole=0.62,
                color_discrete_sequence=PALETTE,
            )
            payment_fig.update_traces(
                textposition="outside",
                textinfo="percent+label",
                hovertemplate="%{label}<br>Spend: " + currency_symbol + "%{value:,.2f}<br>Share: %{percent}<extra></extra>",
                marker={"line": {"color": "#FFFFFF", "width": 2}},
            )
            payment_fig.add_annotation(
                text=f"<b>{money(total_spend, currency_symbol)}</b><br><span style='font-size:11px'>total spend</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font={"family": FONT, "size": 15, "color": NAVY},
            )
            st.plotly_chart(apply_chart_style(payment_fig, 365), width="stretch", config={"displaylogo": False})

    with right:
        with st.container(border=True):
            st.subheader("Daily spending")
            st.caption("Daily totals on dates with recorded expenses")
            daily_totals = data.groupby(data["date"].dt.normalize(), as_index=False)["amount"].sum()
            daily_fig = px.area(
                daily_totals,
                x="date",
                y="amount",
                color_discrete_sequence=[TEAL],
                labels={"amount": "Spend", "date": ""},
            )
            daily_fig.update_traces(
                line={"width": 2, "color": TEAL},
                fillcolor="rgba(38, 166, 154, 0.14)",
                hovertemplate="%{x|%d %b %Y}<br>Spend: %{y:,.2f}<extra></extra>",
            )
            daily_fig.update_yaxes(tickprefix=currency_symbol, separatethousands=True, title="Daily spend")
            st.plotly_chart(apply_chart_style(daily_fig, 365), width="stretch", config={"displaylogo": False})

    st.write("")
    insight_left, insight_right = st.columns([1.3, 1], gap="large")
    with insight_left:
        with st.container(border=True):
            st.subheader("Executive highlights")
            st.markdown(
                f"- **Largest category:** {top_category['category']} at "
                f"{money(float(top_category['amount']), currency_symbol)} ({category_share:.1%} of selected spend)."
            )
            st.markdown(
                f"- **Latest month shown:** {latest_month['month']} at "
                f"{money(latest_month_spend, currency_symbol)} across "
                f"{int(latest_month['transaction_count']):,} transactions."
            )
            st.markdown(
                f"- **Average spend per calendar day:** {money(daily_average, currency_symbol)} "
                f"over {day_count:,} days between the first and last selected expense."
            )
            if monthly_budget is None:
                st.caption("Budget status is not assessed. Enable the monthly budget comparison in the sidebar to evaluate it.")
            else:
                budget_difference = latest_month_spend - monthly_budget
                if budget_difference > 0:
                    st.warning(
                        f"Latest displayed month is {money(budget_difference, currency_symbol)} "
                        f"over the {money(monthly_budget, currency_symbol)} budget."
                    )
                else:
                    st.success(
                        f"Latest displayed month is {money(abs(budget_difference), currency_symbol)} "
                        f"under the {money(monthly_budget, currency_symbol)} budget."
                    )
    with insight_right:
        with st.container(border=True):
            st.subheader("Monthly category detail")
            month_category = data.assign(month=data["date"].dt.to_period("M").astype(str)).pivot_table(
                index="month", columns="category", values="amount", aggfunc="sum", fill_value=0
            )
            st.dataframe(
                month_category.style.format(lambda value: money(value, currency_symbol)),
                width="stretch",
                height=220,
            )

    st.write("")
    with st.expander("View filtered transactions", expanded=False):
        display_data = data.sort_values("date", ascending=False).copy()
        display_data["date"] = display_data["date"].dt.strftime("%Y-%m-%d")
        display_data["amount"] = display_data["amount"].map(lambda value: money(value, currency_symbol))
        st.dataframe(display_data, width="stretch", hide_index=True)

    export_csv = data.sort_values("date").to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered records (CSV)",
        data=export_csv,
        file_name="expense_records_filtered.csv",
        mime="text/csv",
        type="primary",
    )
    st.caption(
        "Management view for analysis only. Data is supplied by the user or synthetically generated; "
        "this dashboard is not an accounting, tax, or investment system."
    )


render_dashboard()
