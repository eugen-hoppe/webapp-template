from fastapi import APIRouter, Depends

from webapp.core.models.user import UserCreate
from webapp.core.repositories.user import UserRepository
from webapp.dependencies import get_user_repository



users_v1 = APIRouter(prefix="/v1")


@users_v1.get("/user/{user_id}")
async def get_user(user_id: int, crud: UserRepository = Depends(get_user_repository)):
    return await crud.get(user_id)


@users_v1.post("/user/")
async def create_user(user: UserCreate, crud: UserRepository = Depends(get_user_repository)):
    return await crud.create(user.db())
