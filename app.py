import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Career Opportunity Radar",
    layout="wide"
)

st.title("📊 Career Opportunity Radar — Singapore Job Market")

# ---------------------------------------------------
# Load Data (Parquet via DuckDB)
# ---------------------------------------------------

@st.cache_resource
def get_connection():
    return duckdb.connect()

@st.cache_data
def get_months():
    con = get_connection()
    query = """
        SELECT DISTINCT month
        FROM read_parquet('SGJobData_enhanced.parquet')
        WHERE month IS NOT NULL
        ORDER BY month
    """
    return con.execute(query).df()["month"].tolist()

@st.cache_data
def get_position_levels():
    con = get_connection()
    query = """
        SELECT DISTINCT positionLevels
        FROM read_parquet('SGJobData_enhanced.parquet')
        WHERE positionLevels IS NOT NULL
        ORDER BY positionLevels
    """
    return con.execute(query).df()["positionLevels"].tolist()

@st.cache_data
def get_sectors():
    con = get_connection()
    query = """
        SELECT DISTINCT sector
        FROM read_parquet('SGJobData_enhanced.parquet')
        WHERE sector IS NOT NULL
        ORDER BY sector
    """
    return con.execute(query).df()["sector"].tolist()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("Filters")

months = get_months()
month_range = st.sidebar.select_slider(
    "Month Range",
    options=months,
    value=(months[0], months[-1])
)

position_levels = get_position_levels()
selected_levels = st.sidebar.multiselect(
    "Position Level",
    options=position_levels,
    default=position_levels
)

sectors = get_sectors()
selected_sectors = st.sidebar.multiselect(
    "Sector",
    options=sectors,
    default=sectors
)

min_postings = st.sidebar.slider(
    "Minimum Postings per Sector",
    min_value=1,
    max_value=500,
    value=30
)

# ---------------------------------------------------
# Query Aggregated Data
# ---------------------------------------------------

con = get_connection()

query = f"""
SELECT
    sector,
    COUNT(*) AS postings,
    MEDIAN(salary_mid) AS median_salary,
    SUM(applications) / COUNT(*) AS applications_per_posting
FROM read_parquet('SGJobData_enhanced.parquet')
WHERE month BETWEEN '{month_range[0]}' AND '{month_range[1]}'
AND positionLevels IN ({",".join([f"'{lvl}'" for lvl in selected_levels])})
AND sector IN ({",".join([f"'{sec}'" for sec in selected_sectors])})
AND salary_is_valid = TRUE
GROUP BY sector
HAVING COUNT(*) >= {min_postings}
ORDER BY postings DESC
"""

df = con.execute(query).df()

# ---------------------------------------------------
# Radar Bubble Chart
# ---------------------------------------------------

st.subheader("Career Opportunity Radar")

fig = px.scatter(
    df,
    x="postings",
    y="median_salary",
    size="applications_per_posting",
    color="median_salary",
    hover_name="sector",
    labels={
        "postings": "Demand (Number of Postings)",
        "median_salary": "Median Monthly Salary",
        "applications_per_posting": "Competition (Applications per Posting)"
    }
)

fig.update_layout(height=650)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Ranked Table
# ---------------------------------------------------

st.subheader("Sector Ranking (Filtered)")

df_sorted = df.sort_values(
    by=["postings", "median_salary"],
    ascending=[False, False]
)

st.dataframe(df_sorted, use_container_width=True)

# ---------------------------------------------------
# Insight Guide
# ---------------------------------------------------

st.markdown("""
### 🔎 How to Interpret This Chart

- **Right side** → Higher demand  
- **Higher up** → Higher median salary  
- **Bigger bubbles** → More competition  

🎯 Ideal job-seeker targets:
- High demand
- Strong salary
- Moderate or manageable competition
""")