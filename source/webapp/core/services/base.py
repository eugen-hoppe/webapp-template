from dataclasses import dataclass, field
from typing import Any, Mapping

from fastapi import BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from webapp.core.db.unit_of_work import UnitOfWork
from webapp.settings import TEMPLATES_DIR


class Service:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow


@dataclass
class HTMX:
    status_code: int = 200
    headers: Mapping[str, str] | None = None
    media_type: str | None = None
    background: BackgroundTasks | None = None
    extension: str = "jinja2"
    templates: Jinja2Templates = field(
        default_factory=lambda: Jinja2Templates(directory=TEMPLATES_DIR)
    )

    def render(self, template_name: str, context: dict[str, Any]) -> HTMLResponse:
        return self.templates.TemplateResponse(
            name=f"{template_name}.{self.extension}",
            context=context,
            status_code=self.status_code,
            headers=self.headers,
            media_type=self.media_type,
            background=self.background,
        )
    
