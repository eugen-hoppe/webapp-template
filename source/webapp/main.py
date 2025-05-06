from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from webapp.apps.api.app import api
from webapp.apps.web.app import web
from webapp.core.db.engine import engine, Base
from webapp.settings import dev_docs, BASE_DIR

app = FastAPI(title="WebApp", **dev_docs)


@app.on_event("startup")
async def _init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/api", api)
app.mount("/web", web)
