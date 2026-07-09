from fastapi import FastAPI
import joblib
import uvicorn


app = FastAPI(
    title="Opportunity Gap Analysis API",
    description="Analyze company skill gaps and recommend training programs",
    version="1.0"
)

opportunity_data = joblib.load(
    "models/opportunity_data.pkl"
)


print("Opportunity Gap Model Loaded Successfully ")



@app.get("/")
def home():

    return {
        "message": "Opportunity Gap Analysis API is running!"
    }


@app.post("/opportunity-gap")
def opportunity_gap(data: dict):


    company_id = data.get(
        "companyId"
    )


    opportunity = opportunity_data[
        opportunity_data["company_id"]
        ==
        company_id
    ].iloc[0]



    required_skills = (

        opportunity["required_skills"]
        .split()

    )



    available_skills = [

        skill.lower()

        for skill in data.get(
            "available_skills",
            []
        )

    ]



    missing_skills = list(

        set(required_skills)
        -
        set(available_skills)

    )



    recommended_training = [

        f"{skill} training program"

        for skill in missing_skills

    ]



    return {


        "companyId":
            company_id,


        "opportunity":
            opportunity["opportunity_title"],


        "skills_in_demand":
            required_skills,


        "missing_skills":
            missing_skills,


        "recommended_training_programs":
            recommended_training

    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001
    )