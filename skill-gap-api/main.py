from fastapi import FastAPI
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn

app = FastAPI(
    title="Skill Gap Analysis API",
    description="Analyze missing skills and recommend learning paths",
    version="1.0"
)

skillgap_vectorizer = joblib.load(
    "models/skillgap_vectorizer.pkl"
)

skillgap_vectors = joblib.load(
    "models/skillgap_vectors.pkl"
)

skillgap_jobs = joblib.load(
    "models/skillgap_jobs.pkl"
)


print("Skill Gap Model Loaded Successfully")

@app.get("/")
def home():

    return {
        "message": "Skill Gap Analysis API is running!"
    }


@app.post("/skill-gap")
def skill_gap(data: dict):


    student_skills = [

        skill.lower()

        for skill in data.get(
            "student_skills",
            []
        )

    ]


    job_index = data.get(
        "job_index",
        0
    )


    required_skills = (
        skillgap_jobs.iloc[job_index]
        ["required_skills"]
        .split()
    )


    student_text = " ".join(
        student_skills
    )


    student_vector = skillgap_vectorizer.transform(
        [student_text]
    )


    similarity_score = cosine_similarity(
        student_vector,
        skillgap_vectors[job_index]
    )[0][0]



    missing_skills = list(

        set(required_skills)
        -
        set(student_skills)

    )



    recommended_courses = [

        f"{skill} course"

        for skill in missing_skills

    ]



    return {

        "studentId":
            data.get("studentId"),


        "job_title":
            skillgap_jobs.iloc[job_index]
            ["job_title"],


        "match_score":
            round(
                float(similarity_score),
                2
            ),


        "missing_skills":
            missing_skills,


        "recommended_courses":
            recommended_courses

    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )