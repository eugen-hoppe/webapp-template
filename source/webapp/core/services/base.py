from dataclasses import dataclass
from typing import Any, Mapping

from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from webapp.core.db.unit_of_work import UnitOfWork
from webapp.settings import TEMPLATES_DIR


class Service:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow


@dataclass
class HTMX:
    templates: Jinja2Templates = Jinja2Templates(directory=TEMPLATES_DIR)
    context: dict[str, Any] | None = None
    status_code: int = 200
    headers: Mapping[str, str] | None = None
    media_type: str | None = None
    background: BackgroundTasks | None = None
    dot: str = "jinja2"

    def __create_payload(
        self, name: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        payload = {
            "status_code": self.status_code,
            "headers": self.headers,
            "media_type": self.media_type,
            "background": self.background,
        }
        payload["name"] = f"{name}.{self.dot}"
        payload["context"] = context if context else self.context
        return payload

    def render(
        self,
        name: str,
        context: dict[str, Any] | None = None,
    ) -> HTMLResponse:
        return self.templates.TemplateResponse(**self.__create_payload(name, context))
