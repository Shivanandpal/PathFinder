import pandas as pd
import json

# Load CSV
df = pd.read_csv("jobs.csv")

roles_data = {}

for _, row in df.iterrows():
    role = row["job_title"]

    skills = str(row["skills"]).split(",")
    skills = [s.strip() for s in skills if s.strip()]

    if role not in roles_data:
        roles_data[role] = {
            "skills_required": list(set(skills)),
            "projects": [],
            "resources": {
                "free": [],
                "paid": []
            }
        }
    else:
        existing = set(roles_data[role]["skills_required"])
        roles_data[role]["skills_required"] = list(existing.union(skills))


# Save JSON
with open("data/roles_data.json", "w") as f:
    json.dump(roles_data, f, indent=4)

print("✅ Kaggle data converted!")