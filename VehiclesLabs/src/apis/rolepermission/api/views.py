# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.utils import http_status
from src.apis.rolepermission.models import Permissions, Marketeer

from django.db.models import Q

logger = logging.getLogger('watchtower-logger')


class PermissionRegisterAPIView(generics.CreateAPIView):
    queryset = Permissions.objects.all()
    serializer_class = JobCardPermissionRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            jobcard_permission = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "User created successfully.",
                'data': jobcard_permission.data
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


class PermissionListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()
    serializer_class = JobCardPermissionRegisterSerializer
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = Permissions.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('user_workshop', 'userID', 'workshopID')
            serializer = JobCardPermissionSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Permission data fetched successfully',
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


class PermissionDetailsByUserWorkshopAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()
    serializer_class = JobCardPermissionSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for user_workshop = {pk}\n\n ")
        try:
            model = Permissions.objects.get(
                user_workshop=pk, isDeleted=False)
            serializer = JobCardPermissionSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Permission data fetched successfully',
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


class PermissionDetailsByUserIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()
    serializer_class = JobCardPermissionSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = Permissions.objects.filter(
                userID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('user_workshop', 'userID', 'workshopID')
            if request.GET.get("search"):
                search = request.GET.get('search')
                model = model.filter( Q(user_workshop__email__icontains=search)
                                    | Q(user_workshop__userphone__icontains=search)
                                    | Q(user_workshop__username__icontains=search))

            serializer = JobCardPermissionSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Permission data fetched successfully',
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


class PermissionDetailsBypermIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()
    serializer_class = JobCardPermissionSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for permID = {pk}\n\n ")
        try:
            model = Permissions.objects.get(permID=pk, isDeleted=False)
            model = model.prefetch_model('user_workshop')
            serializer = JobCardPermissionSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Permission data fetched successfully',
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


class PermissionDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()
    serializer_class = JobCardPermissionSerializer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for permID = {pk}\n\n ")
        try:
            model = Permissions.objects.get(permID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                "success": "true",
                "status_code": status_code,
                "message": "Permission Data Deleted Successfully.",
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


class PermissionUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()
    serializer_class = JobCardUpdatePermissionSerializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data of permID = {pk}\n\n ")
        try:
            model = Permissions.objects.get(permID=pk, isDeleted=False)
            serializer = JobCardUpdatePermissionSerializer(
                model, data=request.data)
            if serializer.is_valid() == True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Permission details Updated Successfully',
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


class MarketeerRegisterAPIView(generics.CreateAPIView):
    queryset = Marketeer.objects.all()
    serializer_class = MarketeerRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            marketeer_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Marketeer created successfully.",
                'data': marketeer_obj.data
            }
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
        return Response(response, status=status_code)


class MarketeerListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Marketeer.objects.all()
    serializer_class = MarketeerListSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        try:
            model = Marketeer.objects.filter(isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('marketerID')
            serializer = MarketeerListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Marketeer data fetched successfully',
                'count': model.count(),
                'data': page
            }
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
        return Response(response, status=status_code)


class MarketeerDetailsBymarketerIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Marketeer.objects.all()
    serializer_class = MarketeerListSerializer

    def get(self, request, pk):
        try:
            model = Marketeer.objects.get(marketerID=pk, isDeleted=False)
            if model:
                model = Marketeer.objects.filter(
                    marketerID=pk, isDeleted=False)
                model = model.prefetch_related('marketerID')
                serializer = MarketeerListSerializer(model, many=True)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Marketeer data fetched successfully',
                    'data': serializer.data
                }
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Marketeer Details does not exists',
                }
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
        return Response(response, status=status_code)


class MarketeerDetailsByUserIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Marketeer.objects.all()
    serializer_class = MarketeerListSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        try:
            model = Marketeer.objects.filter(userID=pk, isDeleted=False)
            model = model.prefetch_related('marketerID')
            serializer = MarketeerListSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Marketeer data fetched successfully',
                'count': model.count(),
                'data': page
            }
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
        return Response(response, status=status_code)


class MarketeerDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        try:
            model = Marketeer.objects.get(mID=pk)
            if model.isDeleted == True:
                status_code = http_status.NOT_FOUND
                response = {
                    'success': False,
                    "status_code": status_code,
                    "message": "Marketeer details Not Found",
                }
            else:
                model.isDeleted = True
                model.save()
                status_code = http_status.OK
                response = {
                    "success": "true",
                    "status_code": status_code,
                    "message": "Marketeer Data Deleted Successfully.",
                }

        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }

        return Response(response, status=status_code)


class MarketeerDetailsBymIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Marketeer.objects.all()
    serializer_class = MarketeerListSerializer

    def get(self, request, pk):
        try:
            model = Marketeer.objects.get(mID=pk, isDeleted=False)
            if model:
                model = Marketeer.objects.get(mID=pk, isDeleted=False)

                serializer = MarketeerListSerializer(model)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Marketeer data fetched successfully',
                    'data': serializer.data
                }
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Marketeer Details does not exists',
                }
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
        return Response(response, status=status_code)


class MarketeerUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Marketeer.objects.all()
    serializer_class = MarketeerListSerializer

    def put(self, request, pk):
        try:
            model = Marketeer.objects.get(mID=pk, isDeleted=False)
            serializer = MarketeerUpdateSerializer(model, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Marketeer details Updated Successfully',
                'data': serializer.data
            }
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
        return Response(response, status=status_code)
