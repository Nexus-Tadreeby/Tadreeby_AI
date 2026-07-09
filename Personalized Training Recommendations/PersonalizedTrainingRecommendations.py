from fastapi import FastAPI
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn

app = FastAPI(
    title="Personalized Training Recommendations API",
    description="Recommend the best training opportunities based on student skills",
    version="1.0"
)


vectorizer = joblib.load(
    "models/recommendation_vectorizer.pkl"
)

opportunity_vectors = joblib.load(
    "models/opportunity_vectors.pkl"
)

opportunities = joblib.load(
    "models/opportunities_data.pkl"
)

print("Recommendation Model Loaded Successfully")


@app.get("/")
def home():
    return {
        "message": "Personalized Training Recommendations API is running!"
    }

@app.post("/training-recommendations")
def training_recommendations(data: dict):

    student_skills = data.get(
        "student_skills",
        []
    )

    student_text = " ".join(
        [skill.lower() for skill in student_skills]
    )

    student_vector = vectorizer.transform(
        [student_text]
    )

    similarity_scores = cosine_similarity(
        student_vector,
        opportunity_vectors
    )[0]

    top_indices = similarity_scores.argsort()[::-1][:3]

    recommendations = []

    for index in top_indices:

        recommendations.append({

            "title":
                opportunities.iloc[index]["title"],

            "match_score":
                round(float(similarity_scores[index]), 2)

        })

    return {

        "studentId":
            data.get("studentId"),

        "recommended_opportunities":
            recommendations
    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001
    )