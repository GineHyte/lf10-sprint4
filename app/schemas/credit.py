from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class StageStatus(Enum):
    DONE = "done"
    PENDING = "pending"
    NONE = "none"


class Stage(BaseModel):
    id: str
    status: StageStatus
    text: str


class GlobalStage(Stage): ...


class OnlineFormStage(Stage):
    title: str
    data: Optional[dict] = {}


class Credit(BaseModel):
    number: int
    global_stages: List[GlobalStage]
    online_form_stages: List[OnlineFormStage]
    created_at: str
    updated_at: str
