# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.utils import http_status
from src.apis.serviceReminder.models import ServiceReminder

logger = logging.getLogger('watchtower-logger')


def Diff(list1, list2):
    return (list(list(set(list1)-set(list2))))


class ServiceReminderRegisterAPIView(generics.CreateAPIView):
    queryset = ServiceReminder.objects.all()
    serializer_class = ServiceReminderRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            job_card_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Services successfully registered.",
                'data': request.data,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class ServiceReminderList(generics.ListAPIView):
    queryset = ServiceReminder.objects.all()
    serializer_class = ServiceReminderListSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = ServiceReminder.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'workshopID', 'serviceID')
            serializer = ServiceReminderListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Serivce Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
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


class ServiceReminderbysdIDAPIView(generics.RetrieveAPIView):
    queryset = ServiceReminder.objects.all()
    serializer_class = ServiceReminderListSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for sdID = {pk}\n\n ")
        try:
            model = ServiceReminder.objects.get(sdID=pk, isDeleted=False)
            model = model.prefetch_related('cusID', 'workshopID', 'serviceID')
            serializer = ServiceReminderListSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': http_status.OK,
                'message': 'Services data fetched successfully',
                'data': serializer.data,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
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


class ServiceReminderbyworkshopIDAPIView(generics.ListAPIView):
    queryset = ServiceReminder.objects.all()
    serializer_class = ServiceReminderListSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for workshopID = {pk}\n\n ")
        try:
            model = ServiceReminder.objects.filter(
                workshopID=pk, isDeleted=False).order_by('reminderDate')
            model = model.prefetch_related('cusID', 'workshopID', 'serviceID')
            serializer = ServiceReminderListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK

            response = {
                'success': True,
                'status_code': http_status.OK,
                'message': 'Services data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
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


class ServiceReminderbycusIDAPIView(generics.ListAPIView):
    queryset = ServiceReminder.objects.all()
    serializer_class = ServiceReminderListSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for cusID = {pk}\n\n ")
        try:
            model = ServiceReminder.objects.filter(
                cusID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'workshopID', 'serviceID')
            serializer = ServiceReminderListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': http_status.OK,
                'message': 'Services data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
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


class ServiceReminderUpdatebyAppointIDAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = ServiceReminderUpdateSerializer
    queryset = ServiceReminder.objects.all()

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data\n\n ")
        try:
            job_update = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Services updated successfully',
                'data': request.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
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


class ServiceReminderDeletebyAppointIDAPIView(generics.DestroyAPIView):
    queryset = ServiceReminder.objects.all()
    serializer_class = ServiceReminderListSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for sdID = {pk}\n\n ")
        try:
            model = ServiceReminder.objects.get(sdID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "status_code": status_code,
                "message": "Appointment deleted successfully.",
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
