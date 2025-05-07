from typing import Sequence

from fastapi import Request
from fastapi.responses import HTMLResponse

from webapp.core.db.unit_of_work import UnitOfWork
from webapp.core.models.location import LocationCreate, LocationRead
from webapp.core.services.base import HTMX, Service


class LocationServiceCRUD(Service):
    async def get(self, loc_id: int) -> LocationRead | None:
        loc = await self.uow.location_repo.get(loc_id)
        return LocationRead.model_validate(loc) if loc else None

    async def search(self, q: str, limit: int = 10) -> list[LocationRead]:
        results = await self.uow.location_repo.search(q, limit)
        return [LocationRead.model_validate(r) for r in results]

    async def create(self, data: LocationCreate) -> LocationRead:
        loc = await self.uow.location_repo.create(data.model_dump())
        return LocationRead.model_validate(loc)


class LocationServiceHTMX:
    def __init__(self) -> None:
        self.htmx = HTMX()

    def render_location_suggestions(
        self, request: Request, locations: Sequence[LocationRead]
    ) -> HTMLResponse:
        return self.htmx.render(
            "_location_suggestions",
            context={
                "request": request,
                "locations": locations,
            },
        )


class LocationFacade:
    def __init__(self, uow: UnitOfWork):
        self.crud = LocationServiceCRUD(uow)
        self.view = LocationServiceHTMX()
