from collections.abc import Sequence
from typing import Generic, TypeVar, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    # ---------- READ ----------
    async def get(self, obj_id: int) -> T | None:
        return await self.session.get(self.model, obj_id)

    async def list(self) -> Sequence[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    # ---------- CREATE ----------
    async def create(self, data: dict) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    # ---------- UPDATE ----------
    async def update(self, obj: T, data: dict) -> T:
        for k, v in data.items():
            setattr(obj, k, v)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    # ---------- DELETE ----------
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()
