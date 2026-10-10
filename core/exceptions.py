import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data
        if isinstance(detail, dict) and set(detail.keys()) == {"detail"}:
            message = str(detail["detail"])
            errors = None
        else:
            message = "Validation failed." if response.status_code == 400 else "Request failed."
            errors = detail
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "message": message,
            "errors": errors,
        }
        return response

    if isinstance(exc, IntegrityError):
        logger.warning("Integrity error: %s", exc)
        return Response(
            {
                "success": False,
                "status_code": status.HTTP_409_CONFLICT,
                "message": "The request conflicts with existing data.",
                "errors": None,
            },
            status=status.HTTP_409_CONFLICT,
        )

    logger.exception("Unhandled exception", exc_info=exc)
    return Response(
        {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Something went wrong on the server.",
            "errors": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
