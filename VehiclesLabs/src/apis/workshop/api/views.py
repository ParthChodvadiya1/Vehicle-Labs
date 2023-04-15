# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.utils import http_status
from src.apis.workshop.models import WorkshopDetail, WorkShopManager

logger = logging.getLogger('watchtower-logger')


class WorkshopRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopDetail.objects.all()
    serializer_class = WorkshopSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            jobcard_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Workshop created successfully.",
                'data': jobcard_obj.data
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


class WorkshopListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopDetail.objects.all()
    serializer_class = WorkshopListSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = WorkshopDetail.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('media')
            serializer = WorkshopListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Workshop Data fetched successfully',
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


class WorkshopDetailAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = WorkshopListSerializer
    queryset = WorkshopDetail.objects.all()

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = WorkshopDetail.objects.get(userID=pk, isDeleted=False)
            # model = model.prefetch_related('media')
            serializer = WorkshopListSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Workshop fetched successfully',
                'data': serializer.data
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


class WorkshopDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopDetail.objects.all()
    serializer_class = WorkshopDetailSerializer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for workshopID = {pk}\n\n ")
        try:
            model = WorkshopDetail.objects.get(workshopID=pk, isDeleted=False)
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
                'success': False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class WorkshopUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopDetail.objects.all()
    serializer_class = WorkshopSerializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for workshopID = {pk}\n\n ")
        try:
            model = WorkshopDetail.objects.get(workshopID=pk, isDeleted=False)
            serializer = WorkshopUpdateSerializer(model, data=request.data)
            if serializer.is_valid() == True:
                serializer.save()
                serializer1 = WorkshopListSerializer(model)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Workshop details Updated Successfully',
                    'data': serializer1.data
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


class WorkshopManagerRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkShopManager.objects.all()
    serializer_class = WorkshopMangerRegisterSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            jobcard_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Workshop manager created successfully.",
                'data': jobcard_obj.data
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


class WorkshopManagerListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkShopManager.objects.all()
    serializer_class = WorkshopManagerSerilizer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = WorkShopManager.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('userID', 'usermanageID', 'workshopID')
            serializer = WorkshopManagerSerilizer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Workshop Data fetched successfully',
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


class WorkshopManagerListByManageIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkShopManager.objects.all()
    serializer_class = WorkshopManagerSerilizer
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorID = {pk}\n\n ")
        try:
            model = WorkShopManager.objects.filter(
                usermanageID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('userID', 'usermanageID', 'workshopID')
            serializer = WorkshopManagerSerilizer(model, many=True)

            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Workshop Data fetched successfully',
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
        return Response(response)


class WorkshopManagerDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkShopManager.objects.all()
    serializer_class = WorkshopManagerSerilizer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for usermanageID = {pk}\n\n ")
        try:
            model = WorkShopManager.objects.get(
                usermanageID=pk, isDeleted=False)
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
                'success': False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)
