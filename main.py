import requests
import pandas as pd
from config import API_KEY

def fetch_jobs(keyword, location="Manchester", results_to_take=20):
    url = "https://www.reed.co.uk/api/1.0/search"
    params = {
        "keywords": keyword,
        "locationName": location,
        "resultsToTake": results_to_take
    }
    response = requests.get(url, auth=(API_KEY, ""), params=params)
    data = response.json()
    return data["results"]

# ── 1. EXTRACT ──────────────────────────────────────────
keywords = ["data engineer", "python developer", "data analyst"]
all_jobs = []

for keyword in keywords:
    print(f"Fetching: {keyword}...")
    jobs = fetch_jobs(keyword=keyword)
    for job in jobs:
        job["search_keyword"] = keyword
    all_jobs.extend(jobs)

df = pd.DataFrame(all_jobs)
df.drop_duplicates(subset="jobId", inplace=True)
print(f"\nRaw jobs fetched: {len(df)}")

# ── 2. TRANSFORM (clean the data) ───────────────────────

# Fill missing salaries with 0
df["minimumSalary"] = df["minimumSalary"].fillna(0)
df["maximumSalary"] = df["maximumSalary"].fillna(0)

# Create one average salary column
df["avgSalary"] = (df["minimumSalary"] + df["maximumSalary"]) / 2

# Clean up location names - remove postcodes, keep city names
df["locationName"] = df["locationName"].str.replace(
    r'\b[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}\b', 
    'Manchester', 
    regex=True
)

# Only keep columns we need
df = df[[
    "jobId",
    "jobTitle", 
    "employerName", 
    "locationName",
    "minimumSalary",
    "maximumSalary",
    "avgSalary",
    "jobUrl",
    "search_keyword"
]]

print(f"Clean jobs ready: {len(df)}")

# ── 3. ANALYSE ──────────────────────────────────────────

# Only analyse jobs that have salary data
df_with_salary = df[df["avgSalary"] > 0]

print(f"\n=== JOBS WITH SALARY DATA: {len(df_with_salary)} ===")

print("\n=== AVERAGE SALARY BY KEYWORD ===")
print(df_with_salary.groupby("search_keyword")["avgSalary"].mean().apply(
    lambda x: f"£{x:,.0f}"
))

print("\n=== TOP HIRING COMPANIES ===")
print(df["employerName"].value_counts().head(5))

print("\n=== HIGHEST PAYING JOBS ===")
top = df_with_salary.nlargest(5, "avgSalary")[["jobTitle", "employerName", "avgSalary"]]
top["avgSalary"] = top["avgSalary"].apply(lambda x: f"£{x:,.0f}")
print(top)

# ── 4. LOAD ─────────────────────────────────────────────
df.to_csv("jobs.csv", index=False)
print("\n✅ Clean data saved to jobs.csv")
print("\nETL Pipeline complete.")