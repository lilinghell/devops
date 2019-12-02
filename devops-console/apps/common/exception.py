from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(exc, DevException):
            response.data['response_code'] = response.data['detail'].split(".", 1)[0]
            response.data['response_msg'] = response.data['detail'].split(".", 1)[1]
            del response.data['detail']
        else:
            response.data['response_code'] = str(response.status_code).zfill(6)
            if response.status_code != status.HTTP_400_BAD_REQUEST:
                response.data['response_msg'] = response.data['detail']
                del response.data['detail']
    else:
        # 未知错误
        data = {}
        response = Response(data, status=status.HTTP_200_OK)
        response.data['response_code'] = "BBBBBBB"
        response.data['response_msg'] = exc.args[0]

    print(response.data)
    return response


class XdError(APIException):
    pass


class DevException(XdError):
    status_code = 200
