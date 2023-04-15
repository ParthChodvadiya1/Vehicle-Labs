import datetime
import logging

from datetime import timedelta
from re import search

from django.db.models import Count
from django.db.models.functions import TruncDate, ExtractMonth, ExtractYear

from rest_framework.response import Response
from rest_framework import generics, permissions, views
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *

from src.utils import http_status
from src.utils.validators import getDate
from src.utils.pagination import StandardResultsSetPagination
# from src.utils.exception import custom_exception_message
from src.apis.countersale.models import CounterSale, MinorServices
from rest_framework import filters
from django.db.models import Q
logger = logging.getLogger('watchtower-logger')


class CounterSaleRegisterAPIView(generics.CreateAPIView):
    queryset = CounterSale.objects.all()
    serializer_class = CounterSaleRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Counter sale successfully registered.",
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


class CounterSalePayment(generics.UpdateAPIView):
    queryset = CounterSale.objects.all()
    serializer_class = CounterSalePaymentSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n countersaleID = {request.data}\n\n ")
        try:
            obj = super().update(request, *args, **kwargs)
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


class CounterSaleCompleted(generics.UpdateAPIView):
    queryset = CounterSale.objects.all()
    serializer_class = CounterSaleCompletedSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n countersale = {request.data}\n\n ")
        try:
            obj = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Counter sale successfully comepleted.",
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


class CounterSaleList(generics.ListAPIView):
    queryset = CounterSale.objects.all()
    serializer_class = CounterSaleSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination


    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = CounterSale.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID')
            if request.GET.get('search'):

                search = request.GET.get('search')

                model = model.filter(Q(vehiclenumber__icontains=search) | Q(servicename__icontains=search) | Q(
                    serviceprice__icontains=search) | Q(cusID__cusname__icontains=search) | Q(cusID__cusemail__icontains=search) | Q(cusID__cusphone__icontains=search)) 

            serializer = CounterSaleSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Counter sale data fetched successfully',
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


class CounterSaleDetail(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = CounterSale.objects.all()
    serializer_class = CounterSaleSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for countersaleID = {pk}\n\n ")
        try:
            model = CounterSale.objects.get(countersaleID=pk, isDeleted=False)
            serializer = CounterSaleSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Counter sale fetched successfully',
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


class CounterSaleDetailbyUserIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = CounterSaleSerializer
    queryset = CounterSale.objects.all()
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            if createdAt:
                createdDate = datetime.datetime.strptime(
                    createdAt, '%Y-%m-%d').date()
                model = CounterSale.objects.filter(
                    userID=pk, isDeleted=False).filter(createdAt__icontains=createdDate).order_by('-createdAt')
            else:
                model = CounterSale.objects.filter(
                    userID=pk, isDeleted=False).order_by('-createdAt')
            if request.GET.get('search'):
    
                search = request.GET.get('search')

                model = model.filter(Q(vehiclenumber__icontains=search) | Q(servicename__icontains=search) | Q(
                    serviceprice__icontains=search) | Q(cusID__cusname__icontains=search) | Q(cusID__cusemail__icontains=search) | Q(cusID__cusphone__icontains=search))            
            model = model.prefetch_related('cusID')
            serializer = CounterSaleSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'counter sale data fetched successfully',
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


class CounterSaleDeleteAPIView(generics.DestroyAPIView):
    queryset = CounterSale.objects.all()
    serializer_class = CounterSaleSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for countersaleID = {pk}\n\n ")
        try:
            model = CounterSale.objects.get(countersaleID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "status_code": status_code,
                "message": "Data deleted successfully.",
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
        return Response(response, status_code)


class CounterSaleUpdateAPIView(generics.UpdateAPIView):
    queryset = CounterSale.objects.all()
    serializer_class = CounterSaleUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n data = {request.data}\n\n ")
        try:
            job_update = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Counter sale update successfully.',
                'data': request.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")

        except Exception as e:
            status_code = http_status.OK
            response = {
                "success": "False",
                "status_code": http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class CounterSaleCountbyDateRangeAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = CounterSaleDateSerializer
    queryset = CounterSale.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n userID = {pk} data = {request.data}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date() + timedelta(days=1)

            models = CounterSale.objects.filter(userID=pk, isDeleted=False)
            models = CounterSale.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                    'date').annotate(count=Count('countersaleID'))
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
                'message': 'Counter sale  count data by date fetched successfully',
                'data': bwt_date,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response} ")
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


class CounterSalebyMonthAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = CounterSaleSerializer
    queryset = CounterSale.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n userID = {pk}")
        try:
            model = CounterSale.objects.filter(userID=pk, isDeleted=False)
            my = [v for v in
                  model.annotate(month=ExtractMonth('createdAt'),
                                 year=ExtractYear('createdAt'),)
                  .order_by()
                  .values('month', 'year')
                  .annotate(total=Count('countersaleID'))
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

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Counter Sale count data by Month fetched successfully',
                'data': obj,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response} ")
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


class MinorServiceRegisterAPIView(generics.CreateAPIView):
    queryset = MinorServices.objects.all()
    serializer_class = MinorServiceSerializer
    permissions_classes = [permissions.AllowAny]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            fueltype_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Minor service registered.",
                'data': fueltype_obj.data
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


class MinorServiceListAPIView(generics.ListAPIView):
    queryset = MinorServices.objects.all()
    serializer_class = MinorServiceDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = MinorServices.objects.filter(
                isDeleted=False).order_by('-createdAt')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(mserviceName__icontains=search) | Q(mservicePrice__icontains=search))             
            serializer = MinorServiceDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Minor service Data fetched successfully',
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


class MinorServiceDetailAPIView(generics.RetrieveAPIView):
    queryset = MinorServices.objects.all()
    serializer_class = MinorServiceDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for mserviceID = {pk}\n\n ")
        try:
            model = MinorServices.objects.get(mserviceID=pk, isDeleted=False)
            status_code = http_status.OK
            serializer = MinorServiceDetailSerializer(model)
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Minor service Data fetched successfully',
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


class MinorServiceDeleteAPIView(generics.DestroyAPIView):
    queryset = MinorServices.objects.all()
    serializer_class = MinorServiceDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for mserviceID = {pk}\n\n ")
        try:
            model = MinorServices.objects.get(mserviceID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "message": "Data deleted successfully.",
                "status_code": status_code,
                "data": "no content"
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deleted data for mserviceID = {pk}\n\n ")

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


class MinorServiceUpdateAPIView(generics.UpdateAPIView):
    queryset = MinorServices.objects.all()
    serializer_class = MinorServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n mserviceID = {pk}\n\n ")
        try:
            model = MinorServices.objects.get(mserviceID=pk, isDeleted=False)
            serializer = MinorServiceSerializer(model, data=request.data)
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
