from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

class BookSurvey(BaseModel):
    character: str
    theme: str
    product_id: str

@app.post("/survey")
async def handle_survey(data: BookSurvey):
    print("Received survey data:", data)
    return {"status": "ok", "message": "Book customization received"}