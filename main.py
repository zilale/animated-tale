from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookSurvey(BaseModel):
    character: str
    theme: str
    product_id: str

@app.post("/survey")
async def handle_survey(data: BookSurvey):
    print("Received survey data:", data)
    return {"status": "ok", "message": "Book customization received"}