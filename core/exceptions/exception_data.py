def exception_data(view):
    try:
        data = view.exception_data
    except Exception as e:
        data = {}
    response = {
        "status": data.get("status", 500),
        "code": data.get("code", None),
        "message": data.get("message", ""),
        "data": data.get("data", []),
        "extra": data.get("extra", {}),
        "meta": data.get("meta", {}),
    }
    return response, data
