from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from errors.responses import validation_error_response

FIELD_MESSAGES = {
    "contactNumber": {
        "string_too_short": "Contact number is required and must be exactly 11 digits.",
        "string_too_long": "Contact number must be exactly 11 digits.",
        "string_pattern_mismatch": "Contact number must contain exactly 11 digits.",
    },
    "address": {
        "string_too_short": "Address is required.",
    },
    "plateNumber": {
        "string_too_short": "Plate number is required.",
        "string_too_long": "Plate number is too long.",
    },
    "make": {
        "string_too_short": "Vehicle make is required.",
    },
    "model": {
        "string_too_short": "Vehicle model is required.",
    },
    "ownerName": {
        "string_too_short": "Owner name is required.",
    },
    "serviceDate": {
        "string_too_short": "Service date is required.",
    },
    "parts": {
        "too_short": "At least one part is required.",
    },
}


async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    if not isinstance(exc, RequestValidationError):
        raise exc

    errors: dict[str, str] = {}

    for error in exc.errors():
        location = error.get("loc", [])
        field = str(location[-1]) if location else "unknown"
        error_type = error.get("type", "")

        field_config = FIELD_MESSAGES.get(field, {})

        message = field_config.get(
            error_type,
            "Invalid value.",
        )

        errors[field] = message

    return JSONResponse(
        status_code=422,
        content=validation_error_response(errors),
    )
