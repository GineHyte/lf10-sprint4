from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.scripts.frontend_utils import *

templates = Jinja2Templates(directory="app/templates")
templates.env.globals.update(statusToClass=status_to_class)
templates.env.globals.update(
    getCursorTwClassFromOnlineFormStatus=get_cursor_tw_class_from_online_form_status
)
templates.env.globals.update(getHtmlTypeFromInputType=get_html_type_from_input_type)
templates.env.globals.update(getTwClassesFromInputType=get_tw_classes_from_input_type)
templates.env.globals.update(getTwClassesFromInputSize=get_tw_classes_from_input_size)
templates.env.globals.update(
    getTwHoverClassesFromInputType=get_tw_hover_classes_from_input_type
)


def render_template(request: Request, template_name: str, context: dict):
    return templates.TemplateResponse(request, template_name, context)
