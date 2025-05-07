from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
DEV = True  # .env default=False
TEMPLATES_DIR = str(BASE_DIR / "apps" / "web" / "templates")

dev_docs = {
    "openapi_url": None,
    "docs_url": None,
    "redoc_url": None,
}
if DEV:
    dev_docs = {}


class Settings(BaseSettings):
    IS_DEV: bool = False
    SECRET_KEY: str
    CSRF_SECRET: str

    class Config:
        env_file = ".env"


conf = Settings()


if conf.IS_DEV:
    print("-" * 80 + " [ DEVELOPMENT ]")
