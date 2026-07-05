from fastapi import FastAPI

app = FastAPI(
    title="Smart Progress Tracking API",
    description="Track student progress and motivation",
    version="1.0"
)

@app.get("/")
def home():

    return {
        "message": "Hello World"
    }


def calculate_progress(data: dict):

    student_id = data.get("studentId")

    total_tasks = data.get("total_tasks", 0)
    completed_tasks = data.get("completed_tasks", 0)

    remaining = total_tasks - completed_tasks

    if total_tasks == 0:
        progress = 0
    else:
        progress = (completed_tasks / total_tasks) * 100

    # motivation message
    if progress == 100:
        message = "Excellent! 🎉 You completed everything"
    elif progress >= 70:
        message = "Great job! Keep going 💪"
    elif progress >= 40:
        message = "Good progress, don’t stop 🚀"
    else:
        message = "You can do it, start now 🔥"

    return {
        "studentId": student_id,
        "completion_percentage": round(progress, 2),
        "tasks_remaining": remaining,
        "motivation": message
    }


@app.post("/smart-progress")
def smart_progress(data: dict):

    return calculate_progress(data)