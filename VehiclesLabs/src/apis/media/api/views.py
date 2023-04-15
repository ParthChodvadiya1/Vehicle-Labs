# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from .serializers import *
from src.utils import http_status
from src.apis.media.models import MediaDetails

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

logger = logging.getLogger('watchtower-logger')

class MediaRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = MediaDetails.objects.all()
    serializer_class = MediaSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success':True,
                'status_code': status_code,
                'message': "Media added successfully.",
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success':False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class MediaListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = MediaDetails.objects.all()
    serializer_class = MediaDetailSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = MediaDetails.objects.filter(isDeleted=False).order_by('createdAt')
            serializer = MediaDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Media Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status= status_code)


class MediaDetailAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = MediaDetailSerializer
    queryset = MediaDetails.objects.all()

    def get(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for mediaID = {pk}\n\n ")
        try:
            model =  MediaDetails.objects.get(mediaID=pk, isDeleted=False)
            serializer = MediaDetailSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Media data fetched successfully',
                'data': serializer.data
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)

class MediaDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = MediaDetails.objects.all()
    serializer_class = MediaSerializer

    def delete(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for mediaID = {pk}\n\n ")
        try:
            model = MediaDetails.objects.get(mediaID=pk)
            if model.isDeleted == True:
                status_code = http_status.NOT_FOUND
                response = {
                    'success':False,
                    "message": "Media detail Not Found",
                    "status_code": status_code
                }
                logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
            else:
                model.isDeleted = True
                model.save()
                status_code = http_status.OK
                response = {
                    "success":"true",
                    "message": "Data Deleted Successfully.",
                    "status_code": status_code
                }
                logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success':False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class MediaUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = MediaDetails.objects.all()
    serializer_class = MediaSerializer


    def put(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n mediaID = {pk}\n\n ")
        try:
            model =  MediaDetails.objects.get(mediaID=pk, isDeleted=False)
            serializer = MediaSerializer(model , data = request.data)
            if serializer.is_valid()== True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Media details Updated Successfully',
                    'data': serializer.data
                }
                logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    "status_code": http_status.BAD_REQUEST,
                    'message': 'something is wrong',
                }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")  
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
'error': str(e)
            }
            logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status= status_code)
