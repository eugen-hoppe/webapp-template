from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite+aiosqlite:///./webapp.db"


engine: AsyncEngine = create_async_engine(
    DATABASE_URL, echo=True, future=True
)

AsyncSessionLocal: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
