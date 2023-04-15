# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.utils import http_status
from src.apis.vendorcustomer.models import VendorCustomer

logger = logging.getLogger('watchtower-logger')



class VendorCustomerRegisterAPIView(generics.CreateAPIView):

    queryset = VendorCustomer.objects.all()
    serializer_class = VendorCustomerRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            ven_cus_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success':True,
                'status_code': status_code,
                'message': "vendor customer successfully registered.",
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


class VendorCustomerListAPIView(generics.ListAPIView):
    queryset = VendorCustomer.objects.all()
    serializer_class = VendorCustomerSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = VendorCustomer.objects.filter(isDeleted=False).order_by('createdAt')
            model = model.prefetch_related('cusID', 'vendorInventoryID','vendorInventoryID__partID','vendorInventoryID__vendorID', 'partID')
            serializer = VendorCustomerSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'data fetched successfully',
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


class VendorCustomerDetailAPIView(generics.RetrieveAPIView):
    queryset = VendorCustomer.objects.all()
    serializer_class = VendorCustomerSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorCustomerID = {pk}\n\n ")
        try:
            model =  VendorCustomer.objects.get(vendorCustomerID=pk, isDeleted=False)
            model = model.prefetch_related('cusID', 'vendorInventoryID','vendorInventoryID__partID','vendorInventoryID__vendorID', 'partID')
            status_code = http_status.OK
            serializer = VendorCustomerSerializer(model)
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'vendor customer fetched successfully',
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
        return Response(response, status= status_code)


class VendorCustomerDeleteAPIView(generics.DestroyAPIView):
    queryset = VendorCustomer.objects.all()
    serializer_class = VendorCustomerSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


    def delete(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for vendorCustomerID = {pk}\n\n ")
        try:
            model = VendorCustomer.objects.get(vendorCustomerID=pk, isDeleted=False)
            status_code = http_status.OK
            response = {
                'success':True,
                "status_code":status_code,
                "message": "Vendor customer deleted",
            }
            logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success':False,
                "status_code": http_status.OK,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response,status=status_code)


class VendorCustomerUpdateAPIView(generics.UpdateAPIView):
    queryset = VendorCustomer.objects.all()
    serializer_class = VendorCustomerSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for vendorCustomerID= {pk} \n\n ")
        try:
            model =  VendorCustomer.objects.get(vendorCustomerID=pk, isDeleted=False)
            serializer = VendorCustomerUpdateSerializer(model , data = request.data)
            if serializer.is_valid()== True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Vendor customer data Updated Successfully',
                    'data': serializer.data
                }
                logger.info(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Something is wrong',
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
        return Response(response, status= status_code)



class CustomerDelivered(generics.UpdateAPIView):
    queryset = VendorCustomer.objects.all()
    serializer_class = CustomerDeliveredSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data\n\n ")
        try:
            job_card_payment_obj = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success':True,
                'status_code': status_code,
                'message': "Inventory Order successfully Delivered.",
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
        
