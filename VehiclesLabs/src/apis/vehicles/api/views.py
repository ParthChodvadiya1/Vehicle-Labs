# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from .serializers import *
from src.utils import http_status
from src.apis.vehicles.models import VehiclesDetail

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

logger = logging.getLogger('watchtower-logger')


class VehiclesRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VehiclesDetail.objects.all()
    serializer_class = VehiclesSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            vehicle_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Vehicle successfully registered."
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


class VehiclesListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = VehiclesListSerializer
    queryset = VehiclesDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = VehiclesDetail.objects.filter(isDeleted=False)
            serializer = VehiclesSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Vehicles Data fetched successfully',
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


class VehiclesDetailAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VehiclesDetail.objects.all()
    serializer_class = VehiclesListSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vehicleID = {pk}\n\n ")
        try:
            model = VehiclesDetail.objects.get(vehicleID=pk)
            if model.isDeleted == False:
                model = VehiclesDetail.objects.get(vehicleID=pk)
                serializer = VehiclesSerializer(model)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'vehicle data fetched successfully',
                    'data': serializer.data
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'vehicle Details does not exists',
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


class VehiclesDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VehiclesDetail.objects.all()
    serializer_class = VehiclesListSerializer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for vehicleID = {pk}\n\n ")
        try:
            model = VehiclesDetail.objects.get(vehicleID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                "success": True,
                "message": "Data Deleted Successfully.",
                "status_code": status_code
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.OK
            response = {
                "success": False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class VehiclesUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VehiclesDetail.objects.all()
    serializer_class = VehiclesListSerializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data\n\n ")
        try:
            model = VehiclesDetail.objects.get(vehicleID=pk, isDeleted=False)
            serializer = VehiclesSerializer(model, data=request.data)
            if serializer.is_valid() == True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Vehicles details Updated Successfully',
                    'data': serializer.data
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'something is wrong',
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
