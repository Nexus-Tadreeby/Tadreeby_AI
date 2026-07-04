from fastapi import FastAPI

app = FastAPI(
    title="Skill Gap Analysis API",
    description="Find missing skills + recommendations",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "message": "Hello World"
    }



def analyze_skill_gap(data: dict):

    student = set([
        s.lower()
        for s in data.get("student_skills", [])
    ])

    required = set([
        s.lower()
        for s in data.get("required_skills", [])
    ])

    missing = list(required - student)
    current = list(student & required)

    return {
        "studentId": data.get("studentId"),
        "current_skills": current,
        "missing_skills": missing,
        "recommended_courses": [
            f"{skill} course"
            for skill in missing
        ]
    }


@app.post("/skill-gap")
def skill_gap(data: dict):

    return analyze_skill_gap(data)