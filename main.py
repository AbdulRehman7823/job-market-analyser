import pandas as pd

# Sample job data - we will replace this with real API data later
jobs = [
    {"title": "Data Engineer", "company": "TechCorp", "location": "Manchester", "salary": 32000, "skills": "Python, SQL"},
    {"title": "Junior Data Analyst", "company": "DataCo", "location": "Remote", "salary": 28000, "skills": "SQL, Excel"},
    {"title": "Python Developer", "company": "SoftwareInc", "location": "London", "salary": 35000, "skills": "Python, Django"},
    {"title": "Data Engineer", "company": "CloudBase", "location": "Remote", "salary": 30000, "skills": "Python, AWS"},
    {"title": "Analytics Engineer", "company": "InsightLtd", "location": "Manchester", "salary": 31000, "skills": "SQL, dbt"},
    {"title": "Junior Data Engineer", "company": "StartupXYZ", "location": "Remote", "salary": 27000, "skills": "Python, SQL"},
]

# Turn it into a DataFrame - this is Pandas
df = pd.DataFrame(jobs)

print("=== ALL JOBS ===")
print(df)

print("\n=== AVERAGE SALARY BY JOB TITLE ===")
print(df.groupby("title")["salary"].mean())

print("\n=== REMOTE JOBS ONLY ===")
remote = df[df["location"] == "Remote"]
print(remote[["title", "company", "salary"]])

print("\n=== HIGHEST PAYING JOB ===")
print(df.loc[df["salary"].idxmax()])