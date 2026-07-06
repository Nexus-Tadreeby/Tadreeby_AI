from fastapi import FastAPI

app = FastAPI(
    title="Completion Rate Prediction API",
    description="Predict completion rate for university students",
    version="1.0"
)

@app.get("/")
def home():

    return {
        "message": "Hello World"
    }

def predict_completion(data: dict):

    university_id = data.get("universityId")

    enrolled_students = data.get(
        "enrolled_students",
        0
    )

    active_students = data.get(
        "active_students",
        0
    )

    if enrolled_students == 0:
        rate = 0
    else:
        rate = (
            active_students /
            enrolled_students
        ) * 100

    # confidence level
    if rate >= 80:
        confidence = "High"
    elif rate >= 50:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {

        "universityId":
            university_id,

        "predicted_completion_rate":
            round(rate, 2),

        "confidence":
            confidence,

        "expected_completion_rate_this_semester":
            f"{round(rate, 2)}%"
    }


@app.post("/completion-rate")
def completion_rate(data: dict):

    return predict_completion(data)