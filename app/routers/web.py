from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.core.logger import logger
from app.core.templates import render_template
from app.schemas.session import CreditSession
from app.scripts.session_controller import (
    attach_session_to_response,
    get_session,
    save_session,
    session_cookie,
)
from app.test_data import credits

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_index(
    request: Request,
    session: CreditSession = Depends(get_session),
    session_reference=Depends(session_cookie),
):
    session.frontend_variables.title = "Kreditanträge"
    await save_session(request, session)

    logger.info(f"rest session: {session_reference}")

    response = render_template(
        request,
        "index.j2",
        {
            "request": request,
            "credits": credits.credits,
            "session": session,
        },
    )
    attach_session_to_response(response, request)
    return response


@router.get("/credit_request/{credit_number}", response_class=HTMLResponse)
async def read_credit_request_detail(
    credit_number: int,
    request: Request,
    session: CreditSession = Depends(get_session),
):
    session.credit_number = str(credit_number)
    session.frontend_variables.title = "Kreditantrag №" + str(credit_number)
    await save_session(request, session)

    response = render_template(
        request,
        "credit_request_stage1.j2",
        {"request": request, "credit": credits.credits[0], "session": session},
    )
    attach_session_to_response(response, request)
    return response


@router.get("/new_credit_request", response_class=HTMLResponse)
async def read_credit_request_new(
    request: Request, session: CreditSession = Depends(get_session)
):
    session.credit_number = None
    session.current_step = 1
    session.frontend_variables.title = "Neuen Kreditantrag erfassen"
    await save_session(request, session)
    await save_session(request, session)

    response = render_template(
        request,
        "credit_request_stage1.j2",
        {"request": request, "session": session},
    )
    attach_session_to_response(response, request)
    return response
