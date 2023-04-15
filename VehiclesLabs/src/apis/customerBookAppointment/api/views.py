import logging

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from src.utils import http_status
# from src.utils.exception import custom_exception_message
from src.apis.customerBookAppointment.models import BookAppointment
from .serializers import *
from src.utils.pagination import StandardResultsSetPagination
pagination_class = StandardResultsSetPagination
logger = logging.getLogger('watchtower-logger')


def Diff(list1, list2):
    return (list(list(set(list1)-set(list2))))


class BookAppointmentRegisterAPIView(generics.CreateAPIView):
    queryset = BookAppointment.objects.all()
    serializer_class = BookAppointmentRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            job_card_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Appointment successfully registered.",
                'data': request.data,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n detail : {response}\n\n ")
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


class BookAppointmentList(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = BookAppointment.objects.all()
    serializer_class = BookAppointmentListSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = BookAppointment.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'servicesID', 'workshopID', 'brandID')
            serializer = BookAppointmentListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Appointment Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Data details : {serializer.data}\n\n ")
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


class AppointDetailbyAppointIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = BookAppointmentListSerializer
    queryset = BookAppointment.objects.all()

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for appointID = {pk}\n\n ")
        try:
            model = BookAppointment.objects.get(appointID=pk, isDeleted=False)
            serializer = BookAppointmentListSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': http_status.OK,
                'message': 'Book Appointment data fetched successfully',
                'data': serializer.data,
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


class AppointDetailbyworkshopIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = BookAppointmentListSerializer
    queryset = BookAppointment.objects.all()
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for workshopID = {pk}\n\n ")
        try:
            model = BookAppointment.objects.filter(
                workshopID=pk, isDeleted=False).order_by('appointDate')
            model = model.prefetch_related('cusID', 'servicesID', 'workshopID', 'brandID')
            
            serializer = BookAppointmentListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': http_status.OK,
                'message': 'Book Appointment data fetched successfully',
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


class AppointDetailbycusIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = BookAppointmentListSerializer
    queryset = BookAppointment.objects.all()
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for cusID = {pk}\n\n ")
        try:
            model = BookAppointment.objects.filter(
                cusID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'servicesID', 'workshopID', 'brandID')            
            serializer = BookAppointmentListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': http_status.OK,
                'message': 'Book Appointment data fetched successfully',
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


class BookAppointUpdatebyAppointIDAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = BookAppointmentUpdateSerializer
    queryset = BookAppointment.objects.all()

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating appointment\n\n ")
        try:
            obj = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Appointment updated successfully',
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


class BookAppointDeletebyAppointIDAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = BookAppointmentListSerializer
    queryset = BookAppointment.objects.all()

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for appointID = {pk}\n\n ")
        try:
            model = BookAppointment.objects.get(appointID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "status_code": status_code,
                "message": "Appointment deleted successfully.",
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
        return Response(response, status_code)
