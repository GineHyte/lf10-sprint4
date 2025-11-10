from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class FrontendVariables(BaseModel):
    title: str = "Kreditanträge"


class CreditSession(BaseModel):
    credit_number: Optional[str] = None
    current_step: int = 1
    payload: Dict[str, Any] = Field(default_factory=dict)
    frontendVariables: FrontendVariables = FrontendVariables()
