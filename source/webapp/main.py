import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware
from webapp.apps.api.app import api
from webapp.apps.web.app import web
from webapp.core.db.engine import Base, engine
from webapp.core.db.scripts.seed_location import migrate_locations
from webapp.settings import BASE_DIR, conf, dev_docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    await migrate_locations()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="WebApp", lifespan=lifespan, **dev_docs)


app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)
app.add_middleware(CSRFProtectMiddleware, csrf_secret=conf.CSRF_SECRET)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/api", api)
app.mount("/web", web)
