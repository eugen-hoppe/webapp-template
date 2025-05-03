from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from webapp.settings import dev_docs, BASE_DIR
from webapp.apps.api.app import api
from webapp.apps.web.app import web


app = FastAPI(title="WebApp", **dev_docs)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/api", api)
app.mount("/", web)
