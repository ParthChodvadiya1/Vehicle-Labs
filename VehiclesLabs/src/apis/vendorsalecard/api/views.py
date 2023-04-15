# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import datetime
import logging
import time
from collections import defaultdict
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.utils import http_status
from src.utils.validators import getDate, send_otp
from src.apis.parts.models import ReuestPartPhoneOTP
from src.apis.workshopinventory.models import WorkshopInventory
from src.apis.vendorsalecard.models import VendorSaleCard, VendorPartSale
from django.db.models import Q
logger = logging.getLogger('watchtower-logger')


class VendorSaleCardRegisterAPIView(generics.CreateAPIView):
    serializer_class = VendorSaleCardRegisterSerializer
    permissions_classes = [permissions.AllowAny]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorSaleCard.objects.all()

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            vendorsale_obj = self.create(request, *args, **kwargs)

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Vendor sale card created successfully.",
                'data': vendorsale_obj.data
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


class VendorSaleCardListAPIView(generics.ListAPIView):
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDetail
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = VendorSaleCard.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('partSaleID', 'workshopID', 'cusID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(saleType__icontains=search) | Q(
                    workshopID__workshopname__icontains=search) | Q(cusID__cusname__icontains=search))

            serializer = VendorSaleCardDetail(model, many=True)

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


class VendorSaleCardDetailAPIView(generics.ListAPIView):
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDetail
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorsalecardID = {pk}\n\n ")
        try:
            model = VendorSaleCard.objects.get(vendorsalecardID=pk)
            status_code = http_status.OK
            model = model.prefetch_related('partSaleID', 'workshopID', 'cusID')
            serializer = VendorSaleCardDetail(model)
            model1 = VendorPartSale.objects.filter(
                vendorsalecardID=pk).order_by('-createdAt')
            model = model.prefetch_related('partID', 'vendorInventoryID')
            serializer1 = VendorPartSaleDetailSerializer(model1, many=True)
            data = serializer.data
            data['partsale'] = serializer1.data

            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Data fetched successfully',
                'data': data
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


class VendorSaleCardDetailByVendorIDAPIView(generics.RetrieveAPIView):
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDetail
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorID = {pk}\n\n ")
        try:
            model = VendorSaleCard.objects.filter(
                vendorID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('partSaleID', 'workshopID', 'cusID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(saleType__icontains=search) | Q(
                    workshopID__workshopname__icontains=search) | Q(workshopID__workshopphone__icontains=search)  | Q(cusID__cusphone__icontains=search))            
            if request.GET.get('isDelivered'):
                if request.GET.get('isDelivered').title() == 'True':
                    model = model.filter(delivered=True)
                elif request.GET.get('isDelivered').title() == 'False':
                    model = model.filter(delivered=False)
            else:
                model = model
            serializer = VendorSaleCardDetail(model, many=True)
            # for data in serializer.data:
            #     model1 = VendorPartSale.objects.filter(
            #         vendorsalecardID=data['vendorsalecardID']).order_by('-createdAt')
            #     serializer1 = VendorPartSaleDetailSerializer(
            #         model1, many=True)
            #     data['partsale'] = serializer1.data
            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Data fetched successfully',
                'count': len(serializer.data),
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


