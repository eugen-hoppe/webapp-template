from abc import ABCMeta, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from webapp.core.repositories.user import UserRepository


class AbstractUnitOfWork(metaclass=ABCMeta):
    user_repo: UserRepository
    # account_repo
    # ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

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
        self.user_repo = UserRepository(self.session)
        # ...
        # self.account_repo ...
        # ...
        return await super().__aenter__()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()
