from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEV = True  # .env default=False


dev_docs = {
    "openapi_url": None,
    "docs_url": None,
    "redoc_url": None,
}
if DEV:
    dev_docs = {}
