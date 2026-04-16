import pandas as pd
import json

# -----------------------------
# 🧠 Skill Normalization Map
# -----------------------------
SKILL_MAP = {
    "python basics": "Python",
    "advanced python": "Python",
    "java basics": "Java",
    "c++ basics": "C++",
    "javascript basics": "JavaScript",
    "sql basics": "SQL"
}

# ❌ Remove these (noise skills)
REMOVE_SKILLS = [
    "communication", "teamwork", "problem-solving",
    "creativity", "collaboration", "leadership"
]

# -----------------------------
# 🧠 Project Templates
# -----------------------------
PROJECTS_DB = {
    "Backend Developer": [
        {
            "level": "Beginner",
            "name": "REST API Project",
            "features": ["CRUD operations", "Database connection", "Basic authentication"]
        },
        {
            "level": "Intermediate",
            "name": "Blog API",
            "features": ["User login", "JWT auth", "Post management"]
        }
    ],

    "AI Engineer": [
        {
            "level": "Beginner",
            "name": "ML Model",
            "features": ["Data preprocessing", "Train model", "Accuracy check"]
        },
        {
            "level": "Intermediate",
            "name": "AI Chatbot",
            "features": ["NLP processing", "Intent detection", "Response system"]
        }
    ],

    "Android Developer": [
        {
            "level": "Beginner",
            "name": "Notes App",
            "features": ["Add/Delete notes", "Local storage", "Simple UI"]
        },
        {
            "level": "Intermediate",
            "name": "API App",
            "features": ["API integration", "RecyclerView", "Navigation"]
        }
    ]
}

# -----------------------------
# 🎓 Learning Resources
# -----------------------------
COURSES_DB = {
    "Backend Developer": {
        "free": [
            "https://www.youtube.com/watch?v=Oe421EPjeBE"
        ],
        "paid": [
            "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/"
        ]
    },

    "AI Engineer": {
        "free": [
            "https://www.youtube.com/watch?v=7eh4d6sabA0"
        ],
        "paid": [
            "https://www.coursera.org/professional-certificates/ai-engineer"
        ]
    },

    "Android Developer": {
        "free": [
            "https://www.youtube.com/watch?v=fis26HvvDII"
        ],
        "paid": [
            "https://www.udemy.com/course/android-kotlin-developer/"
        ]
    }
}

# -----------------------------
# 🧹 Clean Skills Function
# -----------------------------
def clean_skills(skill_string):
    skills = skill_string.split(";")
    cleaned = []

    for skill in skills:
        s = skill.strip().lower()

        if s in REMOVE_SKILLS:
            continue

        if s in SKILL_MAP:
            s = SKILL_MAP[s]

        else:
            s = s.title()

        cleaned.append(s)

    return list(set(cleaned))


# -----------------------------
# 🚀 Main Processing
# -----------------------------
def process_dataset(input_file, output_file):
    df = pd.read_csv(input_file)

    roles_data = {}

    for _, row in df.iterrows():
        role = str(row["Title"]).strip()

        # 👉 Keep only fresher roles
        if "Fresher" not in str(row["ExperienceLevel"]):
            continue

        skills = clean_skills(str(row["Skills"]))

        # Normalize role names
        role_key = role.split("-")[0].strip()

        if role_key not in roles_data:
            roles_data[role_key] = {
                "skills_required": [],
                "projects": PROJECTS_DB.get(role_key, []),
                "resources": COURSES_DB.get(role_key, {
                    "free": [],
                    "paid": []
                })
            }

        # Merge skills
        existing = set(roles_data[role_key]["skills_required"])
        roles_data[role_key]["skills_required"] = list(existing.union(skills))

    # Save JSON
    with open(output_file, "w") as f:
        json.dump(roles_data, f, indent=4)

    print("✅ Data cleaned and enriched successfully!")


# -----------------------------
# ▶️ Run Script
# -----------------------------
if __name__ == "__main__":
    process_dataset("job_dataset.csv", "data/roles_and_data.json")