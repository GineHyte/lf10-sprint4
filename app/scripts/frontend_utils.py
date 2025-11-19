from app.schemas.credit import Credit, StageStatus
from app.scripts.utils import find_stage_by_name

def status_to_class(status: str) -> str:
    status = StageStatus(status)
    if not status or status == StageStatus.NONE:
        return "gray-400"
    if status == StageStatus.DONE:
        return "green-500"
    if status == StageStatus.PENDING:
        return "yellow-500"
    if status == StageStatus.CANCELED:
        return "red-500"
    return "gray-400"


def get_cursor_tw_class_from_credit(credit: dict) -> str:
    credit: Credit = Credit.model_validate(credit)
    online_form_status = find_stage_by_name(credit.global_stages, "online_form").status
    if (
        not online_form_status
        or online_form_status == StageStatus.PENDING
        or online_form_status == StageStatus.NONE
    ):
        return "pointer"
    return "not-allowed"


def get_html_type_from_input_type(type: str) -> str:
    match type:
        case "submit":
            return "submit"
        case "cancel":
            return "button"
    return "button"


def get_tw_classes_from_input_type(type: str) -> str:
    match type:
        case "submit":
            return "bg-blue-600 text-white"
        case "cancel":
            return "bg-gray-600 text-white"
    return "bg-gray-600"


def get_tw_hover_classes_from_input_type(type: str) -> str:
    match type:
        case "submit":
            return "hover:bg-blue-300 hover:text-black"
        case "cancel":
            return "hover:bg-gray-300 hover:text-black"
    return "hover:bg-gray-300"


def get_tw_size_class_button(size: str) -> str:
    match size:
        case "lg":
            return "h-60 w-120"  # TODO: no usages -> need to be corrected
        case "md":
            return "h-20 w-70"
        case "sm":
            return "h-32 w-80"  # TODO: no usages -> need to be corrected
    return "h-44 w-100"

def get_tw_size_class_input_field(size: str) -> str:
    match size:
        case "lg":
            return "w-120"  # TODO: no usages -> need to be corrected
        case "md":
            return "w-70"
        case "sm":
            return "w-80"  # TODO: no usages -> need to be corrected
    return "h-44 w-100"