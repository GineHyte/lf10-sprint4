from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.credit import Credit


class FrontendVariables(BaseModel):
    title: str = "Kreditanträge"


class CreditSession(BaseModel):
    current_stage: str = ""
    credit: Optional[Credit] = None
    frontend_variables: FrontendVariables = FrontendVariables()
