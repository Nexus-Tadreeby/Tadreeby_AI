from fastapi import FastAPI
from collections import Counter

app = FastAPI()

def extract_skills(items, key):
    skills = []
    for item in items:
        skills.extend([
            s.strip().lower()
            for s in item.get(key, "").split(";")
            if s.strip()
        ])
    return skills


def categorize(skills_list):
    counts = Counter(skills_list)
    sorted_skills = [skill for skill, _ in counts.most_common()]

    result = {"high": [], "medium": [], "low": []}

    total = len(sorted_skills)

    if total == 0:
        return result

    for i, skill in enumerate(sorted_skills):
        if i < total * 0.2:
            result["high"].append(skill)
        elif i < total * 0.6:
            result["medium"].append(skill)
        else:
            result["low"].append(skill)

    return result


@app.post("/market-trends")
def market_trends(data: dict):

    students = data.get("students", [])
    opportunities = data.get("opportunities", [])

    return {
        "student_skills_trends": categorize(extract_skills(students, "skills")),
        "opportunity_skills_trends": categorize(extract_skills(opportunities, "requiredSkills"))
    }