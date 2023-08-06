from flask import jsonify

def exception_handler(e):
    return jsonify(code=e.code, detail=e.detail), e.status_code


class APIException(Exception):
    status_code = 400
    code = None
    detail = None

    def __init__(self, *args, **kwargs):
        self.detail = self.detail.format(*args, **kwargs)
        super().__init__(self.detail)


class PermissionDenied(APIException):
    status_code = 403
    code = 'permission_denied'
    detail = '{detail}'
