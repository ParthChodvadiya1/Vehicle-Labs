# from src.utils.exception import custom_exception_message
from rest_framework.views import APIView
from src.utils.pagination import StandardResultsSetPagination
import ast
import logging
import http.client

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.apis.workshopinventory.models import WorkshopInventory
from src.utils import http_status
from src.utils.validators import send_otp
from src.apis.vendorcustomer.api.serializers import VendorCustomerSerializer
from src.apis.vendorcustomer.models import VendorCustomer
from src.apis.parts.models import ReuestPartPhoneOTP
from django.db.models import Q
conn = http.client.HTTPConnection("2factor.in")

logger = logging.getLogger('watchtower-logger')


class WorkshopInventoryRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopInventory.objects.all()
    serializer_class = WorkshopInventoryRegisterSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            wsinventory_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "WorkshopInventory successfully registered.",
                'data': wsinventory_obj.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e),
                # 'error':errors
            }
            # logger.error(f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class WorkshopRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopInventory.objects.all()
    serializer_class = WorkshopRegisterSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            workshop_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "WorkshopInventory successfully registered.",
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


class WorkshopInventoryListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopInventory.objects.all()
    serializer_class = WorkshopInventoryDetailSerializer
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = WorkshopInventory.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('vendorInventoryID', 'vendorInventoryID__vendorID', 'vendorInventoryID__partID', 'partID', 'vendorID', 'workshopID')

            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(vendorID__vendorname__icontains=search) | Q(vendorID__vendorphone__icontains=search) | Q(partID__partName__icontains=search) | Q(partID__partType__icontains=search) | Q(partID__partPrice__icontains=search) | Q(partID__rackNumber__icontains=search) | Q(partID__partNumber__icontains=search) | Q(partID__HSNNumber__icontains=search) | Q(partID__companyName__icontains=search) | Q(partID__vehicleModel__icontains=search) | Q(partID__modelNumber__icontains=search) | Q(partID__varient__icontains=search)) 
                               
            serializer = WorkshopInventoryDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Workshop Inventory Data fetched successfully',
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


class WorkshopInventoryDetailAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = WorkshopInventoryDetailSerializer
    queryset = WorkshopInventory.objects.all()
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for workshopID = {pk}\n\n ")
        try:
            model = WorkshopInventory.objects.filter(
                workshopID=pk, isDeleted=False, orderCompleted=True).order_by('-createdAt')
            model = model.prefetch_related('vendorInventoryID', 'vendorInventoryID__vendorID', 'vendorInventoryID__partID', 'partID', 'vendorID', 'workshopID')
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(vendorID__vendorname__icontains=search) | Q(vendorID__vendorphone__icontains=search) | Q(partID__partName__icontains=search) | Q(partID__partType__icontains=search) | Q(partID__partPrice__icontains=search) | Q(partID__partNumber__icontains=search) | Q(partID__HSNNumber__icontains=search) | Q(partID__companyName__icontains=search) | Q(partID__vehicleModel__icontains=search) | Q(partID__modelNumber__icontains=search) | Q(partID__varient__icontains=search))                
            
            serializer = WorkshopInventoryDetailSerializer(model, many=True)

            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Workshop Inventory fetched successfully',
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


class WorkshopInventoryVendorDetailAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = WorkshopInventoryDetailSerializer
    queryset = WorkshopInventory.objects.all()
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorID = {pk}\n\n ")
        try:
            model = WorkshopInventory.objects.filter(
                vendorID=pk, isDeleted=False, orderCompleted=False).order_by('-createdAt')
            model = model.prefetch_related('vendorInventoryID', 'vendorInventoryID__vendorID', 'vendorInventoryID__partID', 'partID', 'vendorID', 'workshopID')
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(vendorID__vendorname__icontains=search) | Q(vendorID__vendorphone__icontains=search) | Q(partID__partName__icontains=search) | Q(partID__partType__icontains=search) | Q(partID__partPrice__icontains=search) | Q(partID__rackNumber__icontains=search) | Q(partID__partNumber__icontains=search) | Q(partID__HSNNumber__icontains=search) | Q(partID__companyName__icontains=search) | Q(partID__vehicleModel__icontains=search) | Q(partID__modelNumber__icontains=search) | Q(partID__varient__icontains=search))                
                        
            serializer = WorkshopInventoryDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Workshop Inventory fetched successfully',
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


class WorkshopInventoryDetailbyVendorIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = WorkshopInventoryDetailSerializer
    queryset = WorkshopInventory.objects.all()
    querysetcustomer = VendorCustomer.objects.all()
    serializer_customer = VendorCustomerSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorID = {pk}\n\n ")
        try:
            model = WorkshopInventory.objects.filter(
                vendorID=pk, isDeleted=False).order_by('-createdAt')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(vendorID__vendorname__icontains=search) | Q(vendorID__vendorphone__icontains=search) | Q(partID__partName__icontains=search) | Q(partID__partType__icontains=search) | Q(partID__partPrice__icontains=search) | Q(partID__rackNumber__icontains=search) | Q(partID__partNumber__icontains=search) | Q(partID__HSNNumber__icontains=search) | Q(partID__companyName__icontains=search) | Q(partID__vehicleModel__icontains=search) | Q(partID__modelNumber__icontains=search) | Q(partID__varient__icontains=search))                
                        
            serializer = WorkshopInventoryDetailSerializer(model, many=True)

            model1 = VendorCustomer.objects.filter(
                vendorID=pk, isDeleted=False).order_by('-createdAt')
            serializer1 = VendorCustomerSerializer(model1, many=True)
            status_code = http_status.OK

            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Workshop Inventory data fetched successfully',
                'data': serializer.data+serializer1.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            # else:
            #     response= {
            #         'success': False,
            #         'status_code': http_status.BAD_REQUEST,
            #         'message': 'Workshop Inventory Details does not exists',
            #     }
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


class WorkshopInventoryDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopInventory.objects.all()
    serializer_class = WorkshopInventorySerializer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for workshopInventoryID = {pk}\n\n ")
        try:
            model = WorkshopInventory.objects.get(
                workshopInventoryID=pk, isDeleted=False)
            model.delete()
            status_code = http_status.OK
            response = {
                "success": "true",
                "status_code": http_status.OK,
                "message": "Data Deleted Successfully.",
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


class WorkshopInventoryUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = WorkshopInventory.objects.all()
    serializer_class = WorkshopInventorySerializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for workshopInventoryID = {pk}\n\n ")
        try:
            model = WorkshopInventory.objects.get(
                workshopInventoryID=pk, isDeleted=False)
            total = model.total
            requstedQty = request.data.get("workshopPartQty")
            requstedPrice = request.data.get("workshopPartPrice")
            model.total = float(requstedPrice) * int(requstedQty)
            model.due = (float(requstedPrice) * int(requstedQty)) - model.paid
            serializer = WorkshopInventorySerializer(model, data=request.data)
            if serializer.is_valid() == True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Workshop Inventory details Updated Successfully',
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


class WorkshopInventoryPartQtyAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = WorkshopInventoryDetailSerializer
    queryset = WorkshopInventory.objects.all()
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving quantity details for workshopID = {pk}\n\n ")
        try:
            model = WorkshopInventory.objects.filter(
                workshopID=pk, isDeleted=False)
            model = model.prefetch_related('partID')
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(vendorID__vendorname__icontains=search) | Q(vendorID__vendorphone__icontains=search) | Q(partID__partName__icontains=search) | Q(partID__partType__icontains=search) | Q(partID__partPrice__icontains=search) | Q(partID__rackNumber__icontains=search) | Q(partID__partNumber__icontains=search) | Q(partID__HSNNumber__icontains=search) | Q(partID__companyName__icontains=search) | Q(partID__vehicleModel__icontains=search) | Q(partID__modelNumber__icontains=search) | Q(partID__varient__icontains=search))                
                        
            
            serializer = WorkshopInventoryPartQtySerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Workshop Inventory  fetched successfully',
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


class WorkshopInventoryPayment(generics.UpdateAPIView):
    queryset = WorkshopInventory.objects.all()
    serializer_class = InventoryPaymentSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for payment\n\n ")
        try:
            job_card_payment_obj = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Payment successfully registered.",
                'data': request.data,
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


class InventoryOrderedCompleted(generics.UpdateAPIView):
    queryset = WorkshopInventory.objects.all()
    serializer_class = OrderedInventoryCompletedSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for order complete\n\n ")
        try:
            obj = super().update(request, *args, **kwargs)
            workshopInventoryID = request.data.get('workshopInventoryID')
            wp_obj = WorkshopInventory.objects.get(
                workshopInventoryID=workshopInventoryID)
            wp = wp_obj.workshopID
            wp_phone = wp.workshopphone
            wp_phone = str(wp_phone)
            otp = send_otp(wp_phone)
            phone_exist = ReuestPartPhoneOTP.objects.get(phone=wp_phone)
            if phone_exist:
                old = ReuestPartPhoneOTP.objects.update(
                    otp=otp
                )
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code': status_code,
                    'message': 'Inventory Order successfully comepleted. OTP sent successfully.'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                
            else:
                old = ReuestPartPhoneOTP.objects.update_or_create(
                    phone=wp_phone,
                    otp=otp,
                )
            # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=10c0f6a1-fd6e-11ea-9fa5-0200cd936042&to=" +
            #              wp_phone+"&otpvalue="+str(otp)+"&templatename=VLB")
            # res = conn.getresponse()

            # data = res.read()
            # data = data.decode("utf-8")
            # data = ast.literal_eval(data)
            # status_code = http_status.OK
            # if data["Status"] == 'Success':
            #     old.otp_session_id = data["Details"]
            #     old.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code': status_code,
                    'message': 'Inventory Order successfully comepleted. OTP sent successfully.'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                # return Response(response, status_code)
            # else:
            #     workshopInventoryID = request.data.get('workshopInventoryID')
            #     wpi_obj = WorkshopInventory.objects.get(
            #         workshopInventoryID=workshopInventoryID)
            #     wp_obj.orderCompleted = True
            #     status_code = http_status.OK
            #     response = {
            #         'success': False,
            #         'status_code': http_status.BAD_REQUEST,
            #         'message': 'Inventory Order successfully comepleted. OTP sending Failed.',
            #     }
            #     logger.info(
            #         f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            #     return Response(response, status=status_code)
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


class InventoryOrderedDelivered(generics.UpdateAPIView):
    queryset = WorkshopInventory.objects.all()
    serializer_class = OrderedInventoryDeliveredSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for delivery \n\n ")
        try:
            job_card_payment_obj = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Inventory Order successfully Delivered.",
                'data': request.data,
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
