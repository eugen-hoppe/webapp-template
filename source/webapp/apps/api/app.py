from fastapi import FastAPI

from source.webapp.apps.api.v1.users import users_v1


api = FastAPI(title="API", root_path="/api")


api.include_router(users_v1)