class VendorSaleCardDeleteAPIView(generics.DestroyAPIView):
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDetail
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for vendorsalecardID = {pk}\n\n ")
        try:
            model = VendorSaleCard.objects.get(vendorsalecardID=pk)
            if model.isDeleted == True:
                status_code = http_status.OK
                response = {
                    'success': False,
                    "status_code": http_status.BAD_REQUEST,
                    "message": "Vendor Sale Card not found",
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                model.isDeleted = True
                model.save()
                model1 = VendorPartSale.objects.filter(vendorsalecardID=pk)
                serializer1 = VendorPartSaleDetailSerializer(model1, many=True)
                for data in serializer1.data:
                    model2 = VendorInventory.objects.get(
                        vendorInventoryID=data['vendorInventoryID'])
                    model2.vendorPartQty = model2.vendorPartQty + \
                        data['partQty']
                    model2.save()

                status_code = http_status.OK
                response = {
                    'success': True,
                    "message": "Data deleted successfully.",
                    "status_code": status_code,
                    "data": "no content"
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


class VendorSaleCardUpdateAPIView(generics.UpdateAPIView):
    queryset = VendorPartSale.objects.all()
    serializer_class = VendorSaleCardUpdeateSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for vendorsalecardID = {pk} \n\n ")
        try:
            model = VendorPartSale.objects.get(
                vendorsalecardID=pk, partID=request.data.get('partID'))
            serializer = VendorSaleCardUpdeateSerializer(
                model, data=request.data)
            if serializer.is_valid() == True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Data Updated Successfully',
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


class VendorSaleCardPaymentAPIView(generics.UpdateAPIView):
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardPaymentSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data payment\n\n ")
        try:
            payment_obj = super().update(request, *args, **kwargs)
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
                'message': "Something is wrong",
                "error": str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class VendorSaleCardPartRegisterAPIView(generics.CreateAPIView):
    serializer_class = VendorPartSaleRegisterSerializer
    permissions_classes = [permissions.AllowAny]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorPartSale.objects.all()

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            vendorsale_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Vendor sale part created successfully.",
                'data': vendorsale_obj.data
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


class SaleCardbyDateAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = VendorSaleCardDetail
    queryset = VendorSaleCard.objects.all()
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            createdDate = datetime.datetime.strptime(
                createdAt, '%Y-%m-%d').date()
            model = VendorSaleCard.objects.filter(
                vendorID=pk, isDeleted=False).filter(createdAt__icontains=createdDate).order_by('-createdAt')
            serializer = VendorSaleCardDetail(model, many=True)

            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Salecard count data by Date fetched successfully',
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


class VendorSaleCardPartListAPIView(generics.ListAPIView):
    queryset = VendorPartSale.objects.all()
    serializer_class = VendorPartSaleDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = VendorPartSale.objects.filter(
                isDeleted=False).order_by('createdAt')
            model = model.prefetch_related('partID', 'vendorInventoryID', 'vendorInventoryID__partID', 'vendorInventoryID__vendorID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter( Q(partID__partName__icontains=search) | Q(partID__partType__icontains=search)  | Q(partID__companyName__icontains=search))            
            
            
            serializer = VendorPartSaleDetailSerializer(model, many=True)
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


class VendorSaleCardPartDetailAPIView(generics.RetrieveAPIView):
    queryset = VendorPartSale.objects.all()
    serializer_class = VendorPartSaleDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorPartSaleID = {pk}\n\n ")
        try:
            model = VendorPartSale.objects.get(vendorPartSaleID=pk)
            if model.isDeleted == False:
                model = VendorPartSale.objects.get(vendorPartSaleID=pk)
                model = model.prefetch_related('partID', 'vendorInventoryID', 'vendorInventoryID__partID', 'vendorInventoryID__vendorID')
                serializer = VendorPartSaleDetailSerializer(model)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Data fetched successfully',
                    'data': serializer.data
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Details does not exists',
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


class VendorSaleCardPartDeleteAPIView(generics.DestroyAPIView):
    queryset = VendorPartSale.objects.all()
    serializer_class = VendorPartSaleDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for vendorPartSaleID = {pk}\n\n ")
        try:
            model = VendorPartSale.objects.get(
                vendorPartSaleID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "status_code": status_code,
                "message": "Data deleted successfully."
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


class VendorSaleCardPartUpdateAPIView(generics.UpdateAPIView):
    queryset = VendorPartSale.objects.all()
    serializer_class = VendorPartSaleDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for vendorPartSaleID = {pk} \n\n ")
        try:
            model = VendorPartSale.objects.get(vendorPartSaleID=pk)
            if model.isDeleted == False:
                model = VendorPartSale.objects.get(vendorPartSaleID=pk)
                serializer = VendorPartSaleDetailSerializer(
                    model, data=request.data)
                if serializer.is_valid() == True:
                    serializer.save()
                    status_code = http_status.OK
                    response = {
                        'success': True,
                        'status_code':  status_code,
                        'message': 'Data Updated Successfully',
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
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'details does not exists',
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


class VendorsalePartsByCardID(generics.ListAPIView):
    queryset = VendorPartSale.objects.all()
    serializer_class = VendorPartSaleDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorsalecardID = {pk}\n\n ")
        try:
            model = VendorPartSale.objects.filter(
                vendorsalecardID=pk, isDeleted=False)
            model = model.prefetch_related('partID', 'vendorInventoryID', 'vendorInventoryID__partID', 'vendorInventoryID__vendorID')
            status_code = http_status.OK
            serializer = VendorPartSaleDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Data fetched successfully',
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


class VendorSaleCardDelivered(generics.UpdateAPIView):
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDeliveredSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data\n\n ")
        try:

            wp_phone = request.data.get('workshopphone')
            otp_sent = request.data.get('otp')
            wp_phone = str(wp_phone)
            otp = send_otp(wp_phone)
            old = ReuestPartPhoneOTP.objects.filter(
                phone__iexact=wp_phone,
            )
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    vendorsalecard_delivered_obj = super().update(request, *args, **kwargs)
                    old.validated == True,
                    old.save()
                    status_code = http_status.OK
                    response = {
                        'success': True,
                        'status_code': http_status.ACCEPTED,
                        'message': 'Order successfully Delivered, OTP matched.',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                else:
                    status_code = http_status.OK
                    response = {
                        'success': False,
                        'status_code': http_status.BAD_REQUEST,
                        'message': 'OTP incorect, please try again to deliver order.',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'status_code': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Enter valid phone number.',
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


class VendorSaleCardCountbyDateRangeAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = VendorSaleCardDetail
    queryset = VendorSaleCard.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date() + datetime.timedelta(days=1)

            models = VendorSaleCard.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                'date').annotate(count=Count('vendorsalecardID'))

            models = list(models)
            bwt_date = getDate(startDate, endDate)
            for i in bwt_date:
                for d in models:
                    if (d['date'] == i['date']):
                        i['count'] = d['count']

            status_code = http_status.OK

            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'sale card  count data by Date fetched successfully',
                'data': bwt_date,
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


class VenorSaleCustomerCountbyDateRangeAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDetail

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date() + datetime.timedelta(days=1)
            job_count = VendorSaleCard.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                    'date').annotate(count=Count('cusID'))

            job_count = list(job_count)

            model = job_count

            c = defaultdict(int)

            for item in model:
                c[item['date']] += item['count']

            model = [{"date": obj, "count": c[obj]} for obj in c]

            bwt_date = getDate(startDate, endDate)
            for i in bwt_date:
                for d in model:
                    if (d['date'] == i['date']):
                        i['count'] = d['count']

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Customer count data by date fetched successfully',
                'data': bwt_date,
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


class SaleCardbyMonthAPIView(generics.CreateAPIView):

    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = VendorSaleCardDetail
    queryset = VendorSaleCard.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = VendorSaleCard.objects.filter(userID=pk, isDeleted=False)
            my = [v for v in
                  model.annotate(month=ExtractMonth('createdAt'),
                                 year=ExtractYear('createdAt'),)
                  .order_by()
                  .values('month', 'year')
                  .annotate(total=Count('vendorsalecardID'))
                  .values('month', 'year', 'total')
                  ]
            obj = []
            year = request.data.get('year')
            for data in my:
                if(int(year) == data['year']):
                    obj.append(data)
            for i in range(1, 13):
                if i not in [data['month'] for data in obj]:
                    obj.append({'month': i, "total": 0, "year": int(year)})
            newlist = sorted(obj, key=lambda k: k['month'])
            obj = []
            for data in newlist:
                data['month'] = datetime.datetime.strptime(
                    str(data['month']), "%m").strftime("%b")
                obj.append(data)
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Sale card  count data by Month fetched successfully',
                'data': obj,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=http_status.OK)


class SaleCardCustomerbyMonthAPIView(generics.CreateAPIView):

    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = VendorSaleCardDetail
    queryset = VendorSaleCard.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:

            job_count = [v for v in
                         VendorSaleCard.objects.filter(userID=pk, isDeleted=False).annotate(month=ExtractMonth('createdAt'),
                                                                                            year=ExtractYear('createdAt'),)
                         .order_by()
                         .values('month', 'year')
                         .annotate(total=Count('vendorsalecardID'))
                         .values('month', 'year', 'total')
                         ]

            model = job_count
            c = defaultdict(int)

            obj = []
            year = request.data.get('year')
            for data in model:
                if(int(year) == data['year']):
                    obj.append(data)

            for item in obj:
                c[item['month']] += item['total']

            obj = [{"month": obj, "total": c[obj],
                    "year":int(year)} for obj in c]

            for i in range(1, 13):
                if i not in [data['month'] for data in obj]:
                    obj.append({'month': i, "total": 0, "year": int(year)})
            newlist = sorted(obj, key=lambda k: k['month'])
            obj = []
            for data in newlist:
                data['month'] = datetime.datetime.strptime(
                    str(data['month']), "%m").strftime("%b")
                obj.append(data)
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Jobcard  count data by Month fetched successfully',
                'data': obj,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=http_status.OK)
