from fastapi import FastAPI, Request, Depends, status, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from webapp.dependencies import get_user_service
from webapp.core.services.user import UserService
from webapp.settings import BASE_DIR, dev_docs
from webapp.core.models.user import UserCreate


web = FastAPI(title="Web", root_path="/web", **dev_docs)
templates = Jinja2Templates(directory=str(BASE_DIR / "apps" / "web" / "templates"))


@web.get("/users/fragment/table", response_class=HTMLResponse)
async def users_table_fragment(
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.uow.user_repo.list()
    return templates.TemplateResponse("_user_table.jinja2", {"request": request, "users": users})


@web.get("/users/fragment/form", response_class=HTMLResponse)
async def user_form_fragment(
    request: Request,
    user_id: int | None = None,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get(user_id) if user_id else None
    return templates.TemplateResponse("_user_form.jinja2", {"request": request, "user": user})


@web.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    return templates.TemplateResponse("users.jinja2", {"request": request})


@web.post("/users", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def create_user_html(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    # <- hier jetzt das Pydantic-Objekt
    user = await user_service.create(UserCreate(username=username, email=email))
    return templates.TemplateResponse("_user_row.jinja2", {"request": request, "user": user})

@web.put("/users/{user_id}", response_class=HTMLResponse)
async def update_user_html(
    request: Request,
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    # 1. ORM-Entity holen
    existing = await user_service.uow.user_repo.get(user_id)
    if existing is None:
        raise HTTPException(status_code=404)

    # 2. Aktualisieren
    await user_service.uow.user_repo.update(
        existing,
        {"username": username, "email": email},
    )

    # 3. Neu laden (ORM oder Pydantic, beides geht für das Template)
    updated = await user_service.uow.user_repo.get(user_id)
    return templates.TemplateResponse(
        "_user_row.jinja2", {"request": request, "user": updated}
    )




@web.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_html(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    # ORM-Entity holen
    orm_user = await user_service.uow.user_repo.get(user_id)
    if orm_user is None:
        raise HTTPException(status_code=404)

    # löschen
    await user_service.uow.user_repo.delete(orm_user)
    return "" 
