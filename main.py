from fastapi import FastAPI, Request
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

class SurveyData(BaseModel):
    shop_domain: str
    customer_email: str
    responses: dict  # or more specific schema later

@app.post("/survey")
async def handle_survey(data: SurveyData):
    print("Survey received:", data)
    return {"status": "ok", "message": "Survey received"}