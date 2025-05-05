from webapp.core.db.models import User
from webapp.core.repositories.user import UserRepository
from webapp.core.models.user import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get(self, user_id: int) -> User:
        return await self.repo.get(user_id)

    async def create(self, data: UserCreate) -> User:
        return await self.repo.create(data.model_dump())
