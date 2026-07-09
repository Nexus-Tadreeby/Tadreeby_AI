from fastapi import FastAPI
import joblib
import uvicorn

app = FastAPI(
    title="Completion Rate Prediction API",
    description="Predict the expected training completion rate",
    version="1.0"
)



completion_model = joblib.load(
    "models/completion_rate_model.pkl"
)

print("Completion Rate Model Loaded Successfully ")


@app.get("/")
def home():
    return {
        "message": "Completion Rate Prediction API is running!"
    }


@app.post("/completion-rate")
def completion_rate(data: dict):

    input_data = [[
        data.get("total_students"),
        data.get("attendance_rate"),
        data.get("assignment_completion_rate"),
        data.get("active_students")
    ]]

    prediction = completion_model.predict(input_data)[0]

    if prediction >= 80:
        confidence = "High"
    elif prediction >= 50:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "universityId": data.get("universityId"),
        "predicted_completion_rate": round(float(prediction), 2),
        "confidence": confidence,
        "expected_completion_rate_this_semester": f"{round(float(prediction), 2)}%"
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )