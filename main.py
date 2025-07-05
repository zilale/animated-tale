from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        # type: ignore
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
    character: str
    theme: str
    product_id: str


@app.post("/survey")
async def handle_survey(data: BookSurvey):
    print("Received survey data:", data)
    return {"status": "ok", "message": "Book customization received"}
