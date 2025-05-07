from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.core.db.models import Location
from webapp.core.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self, session: AsyncSession):
        super().__init__(Location, session)

    async def search(self, q: str, limit: int = 10) -> list[Location]:
        stmt = (
            select(Location)
            .where(Location.city.ilike(f"{q}%"))
            .order_by(Location.city.asc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()
