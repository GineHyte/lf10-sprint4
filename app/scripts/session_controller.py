from typing import Any, Optional, Protocol, Union, cast
from uuid import UUID, uuid4

from fastapi import Depends, Request, Response, WebSocket
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from fastapi_sessions.frontends.session_frontend import FrontendError

from app.core.config import settings
from app.schemas.session import CreditSession

__all__ = [
    "get_session",
    "get_session_ws",
    "save_session",
    "session_cookie",
    "attach_session_to_response",
]


cookie_parameters = CookieParameters()
session_cookie = SessionCookie(
    cookie_name=settings.session_cookie_name,
    identifier=settings.session_cookie_identifier,
    secret_key=settings.session_secret_key,
    cookie_params=cookie_parameters,
    auto_error=False,
)

_session_backend: InMemoryBackend[UUID, CreditSession] = InMemoryBackend()


class _StateCarrier(Protocol):
    state: Any


async def get_session(
    request: Request,
    response: Response,
    session_reference: Optional[Union[UUID, FrontendError]] = Depends(session_cookie),
) -> CreditSession:
    """Get or create a session for HTTP requests."""
    new_session_needed = session_reference is None or isinstance(
        session_reference, FrontendError
    )

    if new_session_needed:
        session_identifier = uuid4()
        session = CreditSession()
        await _session_backend.create(session_identifier, session)
    else:
        session_identifier = cast(UUID, session_reference)
        session = await _session_backend.read(session_identifier)
        if session is None:
            session = CreditSession()
            await _session_backend.create(session_identifier, session)

    _store_session_identifier(request, session_identifier)
    session_cookie.attach_to_response(response, session_identifier)

    return session


async def get_session_ws(websocket: WebSocket) -> CreditSession:
    """Get or create a session for WebSocket connections."""
    session_reference = None
    cookie_name = settings.session_cookie_name

    if cookie_name in websocket.cookies:
        cookie_value = websocket.cookies[cookie_name]
        try:
            session_reference = session_cookie.verifier.verify_session(cookie_value)
        except Exception:
            session_reference = None

    new_session_needed = session_reference is None or isinstance(
        session_reference, FrontendError
    )

    if new_session_needed:
        session_identifier = uuid4()
        session = CreditSession()
        await _session_backend.create(session_identifier, session)
    else:
        session_identifier = cast(UUID, session_reference)
        session = await _session_backend.read(session_identifier)
        if session is None:
            session = CreditSession()
            await _session_backend.create(session_identifier, session)

    _store_session_identifier(websocket, session_identifier)

    return session


async def save_session(scope: _StateCarrier, session: CreditSession) -> None:
    session_identifier = _get_session_identifier(scope)
    if session_identifier is None:
        raise RuntimeError("No active session associated with the current request.")

    await _session_backend.update(session_identifier, session)


def attach_session_to_response(response: Response, request: Request) -> None:
    session_identifier = _get_session_identifier(request)
    if session_identifier is None:
        return

    session_cookie.attach_to_response(response, session_identifier)


def _store_session_identifier(scope: _StateCarrier, session_identifier: UUID) -> None:
    try:
        scope.state.session_ids[settings.session_cookie_identifier] = session_identifier
    except AttributeError:
        scope.state.session_ids = {
            settings.session_cookie_identifier: session_identifier
        }
    except Exception:
        scope.state.session_ids = {
            settings.session_cookie_identifier: session_identifier
        }


def _get_session_identifier(scope: _StateCarrier) -> Optional[UUID]:
    try:
        maybe_identifier = scope.state.session_ids[settings.session_cookie_identifier]
    except AttributeError:
        return None
    except KeyError:
        return None

    return maybe_identifier if isinstance(maybe_identifier, UUID) else None
