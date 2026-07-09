from fastapi import FastAPI
import joblib
import uvicorn

app = FastAPI(
    title="Smart Progress Tracking API",
    description="Track student progress using Machine Learning",
    version="1.0"
)

progress_model = joblib.load(
    "models/smart_progress_model.pkl"
)

progress_encoder = joblib.load(
    "models/progress_encoder.pkl"
)

print("Smart Progress Model Loaded Successfully")


@app.get("/")
def home():
    return {
        "message": "Smart Progress Tracking API is running!"
    }


@app.post("/smart-progress")
def smart_progress(data: dict):

    input_data = [[
        data.get("total_tasks"),
        data.get("completed_tasks"),
        data.get("attendance_rate"),
        data.get("activity_score")
    ]]

    prediction = progress_model.predict(input_data)[0]

    status = progress_encoder.inverse_transform([prediction])[0]

    total_tasks = data.get("total_tasks")
    completed_tasks = data.get("completed_tasks")

    remaining_tasks = total_tasks - completed_tasks

    if status == "On Track":
        motivation = "Great progress! Keep going "
    else:
        motivation = "You need more focus and improvement "

    return {
        "studentId": data.get("studentId"),
        "completion_status": status,
        "tasks_remaining": remaining_tasks,
        "motivation": motivation
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )