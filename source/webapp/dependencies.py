from typing import AsyncGenerator

from fastapi import Depends

from webapp.core.db.engine import AsyncSessionLocal
from webapp.core.db.unit_of_work import UnitOfWork
from webapp.core.services.user import UserService


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(AsyncSessionLocal) as uow:
        yield uow


async def get_user_service(uow: UnitOfWork = Depends(get_uow)) -> UserService:
    return UserService(uow)
