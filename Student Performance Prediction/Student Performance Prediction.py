from fastapi import FastAPI
import joblib


app = FastAPI(
    title="Student Performance Prediction AI API",
    description="Predict student score using Machine Learning",
    version="1.0"
)

model = joblib.load(
    "student_performance_model.pkl"
)


@app.get("/")
def home():

    return {
        "message": "Hello World"
    }



@app.post("/student-performance")
def student_performance(data: dict):

    input_data = [[
        data.get("attendance"),
        data.get("assignments"),
        data.get("midterm"),
        data.get("quiz"),
        data.get("study_hours")
    ]]


    prediction = model.predict(
        input_data
    )[0]


    if prediction >= 80:
        risk_level = "Low"

    elif prediction >= 50:
        risk_level = "Medium"

    else:
        risk_level = "High"


    return {

        "studentId": data.get("studentId"),

        "predicted_score":
            round(float(prediction), 2),

        "risk_level":
            risk_level,

        "expected_achievement":
            f"{round(float(prediction), 2)}%",

        "risk_indicator":
            risk_level
    }