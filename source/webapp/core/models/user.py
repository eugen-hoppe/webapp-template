from webapp.core.models.base import BaseORM
from webapp.core.models.location import LocationRead


class UserCreate(BaseORM):
    username: str
    email: str
    location_id: int | None = None


class UserRead(UserCreate):
    id: int

    location: "LocationRead | None" = None
