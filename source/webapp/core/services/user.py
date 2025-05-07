from fastapi import Request
from fastapi.responses import HTMLResponse
from webapp.apps.web.forms.user import UserForm
from webapp.core.db.unit_of_work import UnitOfWork
from webapp.core.models.user import UserCreate, UserRead
from webapp.core.services.base import HTMX, Service


class UserServiceCRUD(Service):
    async def get(self, user_id: int) -> UserRead | None:
        user = await self.uow.user_repo.get(user_id)
        return UserRead.model_validate(user) if user else None

    async def create(self, data: UserCreate) -> UserRead:
        user = await self.uow.user_repo.create(data.model_dump())
        return UserRead.model_validate(user)


class UserServiceHTMX:
    def __init__(self):
        self.htmx = HTMX()

    def render_user_table(
        self, request: Request, users: list[UserRead]
    ) -> HTMLResponse:
        return self.htmx.render(
            "_user_table",
            context={
                "request": request,
                "users": users,
                "cols": ["id", "username", "email"],
            },
        )

    def render_user_form(self, request: Request, *, form: UserForm, user=None):
        return self.htmx.render(
            "_user_form", {"request": request, "form": form, "user": user}
        )

    def render_user_row(self, request: Request, user: UserRead) -> HTMLResponse:
        return self.htmx.render(
            "_user_row",
            context={
                "request": request,
                "user": user,
                "cols": ["id", "username", "email"],
            },
        )

    def render_user_page(self, request: Request) -> HTMLResponse:
        return HTMX().render("users", context={"request": request})


class UserFacade:
    def __init__(self, uow: UnitOfWork):
        self.crud = UserServiceCRUD(uow)
        self.view = UserServiceHTMX()
