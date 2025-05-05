from typing import Generic, TypeVar, Type, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.core.db.engine import Base


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    # ---------- READ ----------
    async def get(self, obj_id: int) -> T | None:
        return await self.session.get(self.model, obj_id)

    async def list(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    # ---------- CREATE ----------
    async def create(self, data: dict, *, refresh: bool = True) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        if refresh:
            await self.session.refresh(obj)
        return obj

    # ---------- UPDATE ----------
    async def update(
        self,
        obj: T,
        data: dict,
        *,
        allowed: Iterable[str] | None = None,
        refresh: bool = True,
    ) -> T:
        if allowed is None:
            allowed = data.keys()
        changed = False
        for k, v in data.items():
            if k in allowed and getattr(obj, k) != v:
                setattr(obj, k, v)
                changed = True
        if changed:
            await self.session.flush()
            if refresh:
                await self.session.refresh(obj)
        return obj

    # ---------- DELETE ----------
    async def delete(self, obj: T, *, flush: bool = True) -> None:
        await self.session.delete(obj)
        if flush:
            await self.session.flush()
