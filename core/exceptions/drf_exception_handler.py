import importlib

from core.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import set_rollback

from .exception_data import exception_data


def drf_exception_handler(exc, context):
    response, data = exception_data(context["view"])

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    api_exception = isinstance(exc, exceptions.APIException)
    if api_exception:
        set_rollback()
        if isinstance(exc.detail, (list, dict)):
            response.update(
                {
                    "data": exc.detail,
                    "status": exc.status_code,
                }
            )
        else:
            response.update(
                {
                    "message": exc.detail,
                    "status": exc.status_code,
                }
            )

    try:
        _module = importlib.import_module(context["view"].__module__)
        logger = getattr(_module, "logger")
        logger.exception(
            "{} | {}".format(exc, data),
            extra={
                "clss": context["view"],
                "request": context["request"],
                "drf": True,
            },
        )
    except Exception as e:
        pass

    return JsonResponse(**response)
