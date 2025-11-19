from typing import List

from app.schemas.credit import Stage, Credit

def find_stage_by_name(stages: List[Stage], stage: str):
    for s in stages:
        if getattr(s, "id", None) == stage:
            return s
    return None

def find_credit_by_number(credits: List[Credit], credit_number: int):
    for s in credits:
        if getattr(s, "number", None) == credit_number:
            return s
    return None