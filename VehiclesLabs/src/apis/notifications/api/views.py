# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from src.utils import http_status
from src.apis.notifications.models import Notifications
from .serializers import *

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

logger = logging.getLogger('watchtower-logger')


class RegisterAPIView(generics.CreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            notifications_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Notification successfully registered."
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class NotificationsListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authetication_classes = JSONWebTokenAuthentication
    queryset = Notifications.objects.all()
    serializer_class = NotificationsDetailsSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = Notifications.objects.filter(isDeleted=False).order_by('createdAt')
            serializer = NotificationsDetailsSerializer(model, many=True)

            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Notifications Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class NotificationsDetailsAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Notifications.objects.all()
    serializer_class = NotificationsDetailsSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for mediaID = {pk}\n\n ")
        try:
            model = Notifications.objects.get(notifyID=pk, isDeleted=False)
            serializer = NotificationsDetailsSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Notifications fetched successfully.',
                'data': serializer.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")

        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class NotificationsDetailbyUserIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = NotificationsDetailsSerializer
    queryset = Notifications.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = Notifications.objects.filter(
                userID=pk, isDeleted=False, is_read=False)
            serializer = NotificationsDetailsSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Jobcard  data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class NotificationsDeleteAPIView(generics.DestroyAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsDetailsSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for notifyID = {pk}\n\n ")
        try:
            model = Notifications.objects.get(notifyID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "status_code": status_code,
                "message": "Notifications deleted successfully.",
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class NotificationsUpdateAPIView(generics.UpdateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsDetailsSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data\n\n ")
        try:
            job_update = super().update(request, *args, **kwargs)

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Notifications update successfully.',
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
        except Exception as e:
            status_code = http_status.OK
            response = {
                "success": "False",
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)
