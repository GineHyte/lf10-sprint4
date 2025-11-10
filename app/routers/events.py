from fastapi import APIRouter, Depends, WebSocket

from app.schemas.events import Event
from app.schemas.session import CreditSession
from app.scripts.event_controller import process_json_event
from app.scripts.session_controller import (
    attach_session_to_response,
    get_session_ws,
    save_session,
)

router = APIRouter()


@router.websocket("/event_loop")
async def websocket_endpoint(
    websocket: WebSocket, session: CreditSession = Depends(get_session_ws)
):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        event = Event(**data)
        if not process_json_event(event, session):
            break
    await websocket.close()
