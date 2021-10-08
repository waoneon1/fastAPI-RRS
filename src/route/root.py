from fastapi import APIRouter

root = APIRouter()

@root.get("/")
async def index():
    return {"message": "Hi! and welcome to my API"}