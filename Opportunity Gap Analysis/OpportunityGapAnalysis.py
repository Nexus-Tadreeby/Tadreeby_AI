from fastapi import FastAPI
from collections import Counter

app = FastAPI(
    title="Opportunity Gap Analysis API",
    description="Analyze demanded skills and suggest training programs",
    version="1.0"
)

@app.get("/")
def home():

    return {
        "message": "Hello World"
    }


def analyze_gap(data: dict):

    company_id = data.get("companyId")

    opportunities = data.get(
        "opportunities",
        []
    )

    all_skills = []

    for opportunity in opportunities:

        skills = opportunity.get(
            "requiredSkills",
            []
        )

        all_skills.extend([
            skill.lower()
            for skill in skills
        ])

    counts = Counter(all_skills)

    demanded_skills = [
        skill
        for skill, count
        in counts.most_common(5)
    ]

    programs = [
        f"{skill} Training Program"
        for skill in demanded_skills
    ]

    return {
        "companyId": company_id,

        "suggested_skills_in_demand":
            demanded_skills,

        "recommended_training_programs":
            programs
    }


@app.post("/opportunity-gap")
def opportunity_gap(data: dict):

    return analyze_gap(data)