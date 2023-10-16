from django.conf import settings
from django.http import JsonResponse as BaseJsonResponse

META = {
    "version": settings.VERSION,
}


class JsonResponse(BaseJsonResponse):
    def __init__(
        self,
        data=None,
        message="",
        extra=None,
        status=200,
        code=None,
        meta=None,
        **kwargs
    ):
        message = "Internal Server Error" if status >= 500 and not message else message
        meta = meta or {}
        content = {
            "code": code or status,
            "message": message or "",
            "data": data or [],
            "extra": extra or {},
            "meta": {**meta, **META},
        }
        super().__init__(data=content, status=status, **kwargs)
