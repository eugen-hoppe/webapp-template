from fastapi import Depends, FastAPI, Request, status, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from webapp.apps.web.forms.user import UserForm
from webapp.core.db.unit_of_work import UnitOfWork
from webapp.core.models.user import UserCreate
from webapp.core.services.base import HTMX
from webapp.core.services.user import UserFacade
from webapp.core.services.location import LocationFacade
from webapp.dependencies import get_uow, get_user_facade, get_location_facade
from webapp.settings import dev_docs

web = FastAPI(title="Web", root_path="/web", **dev_docs)


@web.get("/users/fragment/table", response_class=HTMLResponse)
async def users_table_fragment(
    request: Request,
    user_fx: UserFacade = Depends(get_user_facade),
):
    users = await user_fx.crud.uow.user_repo.get_list()
    return user_fx.view.render_user_table(request, users)


@web.get("/users/fragment/form", response_class=HTMLResponse)
async def user_form_fragment(
    request: Request,
    user_id: int | None = None,
    user_fx: UserFacade = Depends(get_user_facade),
):
    user = await user_fx.crud.get(user_id) if user_id else None
    form = UserForm(request, obj=user)
    return user_fx.view.render_user_form(request, form=form, user=user)


@web.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    return HTMX().render("users", context={"request": request})


@web.post("/users", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def create_user_html(
    request: Request, user_fx: UserFacade = Depends(get_user_facade)
):
    form = await UserForm.from_formdata(request)
    if not await form.validate_on_submit():
        return user_fx.view.render_user_form(request, form=form)
    user = await user_fx.crud.create(UserCreate(**form.data))
    return user_fx.view.render_user_row(request, user)


@web.put("/users/{user_id}", response_class=HTMLResponse)
async def update_user_html(
    request: Request,
    user_id: int,
    user_fx: UserFacade = Depends(get_user_facade),
):
    existing = await user_fx.crud.uow.user_repo.get(user_id)
    if existing is None:
        raise HTTPException(status_code=404)

    form = await UserForm.from_formdata(request, obj=existing)
    if not await form.validate_on_submit():
        return user_fx.view.render_user_form(request, form=form, user=existing)

    await user_fx.crud.uow.user_repo.update(
        existing,
        {
            "username": form.username.data,
            "email": form.email.data,
            "location_id": int(form.location_id.data) if form.location_id.data else None,
        },
    )

    updated = await user_fx.crud.uow.user_repo.get(user_id)
    return user_fx.view.render_user_row(request, updated)


@web.delete("/users/{user_id}", response_class=HTMLResponse)
async def delete_user_html(
    request: Request,
    user_id: int,
    user_fx: UserFacade = Depends(get_user_facade),
):
    orm_user = await user_fx.crud.uow.user_repo.get(user_id)
    if orm_user is None:
        raise HTTPException(status_code=404)

    await user_fx.crud.uow.user_repo.delete(orm_user)

    html_oob = '<div id="user-form-panel" hx-swap-oob="true"></div>'
    return HTMLResponse(html_oob)


@web.get("/table/{entity_name}", response_class=HTMLResponse)
async def generic_table(
    request: Request,
    entity_name: str,
    uow: UnitOfWork = Depends(get_uow),
):
    repo = uow.get_repository(entity_name)
    if not repo:
        raise HTTPException(status_code=404, detail="Entity not found")

    items = await repo.get_list()
    if not repo.tb_columns():
        raise HTTPException(status_code=400)
    return HTMX().render(
        "generic/table_wrapper",
        context={
            "request": request,
            "items": items,
            "columns": repo.tb_columns(),
        },
    )


@web.get("/locations/fragment/suggest", response_class=HTMLResponse)
async def location_suggestions(
    request: Request,
    q: str = Query(..., min_length=2, alias="location_search"),
    loc_fx: LocationFacade = Depends(get_location_facade),
):
    results = await loc_fx.crud.search(q)
    return loc_fx.view.render_location_suggestions(request, results)
