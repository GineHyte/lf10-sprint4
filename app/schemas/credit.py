from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class StageStatus(Enum):
    DONE = "done"
    PENDING = "pending"
    NONE = "none"


class GlobalStageId(Enum):
    ONLINE_FORM = "online_form"
    DOCUMENTS = "documents"
    TESTS = "tests"
    SECURITY = "security"
    FINAL_DECISION = "final_decision"


class OnlineFormStageId(Enum):
    CREDIT_FORMAT = "credit_format"
    PERSONAL_DATA = "personal_data"


class Stage(BaseModel):
    status: StageStatus
    text: str


class GlobalStage(Stage): ...


class OnlineFormStage(Stage):
    id: GlobalStageId
    title: str
    data: Optional[dict] = {}


class Credit(BaseModel):
    number: int
    global_stages: List[GlobalStage]
    online_form_stages: List[OnlineFormStage]
    created_at: str
    updated_at: str
