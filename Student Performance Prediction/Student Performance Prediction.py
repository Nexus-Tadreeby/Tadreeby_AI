from fastapi import FastAPI

app = FastAPI(
    title="Student Performance Prediction API",
    description="Predict student score and risk level",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "message": "Hello World"
    }


def predict_performance(data: dict):

    student_id = data.get("studentId")

    scores = data.get("scores", [])

    if len(scores) == 0:
        avg_score = 0
    else:
        avg_score = sum(scores) / len(scores)

    # risk level
    if avg_score >= 80:
        risk = "Low"
    elif avg_score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    return {

        "studentId":
            student_id,

        "predicted_score":
            round(avg_score, 2),

        "risk_level":
            risk,

        "expected_achievement":
            f"{round(avg_score,2)}%",

        "risk_indicator":
            risk
    }


@app.post("/student-performance")
def student_performance(data: dict):

    return predict_performance(data)