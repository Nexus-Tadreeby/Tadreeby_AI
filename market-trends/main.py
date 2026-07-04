from fastapi import FastAPI
from collections import Counter

app = FastAPI(
    title="Market Trends API",
    description="Analyze students and opportunities skills trends",
    version="1.0"
)

def extract_skills(items, key):

    skills = []

    for item in items:

        value = item.get(key, "")

        if isinstance(value, list):
            skills.extend([v.lower() for v in value])

        else:
            skills.extend([
                s.strip().lower()
                for s in value.split(";")
                if s.strip()
            ])

    return skills


def categorize(skills_list):

    counts = Counter(skills_list)

    sorted_skills = [
        skill for skill, _ in counts.most_common()
    ]

    result = {
        "high": [],
        "medium": [],
        "low": []
    }

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



@app.get("/")
def home():

    return {
        "message": "Market Trends API is running"
    }



@app.post("/ai/market-trend")
def market_trends(data: dict):

    students = data.get("students", [])
    opportunities = data.get("opportunities", [])

    student_skills = extract_skills(
        students,
        "skills"
    )

    opportunity_skills = extract_skills(
        opportunities,
        "requiredSkills"
    )

    return {
        "student_skills_trends":
            categorize(student_skills),

        "opportunity_skills_trends":
            categorize(opportunity_skills)
    }