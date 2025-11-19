from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.core.templates import render_template
from app.schemas.credit import StageStatus
from app.schemas.session import CreditSession
from app.scripts.session_controller import (
    attach_session_to_response,
    get_session,
    save_session,
)
from app.scripts.utils import find_stage_by_name
from app.core.logger import logger

router = APIRouter(prefix="/components", tags=["components"])


@router.get("/online_form_stages/{stage}", response_class=HTMLResponse)
async def get_online_form_stage(
    stage: str,
    request: Request,
    session: CreditSession = Depends(get_session),
):
    logger.info(session)
    session.current_stage = stage
    await save_session(request, session)

    response = render_template(
        request,
        "online_form_stages/{}_stage.j2".format(stage),
        {
            "request": request,
            "stage": find_stage_by_name(session.credit.online_form_stages, stage),
            "credit": session.credit,
            "session": session,
        },
    )

    attach_session_to_response(response, request)
    return response
