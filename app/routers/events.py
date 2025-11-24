from fastapi import APIRouter, Depends, WebSocket

from app.core.config import settings
from app.core.logger import logger
from app.schemas.events import Event
from app.schemas.session import CreditSession
from app.scripts.event_controller import process_json_event
from app.scripts.session_controller import get_session_ws, save_session

router = APIRouter()


@router.websocket("/event_loop")
async def websocket_endpoint(
    websocket: WebSocket,
    session: CreditSession = Depends(get_session_ws),
):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        logger.info(f"Received event data: {data}")

        event = Event.model_validate(data)
        logger.info(
            f"websocket session {websocket.cookies[settings.session_cookie_name]}"
        )
        logger.info(f"Processing event: {event.type} (requestId: {event.requestId})")

        if not process_json_event(websocket, event, session):
            logger.warning(f"Event processing returned False, closing connection")
            break

        await save_session(websocket, session)

        # Send confirmation if client is waiting for response
        if event.wait_for_response and event.requestId is not None:
            await websocket.send_json({"requestId": event.requestId, "ok": True})
            logger.debug(f"Sent confirmation for requestId: {event.requestId}")

    await websocket.close()
