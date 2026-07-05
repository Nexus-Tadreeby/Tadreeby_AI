from fastapi import FastAPI

app = FastAPI(
    title="Personalized Training Recommendations API",
    description="Recommend best opportunities for students",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "message": "Hello World"
    }


def recommend_opportunities(data: dict):

    student_id = data.get("studentId")

    student_skills = set([
        skill.lower()
        for skill in data.get("student_skills", [])
    ])

    opportunities = data.get(
        "opportunities",
        []
    )

    recommendations = []

    for opportunity in opportunities:

        required = set([
            skill.lower()
            for skill in opportunity.get(
                "requiredSkills",
                []
            )
        ])

        matched = student_skills.intersection(
            required
        )

        score = len(matched)

        recommendations.append({

            "opportunity_name":
                opportunity.get("title"),

            "matched_skills":
                list(matched),

            "matching_score":
                score
        })

    recommendations.sort(
        key=lambda x: x["matching_score"],
        reverse=True
    )

    return {
        "studentId": student_id,
        "recommended_opportunities":
            recommendations[:3]
    }


@app.post("/training-recommendations")
def training_recommendations(data: dict):

    return recommend_opportunities(data)
