from fastapi import WebSocket

from app.schemas.events import *
from app.schemas.session import CreditSession

event: Event  # static
session: CreditSession  # static


def process_json_event(
    prop_websocket: WebSocket, prop_event: Event, prop_session: CreditSession
) -> bool:
    """If returns false -> close the connection"""
    global event, session, websocket

    event = prop_event
    session = prop_session
    websocket = prop_websocket

    match event.type:
        case EventType.SET_CREDIT_SESSION_VARIABLE:
            set_credit_session_variable(event.payload)
        case EventType.SET_CREDIT_SESSION_FRONTEND_VARIABLE:
            set_credit_session_frontend_variable(event.payload)
        case EventType.CLOSE_CONNECTION:
            return False

    return True


def set_credit_session_variable(payload: SetCreditSessionVariablePayload):
    global session

    payload = SetCreditSessionVariablePayload.model_validate(payload)
    setattr(session, payload.key, payload.value)


def set_credit_session_frontend_variable(payload: SetCreditSessionVariablePayload):
    global session

    payload = SetCreditSessionVariablePayload.model_validate(payload)
    setattr(session.frontend_variables, payload.key, payload.value)
