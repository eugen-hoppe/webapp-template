from fastapi import APIRouter, Depends, status
from webapp.core.models.user import UserCreate, UserRead
from webapp.core.services.user import UserFacade
from webapp.dependencies import get_user_facade

users_v1 = APIRouter(prefix="/v1")


@users_v1.get(
    "/user/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    user_fx: UserFacade = Depends(get_user_facade),
):
    return await user_fx.get(user_id)


@users_v1.post(
    "/user/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    user_fx: UserFacade = Depends(get_user_facade),
):
    return await user_fx.create(user)
