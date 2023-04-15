import logging

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from src.utils.exception import custom_exception_message
from src.apis.admininquiry.models import AdminInquiry
from src.utils import http_status
from src.utils.pagination import StandardResultsSetPagination

from .serializers import *

logger = logging.getLogger('watchtower-logger')

class AdminInquiryRegisterAPIView(generics.CreateAPIView):
    serializer_class = AdminInquiryRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = AdminInquiry.objects.all()

    def post(self, request, *args, **kwargs):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            inquiry_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success':True,
                'status_code': status_code,
                'message': "Request Successfully registered.",
                'data': request.data,
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")   
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

class AdminInquiryDetailAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = AdminInquiry.objects.all()
    serializer_class = AdminInquiryDetailSeriallizer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = AdminInquiry.objects.filter(isDeleted=False).order_by('-createdAt')
            serializer = AdminInquiryDetailSeriallizer(model, many=True)

            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")  
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

class AdminInquiryDetailByIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = AdminInquiry.objects.all()
    serializer_class = AdminInquiryDetailSeriallizer

    def get(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for inquiryID = {pk}\n\n ")
        try:
            model =  AdminInquiry.objects.get(inquiryID=pk, isDeleted=False)
          
            serializer = AdminInquiryDetailSeriallizer(model)
            status_code = http_status.OK    
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'data fetched successfully',
                'data': serializer.data
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")  
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

class AdminInquiryDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = AdminInquiry.objects.all()
    serializer_class = AdminInquiryDetailSeriallizer


    def delete(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for inquiryID = {pk}\n\n ")
        try:
            model = AdminInquiry.objects.get(inquiryID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                "success":"true",
                "status_code": status_code,
                "message": "Data Deleted Successfully.",
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")   

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

class AdminInquiryUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = AdminInquiry.objects.all()
    serializer_class = AdminInquiryDetailSeriallizer

    def put(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\nupdatation of inquiryID = {pk}\n\n ")
        try:
            model =  AdminInquiry.objects.get(inquiryID=pk, isDeleted=False)
            serializer = AdminInquiryDetailSeriallizer(model , data = request.data)
            if serializer.is_valid()== True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'details Updated Successfully',
                    'data': serializer.data
                }
                logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n ")  
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'something is wrong',
                }
                logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n ")  

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
