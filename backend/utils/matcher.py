import json

def load_roles():
    with open("data/roles_data.json", "r") as file:
        return json.load(file)


def match_role(user_skills, roles_data):
    user_skills = [skill.strip().lower() for skill in user_skills.split(",")]

    best_match = None
    max_match = 0

    for role, data in roles_data.items():
        required = [s.lower() for s in data["skills_required"]]
        match_count = len(set(user_skills) & set(required))

        if match_count > max_match:
            max_match = match_count
            best_match = role

    return best_match, max_match


def get_missing_skills(user_skills, required_skills):
    user_skills = [s.strip().lower() for s in user_skills.split(",")]
    return [s for s in required_skills if s.lower() not in user_skills]