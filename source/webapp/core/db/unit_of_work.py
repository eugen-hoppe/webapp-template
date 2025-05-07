from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from webapp.core.repositories.base import BaseRepository
from webapp.core.repositories.user import UserRepository
from webapp.core.repositories.location import LocationRepository


class AbstractUnitOfWork(metaclass=ABCMeta):
    user_repo: UserRepository
    location_repo = LocationRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        await self.session.begin()

        self.user_repo = UserRepository(self.session)
        self.location_repo = LocationRepository(self.session)

        return self

    async def __aexit__(self, exc_type, *_):
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session.in_transaction():
            await self.session.rollback()

    def get_repository(self, repository_name: str) -> BaseRepository | None:
        return getattr(self, f"{repository_name}_repo", None)
