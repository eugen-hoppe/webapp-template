from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = str(BASE_DIR / "apps" / "web" / "templates")


class Settings(BaseSettings):
    IS_DEV: bool = False
    SECRET_KEY: str
    CSRF_SECRET: str

    class Config:
        env_file = ".env"


conf = Settings()


dev_docs = {
    "openapi_url": None,
    "docs_url": None,
    "redoc_url": None,
}
if conf.IS_DEV:
    dev_docs = {}
    print("-" * 80 + " [ DEVELOPMENT ]")
