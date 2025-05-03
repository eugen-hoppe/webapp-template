from fastapi import FastAPI

from webapp.settings import dev_docs
from webapp.apps.web.app import web


app = FastAPI(title="WebApp", **dev_docs)


app.mount("/", web)
