from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.scripts.frontend_utils import *

templates = Jinja2Templates(directory="app/templates")
templates.env.globals.update(statusToClass=status_to_class)
templates.env.globals.update(
    getCursorTwClassFromOnlineFormStatus=get_cursor_tw_class_from_online_form_status
)


def render_template(request: Request, template_name: str, context: dict):
    return templates.TemplateResponse(request, template_name, context)
