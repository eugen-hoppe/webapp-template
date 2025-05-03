from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from webapp.settings import BASE_DIR, dev_docs


web = FastAPI(title="Web", root_path="/web", **dev_docs)


templates = Jinja2Templates(directory=str(BASE_DIR / "apps" / "web" / "templates"))


@web.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.jinja2", {"request": request})
