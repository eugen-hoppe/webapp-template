from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware
from webapp.apps.api.app import api
from webapp.apps.web.app import web
from webapp.core.db.engine import Base, engine
from webapp.settings import BASE_DIR, conf, dev_docs

app = FastAPI(title="WebApp", **dev_docs)


app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)
app.add_middleware(CSRFProtectMiddleware, csrf_secret=conf.CSRF_SECRET)


@app.on_event("startup")
async def _init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/api", api)
app.mount("/web", web)
