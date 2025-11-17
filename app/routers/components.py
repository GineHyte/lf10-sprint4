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

router = APIRouter(prefix="/components")


def _online_form_stage_allowed(session: CreditSession, stage: str) -> bool:
    if session.credit.global_stages.online_form.status == StageStatus.DONE:
        return True

    stage_status: StageStatus = session.credit.online_form_stages[stage].status

    if stage_status == StageStatus.DONE or stage_status == StageStatus.PENDING:
        return True

    return False


@router.get("/online_form_stages/{stage}", response_class=HTMLResponse)
async def get_online_form_stage(
    stage: str,
    request: Request,
    session: CreditSession = Depends(get_session),
):
    if not _online_form_stage_allowed(session, stage):
        return HTMLResponse()

    session.current_stage = stage
    await save_session(request, session)

    response = render_template(
        request,
        "stages/{}_stage.j2".format(stage),
        {
            "request": request,
            "credit": session.credit,
            "session": session,
        },
    )

    attach_session_to_response(response, request)
    return response
