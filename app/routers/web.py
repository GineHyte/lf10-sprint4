from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.core.logger import logger
from app.core.templates import render_template
from app.schemas.credit import Credit
from app.schemas.session import CreditSession
from app.scripts.session_controller import get_session, save_session
from app.scripts.utils import find_credit_by_number
from app.test_data import credits

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_index(
    request: Request,
    session: CreditSession = Depends(get_session),
):
    session.frontend_variables.title = "Kreditanträge"
    await save_session(request, session)

    response = render_template(
        request,
        "index.j2",
        {
            "request": request,
            "credits": credits.credits,
            "session": session,
        },
    )
    return response


@router.get("/credit_request/{credit_number}", response_class=HTMLResponse)
async def read_credit_request(
    credit_number: int,
    request: Request,
    session: CreditSession = Depends(get_session),
):
    session.credit = find_credit_by_number(credits.credits, credit_number)
    session.frontend_variables.title = "Kreditantrag №" + str(credit_number)
    if session.current_stage == "quit":
        session.current_stage = "credit_format"
    await save_session(request, session)

    response = render_template(
        request,
        "credit_request_base.j2",
        {
            "request": request,
            "credit": session.credit,
            "session": session,
        },
    )
    logger.info(response.headers)
    return response


@router.get("/new_credit_request", response_class=HTMLResponse)
async def read_credit_request_new(
    request: Request, session: CreditSession = Depends(get_session)
):
    session.credit = Credit()
    session.current_stage = "credit_format"
    session.frontend_variables.title = "Neuen Kreditantrag erfassen"
    await save_session(request, session)

    response = render_template(
        request,
        "credit_request_base.j2",
        {"request": request, "session": session},
    )
    return response
