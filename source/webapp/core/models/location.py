from webapp.core.models.base import BaseORM


class LocationCreate(BaseORM):
    post_code: str
    city: str


class LocationRead(LocationCreate):
    id: int
