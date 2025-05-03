from fastapi import APIRouter



users_v1 = APIRouter(prefix="/v1")


@users_v1.get("/user/{user_id}")
async def get_user(user_id: int):
    return f"User {user_id}"
