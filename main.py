# main.py
from typing import Union
from fastapi import FastAPI
from mangum import Mangum # Add this import

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# This is the handler function for AWS Lambda
handler = Mangum(app)