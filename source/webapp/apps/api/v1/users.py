from fastapi import APIRouter, Depends, status
from webapp.core.models.user import UserCreate, UserRead
from webapp.core.services.user import UserService
from webapp.dependencies import get_user_service

users_v1 = APIRouter(prefix="/v1")


@users_v1.get(
    "/user/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get(user_id)


@users_v1.post(
    "/user/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create(user)
