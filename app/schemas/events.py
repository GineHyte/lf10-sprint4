from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class EventType(Enum):
    SET_CREDIT_SESSION_VARIABLE = 1
    SET_CREDIT_SESSION_FRONTEND_VARIABLE = 2
    CLOSE_CONNECTION = 3


class Event(BaseModel):
    type: EventType
    payload: Optional[Dict] = None
    waitForResponse: bool = False
    requestId: Optional[int] = None  # Only used when waitForResponse=True


class SetCreditSessionVariablePayload(BaseModel):
    key: str
    value: Any
