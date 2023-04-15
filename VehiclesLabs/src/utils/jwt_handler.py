import datetime
from django.conf import settings
from django.utils import timezone
from .main import JWT_AUTH
from src.utils import http_status
expire_delta = JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def jwt_response_payload_handler1(token, user=None, request=None):
    return {
        'success': True,
        'status_code': http_status.OK,
        'message': 'User Logged In successfully',
        'data': {
            'token': token,
            'userID': user.userID,
            'username': user.username,
            'useremail': user.email,
            'userphone': user.userphone,
            'useraddress': user.useraddress,
            'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200)
        }
    }
