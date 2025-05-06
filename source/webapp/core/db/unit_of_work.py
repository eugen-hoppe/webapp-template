from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from webapp.core.repositories.user import UserRepository


class AbstractUnitOfWork(metaclass=ABCMeta):
    user_repo: UserRepository
    # ...

    # ---------- context-manager ----------
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError  # pragma: no cover

    # ---------- transaction control ----------
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    # ---------- context-manager ----------
    async def __aenter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        await self.session.begin()
        self.user_repo = UserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, *_):
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    # ---------- transaction control ----------
    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session.in_transaction():
            await self.session.rollback()
