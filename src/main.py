import uvicorn

from pymongo import MongoClient
from typing import Optional, List
from fastapi import FastAPI, status
from pydantic import BaseModel


app = FastAPI()
DB = "rrsdb"
MSG_COLLECTION = "domain"

class Competency(BaseModel):
    id: int
    mode: str
    name: str
    summary: Optional[str] = None
    description: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.post("/domain/add")
async def add_domain(competency: Competency):
    DATA_COMPETENCY = {
        "id": competency.id,
        "mode": competency.mode,
        "name": competency.name,
        "summary": competency.summary,
        "description": competency.description
    }

    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(competency.dict())
        ack = result.acknowledged
        return {
            "message": "new data is added",
            "status": ack,
            "new_data": DATA_COMPETENCY
        }

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level="info", reload=True)