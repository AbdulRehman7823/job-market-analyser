import pandas as pd
import sqlite3

# Load CSV into a real SQLite database
df = pd.read_csv("jobs.csv")

# Create a database connection
conn = sqlite3.connect("jobs.db")

# Save dataframe as a SQL table
df.to_sql("jobs", conn, if_exists="replace", index=False)

print("✅ Database created")
print("Now writing SQL queries...\n")

# ── QUERY 1 ─────────────────────────────────────────────
# Average salary by job type - classic GROUP BY
query1 = """
SELECT 
    search_keyword,
    COUNT(*) as total_jobs,
    ROUND(AVG(avgSalary), 0) as avg_salary,
    ROUND(MIN(avgSalary), 0) as min_salary,
    ROUND(MAX(avgSalary), 0) as max_salary
FROM jobs
WHERE avgSalary > 0
GROUP BY search_keyword
ORDER BY avg_salary DESC
"""

print("=== QUERY 1: Salary breakdown by job type ===")
print(pd.read_sql(query1, conn))

# ── QUERY 2 ─────────────────────────────────────────────
# Top paying companies - who should you apply to first?
query2 = """
SELECT 
    employerName,
    COUNT(*) as jobs_posted,
    ROUND(AVG(avgSalary), 0) as avg_salary
FROM jobs
WHERE avgSalary > 0
GROUP BY employerName
HAVING COUNT(*) >= 1
ORDER BY avg_salary DESC
LIMIT 10
"""

print("\n=== QUERY 2: Top paying companies ===")
print(pd.read_sql(query2, conn))

# ── QUERY 3 ─────────────────────────────────────────────
# Salary ranges - what bracket has the most jobs?
query3 = """
SELECT 
    CASE 
        WHEN avgSalary = 0 THEN 'Not disclosed'
        WHEN avgSalary < 30000 THEN 'Under £30k'
        WHEN avgSalary < 40000 THEN '£30k - £40k'
        WHEN avgSalary < 50000 THEN '£40k - £50k'
        WHEN avgSalary < 60000 THEN '£50k - £60k'
        ELSE 'Above £60k'
    END as salary_bracket,
    COUNT(*) as total_jobs
FROM jobs
GROUP BY salary_bracket
ORDER BY total_jobs DESC
"""

print("\n=== QUERY 3: Jobs by salary bracket ===")
print(pd.read_sql(query3, conn))

conn.close()