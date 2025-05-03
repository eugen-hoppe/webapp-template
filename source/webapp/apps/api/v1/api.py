from fastapi import APIRouter


api_v1 = APIRouter(prefix="/v1")


@api_v1.get("/ping")
async def ping():
    return "Pong"
