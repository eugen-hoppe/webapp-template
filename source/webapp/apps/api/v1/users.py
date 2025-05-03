from fastapi import APIRouter, Request



users_v1 = APIRouter(prefix="/v1")



@users_v1.get("/user/")
async def get_user_by_query(user_id: int, request: Request):
    return f"<p>User: <strong>{user_id}</strong></p>"
