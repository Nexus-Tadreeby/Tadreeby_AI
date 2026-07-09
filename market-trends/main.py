from fastapi import FastAPI
import joblib
import uvicorn


app = FastAPI(
    title="Market Trends Analysis API",
    description="Analyze high-demand skills in the market",
    version="1.0"
)



market_trends = joblib.load(
    "models/market_trends.pkl"
)


print("Market Trends Model Loaded Successfully")



@app.get("/")
def home():

    return {
        "message": "Market Trends Analysis API is running!"
    }



@app.post("/market-trends")
def market_trends_analysis(data: dict):


    opportunities = data.get(
        "opportunities",
        []
    )


    skills = []



    for opportunity in opportunities:

        required_skills = opportunity.get(
            "requiredSkills",
            []
        )


        skills.extend(
            [
                skill.lower()
                for skill in required_skills
            ]
        )



    result = {

        "high_demand": [],

        "medium_demand": [],

        "low_demand": []

    }



    for skill in skills:


        if skill in market_trends["high_demand"]:

            result["high_demand"].append(
                skill
            )


        elif skill in market_trends["medium_demand"]:

            result["medium_demand"].append(
                skill
            )


        else:

            result["low_demand"].append(
                skill
            )

    for key in result:

        result[key] = list(
            set(result[key])
        )



    return {

        "market_skill_trends":
            result

    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001
    )