from fastapi import APIRouter, Depends, Query, status
from webapp.core.models.location import LocationRead, LocationCreate
from webapp.core.services.location import LocationFacade
from webapp.dependencies import get_location_facade

locations_v1 = APIRouter(prefix="/v1")


@locations_v1.get(
    "/locations",
    response_model=list[LocationRead],
    status_code=status.HTTP_200_OK,
)
async def search_locations(
    q: str = Query(min_length=1),
    loc_fx: LocationFacade = Depends(get_location_facade),
):
    return await loc_fx.crud.search(q)


@locations_v1.post(
    "/locations",
    response_model=LocationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_location(
    location: LocationCreate,
    loc_fx: LocationFacade = Depends(get_location_facade),
):
    return await loc_fx.crud.create(location)
