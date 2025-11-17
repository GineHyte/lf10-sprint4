def status_to_class(status: str) -> str:
    if not status or status == "none":
        return "gray-400"
    status = status.lower()
    if status == "done":
        return "green-500"
    if status == "pending":
        return "yellow-500"
    if status == "canceled":
        return "red-500"
    return "gray-400"


def get_cursor_tw_class_from_online_form_status(online_form_status: str) -> str:
    if (
        not online_form_status
        or online_form_status == "pending"
        or online_form_status == "none"
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


def get_tw_classes_from_input_size(size: str) -> str:
    match size:
        case "lg":
            return "h-60 w-120"  # TODO: no usages -> need to be corrected
        case "md":
            return "h-20 w-60"
        case "sm":
            return "h-32 w-80"  # TODO: no usages -> need to be corrected
    return "h-44 w-100"
