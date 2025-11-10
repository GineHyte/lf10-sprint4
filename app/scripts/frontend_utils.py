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
