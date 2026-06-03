import streamlit as st
import pandas as pd
import requests
from config import API_KEY

# ── PAGE CONFIG ─────────────────────────────────────────
st.set_page_config(
    page_title="UK Job Market Analyser",
    page_icon="🇬🇧",
    layout="wide"
)

# ── FETCH DATA ──────────────────────────────────────────
@st.cache_data(ttl=3600)  # cache for 1 hour so it doesn't call API every refresh
def fetch_all_jobs():
    keywords = ["data engineer", "python developer", "data analyst"]
    cities = ["Manchester", "London", "Leeds"]
    all_jobs = []

    for keyword in keywords:
        for city in cities:
            url = "https://www.reed.co.uk/api/1.0/search"
            params = {"keywords": keyword, "locationName": city, "resultsToTake": 10}
            response = requests.get(url, auth=(API_KEY, ""), params=params)
            jobs = response.json().get("results", [])
            for job in jobs:
                job["search_keyword"] = keyword
                job["search_city"] = city
            all_jobs.extend(jobs)

    df = pd.DataFrame(all_jobs)
    df.drop_duplicates(subset="jobId", inplace=True)
    df["minimumSalary"] = df["minimumSalary"].fillna(0)
    df["maximumSalary"] = df["maximumSalary"].fillna(0)
    df["avgSalary"] = (df["minimumSalary"] + df["maximumSalary"]) / 2
    return df

# ── LOAD DATA ────────────────────────────────────────────
with st.spinner("Fetching live UK job data..."):
    df = fetch_all_jobs()

df_with_salary = df[df["avgSalary"] > 0]

# ── HEADER ───────────────────────────────────────────────
st.title("🇬🇧 UK Job Market Analyser")
st.markdown("Live data from Reed.co.uk — updated every hour")

# ── TOP METRICS ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs Found", len(df))
with col2:
    st.metric("Jobs With Salary", len(df_with_salary))
with col3:
    avg = df_with_salary["avgSalary"].mean()
    st.metric("Average Salary", f"£{avg:,.0f}")
with col4:
    top_salary = df_with_salary["avgSalary"].max()
    st.metric("Highest Salary", f"£{top_salary:,.0f}")

st.divider()

# ── FILTERS ──────────────────────────────────────────────
st.subheader("🔍 Filter Jobs")

col1, col2 = st.columns(2)

with col1:
    selected_keyword = st.selectbox(
        "Job Type",
        ["All"] + df["search_keyword"].unique().tolist()
    )

with col2:
    selected_city = st.selectbox(
        "City",
        ["All"] + df["search_city"].unique().tolist()
    )

# Apply filters
filtered = df.copy()
if selected_keyword != "All":
    filtered = filtered[filtered["search_keyword"] == selected_keyword]
if selected_city != "All":
    filtered = filtered[filtered["search_city"] == selected_city]

st.markdown(f"**{len(filtered)} jobs found**")

# ── JOB TABLE ────────────────────────────────────────────
st.subheader("📋 Job Listings")

display = filtered[[
    "jobTitle", "employerName", "locationName", "avgSalary", "jobUrl"
]].copy()

display["avgSalary"] = display["avgSalary"].apply(
    lambda x: f"£{x:,.0f}" if x > 0 else "Not disclosed"
)

display.columns = ["Job Title", "Company", "Location", "Avg Salary", "Link"]
st.dataframe(display, use_container_width=True, hide_index=True)

st.divider()

# ── CHARTS ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Average Salary by Job Type")
    salary_by_keyword = df_with_salary.groupby("search_keyword")["avgSalary"].mean()
    st.bar_chart(salary_by_keyword)

with col2:
    st.subheader("📍 Jobs Available by City")
    jobs_by_city = df["search_city"].value_counts()
    st.bar_chart(jobs_by_city)

st.divider()

# ── TOP COMPANIES ─────────────────────────────────────────
st.subheader("🏢 Top Hiring Companies")
top_companies = df["employerName"].value_counts().head(10)
st.bar_chart(top_companies)
