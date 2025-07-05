from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)
handler = Mangum(app)

class BookSurvey(BaseModel):
    num_children: int
    children: list[dict]  # Each child will contain fields like name, age, gender, features
    personality: list[str]
    hobbies: list[str]
    curiosities: list[str]
    favorite_places: list[str]
    family_mentions: list[str] = []
    pets: list[dict] = []
    virtues: list[str] = []
    illustration_style: str = ""
    product_id: str

@app.post("/survey")
async def handle_survey(data: BookSurvey):
    print("Received full survey data:", data)
    return {"status": "ok", "message": "Book customization received"}
