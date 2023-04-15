from rest_framework import status
from rest_framework.response import Response


def response_all(success=None, status=None, message=None, data={}, error=None, ):
    response = {
        'success': success,
        'status_code': status,
        'message': message,
        'data': data,
        'error': error
    }
    return Response(response, status)

def response_nondata(success=None, status=None, message=None):
    response = {
        'success': success,
        'status_code': status,
        'message': message,
    }
    return Response(response, status)
