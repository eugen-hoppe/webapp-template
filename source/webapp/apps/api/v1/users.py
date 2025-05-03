from fastapi import APIRouter, Request, Depends


from webapp.core.crud.users import UserCRUD


users_v1 = APIRouter(prefix="/v1")



@users_v1.get("/user/")
async def get_user_by_query(user_id: int, request: Request):
    return f"<p>User: <strong>{user_id}</strong></p>"


@users_v1.get("/user/{user_id}")
async def get(user_id: str, user_crud: UserCRUD = Depends(UserCRUD)):
    return await user_crud.get_by_id(user_id=user_id)


@users_v1.post("/user/")
async def create(user: dict[str, str], user_crud: UserCRUD = Depends(UserCRUD)):
    await user_crud.create(user)
