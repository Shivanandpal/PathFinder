from fastapi import FastAPI
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "data", "roles_data.json")

with open(data_path) as f:
    roles_data = json.load(f)

# Request model
class UserInput(BaseModel):
    degree: str
    skills: str
    year: str
    role: str = None   # ✅ ADD THIS LINE

# Matching logic
def match_role(user_skills):
    user_skills = [s.strip().lower() for s in user_skills.split(",")]

    best_role = None
    max_match = 0

    for role, data in roles_data.items():
        required = [s.lower() for s in data["skills_required"]]
        match = len(set(user_skills) & set(required))

        if match > max_match:
            max_match = match
            best_role = role

    return best_role, max_match

# API endpoint
@app.post("/analyze")
def analyze(user: UserInput):

    # ✅ If user selected a role → use it
    if user.role and user.role in roles_data:
        role = user.role
        data = roles_data[role]

        user_skills = [s.strip().lower() for s in user.skills.split(",")]
        required = [s.lower() for s in data["skills_required"]]

        score = len(set(user_skills) & set(required))

    # ✅ Otherwise → auto match
    else:
        role, score = match_role(user.skills)

        if not role:
            return {"error": "No match found"}

        data = roles_data[role]
    user_skills_list=[s.strip().lower() for s in user.skills.split(",")]
    missing = [
        s for s in data["skills_required"]
        if s.lower() not in user.skills.lower()
    ]

    readiness = int((score / len(data["skills_required"])) * 100)

    return {
        "role": role,
        "readiness": readiness,
        "missing_skills": missing,
        "projects": data.get("projects", []),
        "career_path": data.get("career_path", []),
        "resources": data["resources"]
    }