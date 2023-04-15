# from src.utils.exception import custom_exception_message
from src.utils.pagination import StandardResultsSetPagination
import logging
import datetime

from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from src.apis.vendors.models import VendorDetail
from src.utils import http_status
from src.apis.vendorsalecard.models import VendorSaleCard, VendorPartSale
from src.apis.vendorsalecard.api.serializers import VendorSaleCardDetail, VendorPartSaleDetailSerializer

logger = logging.getLogger('watchtower-logger')


class VendorRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorDetail.objects.all()
    serializer_class = VendorSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            vendor_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Vendor created successfully.",
                'data': vendor_obj.data
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


class VendorListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorDetail.objects.all()
    serializer_class = VendorListSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = VendorDetail.objects.filter(
                isDeleted=False).order_by('-createdAt')
            serializer = VendorSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Vendor Data fetched successfully',
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


class VendorDetailAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = VendorSerializer
    queryset = VendorDetail.objects.all()

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = VendorDetail.objects.get(userID=pk, isDeleted=False)
            serializer = VendorSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Vendor fetched successfully',
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


class VendorDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorDetail.objects.all()
    serializer_class = VendorDetailSerializer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for vendorID = {pk}\n\n ")
        try:
            model = VendorDetail.objects.get(vendorID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                "success": "true",
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


class VendorUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorDetail.objects.all()
    serializer_class = VendorUpdateSerializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for vendorID = {pk} \n\n ")
        try:
            model = VendorDetail.objects.get(vendorID=pk, isDeleted=False)
            serializer = VendorUpdateSerializer(model, data=request.data)
            if serializer.is_valid() == True:
                serializer.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Vendor details Updated Successfully',
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


class VendorSalesLastFiveDataAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorSaleCard.objects.all()
    serializer_class = VendorSaleCardDetail
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving last five details for vendorID = {pk}\n\n ")
        try:
            model = VendorSaleCard.objects.filter(
                vendorID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('workshopID', 'cusID', 'partSaleID')
            model = list(model)[-5:]

            serializer = VendorSaleCardDetail(model, many=True)
            # for data in serializer.data:
            #     model1 = VendorPartSale.objects.filter(
            #         vendorsalecardID=data['vendorsalecardID'])
            #     serializer1 = VendorPartSaleDetailSerializer(model1, many=True)
            #     data['partsale'] = serializer1.data

            model2 = serializer.data
            model2 = sorted(
                model2, key=lambda x: x['createdAt'], reverse=True)[:5]
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'vendor data fetched successfully',
                'data': model2[:5]
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


class VendorSalesCountbyDateAPIView(generics.ListAPIView):

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
            model = VendorSaleCard.objects.filter(vendorID=pk, isDeleted=False)
            total_count = model.count()

            total_count1 = model.annotate(day=TruncDate('createdAt')).values(
                'day').annotate(c=Count('vendorsalecardID')).values('day', 'c')

            count1 = {
                'day': createdAt,
                'c': 0
            }
            count = list(total_count1)

            for item in count:
                if(item['day'] == createdDate):
                    count1 = item
                    break

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Sales data count by Date fetched successfully',
                'total_count': total_count,
                'data': count1,
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


class VendorSalesAmountbyDateAPIView(generics.ListAPIView):
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
            model = VendorSaleCard.objects.filter(vendorID=pk, isDeleted=False)
            modeldate = VendorSaleCard.objects.filter(
                vendorID=pk, isDeleted=False).filter(createdAt__icontains=createdDate)

            serializer = VendorSaleCardDetail(model, many=True)
            serializerdate = VendorSaleCardDetail(modeldate, many=True)

            total = [(data['total']) for data in serializer.data]

            paid = [(data['paid']) for data in serializer.data]

            due = [(data['due']) for data in serializer.data]

            count = {
                "day": createdAt,
                "total": sum([(data['total']) for data in serializerdate.data])
            }

            status_code = http_status.OK

            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Amount data by Date fetched successfully',
                'data': count,
                "total": sum(total),
                "paid": sum(paid),
                "due": sum(due)
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


class VendorManagerRegisterAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorManager.objects.all()
    serializer_class = VendorMangerRegisterSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            manager_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Vendor manager created successfully.",
                'data': manager_obj.data
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


class VendorManagerListAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorManager.objects.all()
    serializer_class = VendorManagerSerilizer
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = VendorManager.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('userID', 'usermanageID', 'vendorID')
            serializer = VendorManagerSerilizer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': ' Data fetched successfully',
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
    queryset = VendorManager.objects.all()
    serializer_class = VendorManagerSerilizer
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for vendorID = {pk}\n\n ")
        try:
            model = VendorManager.objects.filter(
                usermanageID=pk, isDeleted=False)
            model = model.prefetch_related('userID', 'usermanageID', 'vendorID')
            serializer = VendorManagerSerilizer(model, many=True)
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


class WorkshopManagerDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = VendorManager.objects.all()
    serializer_class = VendorManagerSerilizer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for usermanageID = {pk}\n\n ")
        try:
            model = VendorManager.objects.get(usermanageID=pk, isDeleted=False)
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
