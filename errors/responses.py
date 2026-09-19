from typing import Any


def validation_error_response(
    errors: dict[str, Any],
):
    return {
        "success": False,
        "message": "Validation failed.",
        "errors": errors,
    }