from fastapi import FastAPI

from webapp.apps.api.v1.api import api_v1


api = FastAPI(title="API", root_path="/api")


api.include_router(api_v1)
