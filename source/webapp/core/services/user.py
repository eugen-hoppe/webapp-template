from webapp.core.db.unit_of_work import UnitOfWork
from webapp.core.models.user import UserCreate, UserRead


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get(self, user_id: int) -> UserRead | None:
        user = await self.uow.user_repo.get(user_id)
        return UserRead.model_validate(user) if user else None

    async def create(self, data: UserCreate) -> UserRead:
        user = await self.uow.user_repo.create(data.model_dump())
        return UserRead.model_validate(user)
