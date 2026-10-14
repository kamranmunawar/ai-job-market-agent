
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from skill_market_analyzer import SkillMarketAnalyzer


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "jobs.db"

st.set_page_config(
    page_title="UK AI Job Market",
    page_icon="📊",
    layout="wide",
)

st.title("UK AI Job Market Intelligence")
st.caption(
    "Technical skills extracted from UK AI vacancies "
    "using Adzuna, employer-page matching and Ollama."
)


@st.cache_data
def load_analysis(db_path: str, db_mtime: float):
    analyzer = SkillMarketAnalyzer(db_path)
    return analyzer.analyze()


@st.cache_data
def load_status_counts(db_path: str, db_mtime: float):
    with sqlite3.connect(db_path) as conn:
        return dict(
            conn.execute(
                """
                SELECT processing_status, COUNT(*)
                FROM jobs
                GROUP BY processing_status
                """
            ).fetchall()
        )


if not DB_PATH.exists():
    st.error(f"Database not found: {DB_PATH}")
    st.stop()

db_mtime = DB_PATH.stat().st_mtime

analysis = load_analysis(str(DB_PATH), db_mtime)
status_counts = load_status_counts(str(DB_PATH), db_mtime)

completed = analysis["completed_jobs"]
total = sum(status_counts.values())
needs_review = status_counts.get("needs_review", 0)
failed = status_counts.get("failed", 0)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total vacancies", total)
col2.metric("Analysed", completed)
col3.metric("Needs review", needs_review)
col4.metric(
    "Completion rate",
    f"{completed / total:.1%}" if total else "0%",
)

st.divider()

categories = sorted(analysis["by_category"])

selected_category = st.selectbox(
    "Job category",
    ["All categories"] + categories,
)

top_n = st.slider(
    "Number of skills",
    min_value=5,
    max_value=30,
    value=15,
    step=5,
)

if selected_category == "All categories":
    skill_counts = analysis["overall"]
    denominator = completed
else:
    skill_counts = analysis["by_category"][selected_category]
    denominator = analysis["category_job_counts"][
        selected_category
    ]

records = [
    {
        "Skill": skill,
        "Vacancies": count,
        "Demand (%)": (
            round(100 * count / denominator, 1)
            if denominator
            else 0
        ),
    }
    for skill, count in skill_counts.most_common()
]

df = pd.DataFrame(
    records,
    columns=["Skill", "Vacancies", "Demand (%)"],
)

st.subheader("Most requested skills")

if df.empty:
    st.info("No extracted skills available.")
else:
    chart_df = df.head(top_n).set_index("Skill")

    st.bar_chart(
        chart_df["Demand (%)"],
        horizontal=True,
        x_label="Percentage of analysed vacancies",
        y_label="Skill",
    )

    st.dataframe(
        df.head(top_n),
        hide_index=True,
        use_container_width=True,
    )

    st.download_button(
        "Download skills CSV",
        data=df.to_csv(index=False),
        file_name="ai_job_skills.csv",
        mime="text/csv",
    )

st.divider()

st.subheader("Coverage by job category")

coverage_records = [
    {
        "Category": category,
        "Analysed vacancies": count,
    }
    for category, count in sorted(
        analysis["category_job_counts"].items()
    )
]

coverage_df = pd.DataFrame(coverage_records)

st.dataframe(
    coverage_df,
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "A vacancy can belong to multiple search categories. "
    "Demand percentages use successfully analysed vacancies "
    "in the selected category as their denominator. "
    "These results are exploratory and do not represent "
    "the entire UK AI labour market."
)
