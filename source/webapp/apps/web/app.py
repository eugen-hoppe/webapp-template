from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from webapp.core.models.user import UserCreate
from webapp.core.services.base import HTMX
from webapp.core.services.user import UserService
from webapp.dependencies import get_user_service
from webapp.settings import dev_docs

web = FastAPI(title="Web", root_path="/web", **dev_docs)


@web.get("/users/fragment/table", response_class=HTMLResponse)
async def users_table_fragment(
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.uow.user_repo.list()
    user_service.htmx.context = {"request": request, "users": users}  # .           HTMX
    return user_service.htmx.render("_user_table")


@web.get("/users/fragment/form", response_class=HTMLResponse)
async def user_form_fragment(
    request: Request,
    user_id: int | None = None,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get(user_id) if user_id else None
    user_service.htmx.context = {"request": request, "user": user}  # .             HTMX
    return user_service.htmx.render("_user_form")


@web.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    return HTMX().render("users", context={"request": request})


@web.post("/users", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def create_user_html(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.create(UserCreate(username=username, email=email))
    user_service.htmx.context = {"request": request, "user": user}  # .             HTMX
    return user_service.htmx.render("_user_row")


@web.put("/users/{user_id}", response_class=HTMLResponse)
async def update_user_html(
    request: Request,
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    existing = await user_service.uow.user_repo.get(user_id)
    if existing is None:
        raise HTTPException(status_code=404)
    await user_service.uow.user_repo.update(
        existing,
        {"username": username, "email": email},
    )
    updated = await user_service.uow.user_repo.get(user_id)
    user_service.htmx.context = {"request": request, "user": updated}  # .          HTMX
    return user_service.htmx.render("_user_row")


@web.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_html(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    orm_user = await user_service.uow.user_repo.get(user_id)
    if orm_user is None:
        raise HTTPException(status_code=404)
    await user_service.uow.user_repo.delete(orm_user)
    return ""
