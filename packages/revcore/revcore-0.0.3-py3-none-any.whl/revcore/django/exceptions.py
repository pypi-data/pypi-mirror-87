from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if isinstance(exc, APIError):
        if response is not None:
            response.status_code = exc.status_code
            response.data = {'error': exc.code, 'detail': exc.detail}
    return response


class APIError(APIException):
    status_code = 200
    code = None
    detail = None

    def __init__(self, *args, **kwargs):
        self.detail = self.detail.format(**kwargs)
