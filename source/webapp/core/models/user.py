from webapp.core.models.base import BaseORM


class UserCreate(BaseORM):
    username: str
    email: str


class UserRead(UserCreate):
    id: int
