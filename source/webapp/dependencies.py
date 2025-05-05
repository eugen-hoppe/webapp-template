from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.core.db.engine import AsyncSessionLocal
from webapp.core.db.unit_of_work import UnitOfWork
from webapp.core.repositories.user import UserRepository
from webapp.core.services.user import UserService


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(AsyncSessionLocal) as uow:
        yield uow


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))
