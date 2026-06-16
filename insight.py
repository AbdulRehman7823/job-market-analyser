import pandas as pd


df = pd.read_csv("jobs.csv")

print("Enter a keyword")
keyword = input()

filtered = df[df["jobTitle"].str.contains(keyword, case=False, na=False)]

print("Total jobs found",len(filtered))
filtered = filtered[filtered["avgSalary"] > 0]

avg = filtered["avgSalary"].mean()
print(f"Average Salary: £{avg:,.0f}")
print("Highest paying job and company",filtered.nlargest(1, "avgSalary")[["jobTitle", "employerName", "avgSalary"]])
print("Lowest paying job and company",filtered.nsmallest(1, "avgSalary")[["jobTitle", "employerName", "avgSalary"]])

save = input("\nDo you want to save results to filtered_jobs.csv? (yes/no): ")
if save.lower() == "yes":
    filtered.to_csv("filtered_jobs.csv", index=False)
    print("✅ Saved to filtered_jobs.csv")
else:
    print("Okay, exiting. Goodbye!")