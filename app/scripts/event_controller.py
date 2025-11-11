from app.schemas.events import *
from app.schemas.session import CreditSession

event: Event
session: CreditSession


def process_json_event(prop_event: Event, prop_session: CreditSession) -> bool:
    """If returns false -> close the connection"""
    global event, session

    event = prop_event
    session = prop_session

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
    setattr(session.frontendVariables, payload.key, payload.value)
