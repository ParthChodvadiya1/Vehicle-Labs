from src.utils.pagination import StandardResultsSetPagination
import datetime
import locale
import logging

from datetime import timedelta
from django.db.models import Count, Sum, Q
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate
from django.http import HttpResponse
from django.views.generic import View
from collections import defaultdict

from .serializers import *
from src.utils import http_status
from src.utils.validators import getDate
# from src.utils.exception import custom_exception_message
from src.apis.customer.models import CustomerDetail
from src.apis.jobcards.models import JobCardDetail, JobcardServices, JobcardParts
from src.apis.vehicles.models import VehiclesDetail
from src.apis.workshop.models import WorkshopDetail
from src.apis.fueltype.models import fueltype
from src.apis.jobcards.models import JobCardDetail, JobcardServices, JobcardParts, WorkshopCustomer
from src.utils.pdfgenerator import render_to_pdf
from src.apis.countersale.models import CounterSale
from src.apis.customer.api.serializers import CustomerSerializer

from rest_framework import generics, permissions, views
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


logger = logging.getLogger('watchtower-logger')


class RegisterAPIView(generics.CreateAPIView):
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardRegisterSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            job_card_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Job card successfully registered.",
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class WorkshopCustomerbyUserIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = WorkshopCustomer
    queryset = JobCardDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = WorkshopCustomer.objects.filter(
                userID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(cusID__cusname__icontains=search) | Q(cusID__cusphone__icontains=search) | Q(cusID__cusemail__icontains=search))            
            serializer = WorkshopCustomerbyUserIDSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Workshop Customers data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardPayment(generics.UpdateAPIView):
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardPaymentSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n jobcard = {request.data}\n\n ")
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
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class JobCardCompleted(generics.UpdateAPIView):
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardCompletedSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n jobcard = {request.data}\n\n ")
        try:
            job_card_payment_obj = super().update(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Job card successfully comepleted.",
                'data': request.data,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardList(generics.ListAPIView):
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]    
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = JobCardDetail.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'fueltypeID', 'vehicleID', 'brandID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(brandID__brandmodel__icontains=search) | Q(fueltypeID__fueltype__icontains=search) | Q(vehicleID__vehiclenumber__icontains=search) | Q(cusID__cusname__icontains=search) | Q(cusID__cusphone__icontains=search))            
            serializer = JobCardSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Job Card Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardDetails(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardSerializer
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for jobID = {pk}\n\n ")
        try:
            model = JobCardDetail.objects.get(jobID=pk, isDeleted=False)
            serializer = JobCardSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Job Card fetched successfully',
                'data': serializer.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardDetailbyUserIDAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            if createdAt:
                createdDate = datetime.datetime.strptime(
                    createdAt, '%Y-%m-%d').date()
                model = JobCardDetail.objects.filter(
                    userID=pk, isDeleted=False).filter(createdAt__icontains=createdDate).order_by('-createdAt')
            else:
                model = JobCardDetail.objects.filter(
                    userID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'fueltypeID', 'vehicleID', 'brandID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(brandID__brandmodel__icontains=search) | Q(fueltypeID__fueltype__icontains=search) | Q(vehicleID__vehiclenumber__icontains=search) | Q(cusID__cusname__icontains=search) | Q(cusID__cusphone__icontains=search))
            isCompleted = request.GET.get('isCompleted')
            if isCompleted:
                if isCompleted.title() == 'True':
                    model = model.filter(isCompleted=True)
                elif isCompleted.title() == 'False':
                    model = model.filter(isCompleted=False)
            else:
                model = model
            
            serializer = JobCardSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Jobcard  data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardbyDateDetailsAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            createdDate = datetime.datetime.strptime(
                createdAt, '%Y-%m-%d').date()
            model = JobCardDetail.objects.filter(
                userID=pk, isDeleted=False).filter(createdAt__icontains=createdDate).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'fueltypeID', 'vehicleID', 'brandID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(brandID__brandmodel__icontains=search) | Q(fueltypeID__fueltype__icontains=search) | Q(vehicleID__vehiclenumber__icontains=search) | Q(cusID__cusname__icontains=search) | Q(cusID__cusphone__icontains=search))            
            isCompleted = request.GET.get('isCompleted')
            if isCompleted:
                if isCompleted.title() == 'True':
                    model = model.filter(isCompleted=True)
                elif isCompleted.title() == 'False':
                    model = model.filter(isCompleted=False)
            else:
                model = model            
            serializer = JobCardSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Jobcard  count data by Date fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardbyDateAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            createdDate = datetime.datetime.strptime(
                createdAt, '%Y-%m-%d').date()
            model = JobCardDetail.objects.filter(
                userID=pk, isDeleted=False).filter(createdAt__icontains=createdDate).order_by('-createdAt')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(brandID__brandmodel__icontains=search) | Q(fueltypeID__fueltype__icontains=search) | Q(vehicleID__vehiclenumber__icontains=search) | Q(cusID__cusname__icontains=search) | Q(cusID__cusphone__icontains=search))            
            isCompleted = request.GET.get('isCompleted')
            if isCompleted:
                if isCompleted.title() == 'True':
                    model = model.filter(isCompleted=True)
                elif isCompleted.title() == 'False':
                    model = model.filter(isCompleted=False)
            else:
                model = model
            serializer = JobCardSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data            
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Jobcard  count data by Date fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Data details : {serializer.data}\n\n ")
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


class JobCardbyMonthAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            model = JobCardDetail.objects.filter(userID=pk, isDeleted=False)
            my = [v for v in
                  model.annotate(month=ExtractMonth('createdAt'),
                                 year=ExtractYear('createdAt'),)
                  .order_by()
                  .values('month', 'year')
                  .annotate(total=Count('jobID'))
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
                'status_code':  status_code,
                'message': 'Jobcard  count data by Month fetched successfully',
                'data': obj,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardCountbyDateRangeAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date() + timedelta(days=1)

            models = JobCardDetail.objects.filter(userID=pk, isDeleted=False)

            models = JobCardDetail.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                'date').annotate(count=Count('jobID'))

            models = list(models)
            bwt_date = getDate(startDate, endDate)
            for i in bwt_date:
                for d in models:
                    if (d['date'] == i['date']):
                        i['count'] = d['count']

            status_code = http_status.OK

            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Jobcard  count data by Date fetched successfully',
                'data': bwt_date,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardCountbyDateAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            createdDate = datetime.datetime.strptime(
                createdAt, '%Y-%m-%d').date()
            model = JobCardDetail.objects.filter(userID=pk, isDeleted=False)
            total_count = model.count()
            total_count1 = model.annotate(day=TruncDate('createdAt')).values(
                'day').annotate(c=Count('jobID')).values('day', 'c')
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
                'status_code':  status_code,
                'message': 'Jobcard  count data by Date fetched successfully',
                'total_count': total_count,
                'data': count1,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardLastAmountbyDateAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            createdAt = request.GET.get('createdAt')
            createdDate = datetime.datetime.strptime(
                createdAt, '%Y-%m-%d').date()
            obj = JobCardDetail.objects.filter(userID=pk, isDeleted=False)
            obj1 = CounterSale.objects.filter(userID=pk, isDeleted=False)

            if obj:
                total = 0
                paid = 0
                due = 0
                total_count = obj.annotate(day=TruncDate('createdAt')).values('day').annotate(total=Sum(
                    'total')).annotate(paid=Sum('paid')).annotate(due=Sum('due')).values('day', 'total', 'paid', 'due')

                total_count1 = obj1.annotate(day=TruncDate('createdAt')).values(
                    'day').annotate(total=Sum('serviceprice')).values('day', 'total')
                count_total = list(total_count) + list(total_count1)

                c = defaultdict(int)

                for item in count_total:
                    c[item['day']] += item['total']
                    total += item['total']
                    if('paid' in item.keys()):
                        paid += item['paid']
                        due += item['due']
                    else:
                        paid += item['total']

                data = {
                    'day': createdDate,
                    'total': c[createdDate]
                }
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Jobcard  count data by Date fetched successfully',
                    'data': data,
                    "total": total,
                    "paid": paid,
                    "due": due
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Jobcard  Details does not exists',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")

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


class JobCardDeleteAPIView(generics.DestroyAPIView):
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for ID = {pk}\n\n ")
        try:
            model = JobCardDetail.objects.get(jobID=pk, isDeleted=False)
            model.isDeleted = True
            model.save()
            status_code = http_status.OK
            response = {
                'success': True,
                "status_code": http_status.BAD_REQUEST,
                "message": "Data deleted successfully.",
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")

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


class JobCardUpdateAPIView(generics.UpdateAPIView):
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating jobcard data :{request.data}\n\n ")
        try:
            job_update = super().update(request, *args, **kwargs)

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Job card update successfully.',
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
        except Exception as e:
            status_code = http_status.OK
            response = {
                "success": "False",
                "status_code": http_status.NOT_FOUND,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class JobCardLastFiveDataAPIView(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardSerializer
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n userID = {pk}\n\n ")
        try:
            model = JobCardDetail.objects.filter(
                userID=pk, isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('cusID', 'fueltypeID', 'vehicleID', 'brandID')
            if model:
                model = list(model)[-5:][::-1]
                serializer = JobCardSerializer(model, many=True)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Jobcard  data fetched successfully',
                    'data': serializer.data
                }
            else:
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  status_code,
                    'message': 'Jobcard  details does not exists.'
                }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardServicesAPIView(generics.CreateAPIView):
    queryset = JobcardServices.objects.all()
    serializer_class = JobcardServicesSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            job_card_service_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Job card Services successfully registered.",
                'data': request.data,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardServicesDetail(generics.ListAPIView):
    queryset = JobcardServices.objects.all()
    serializer_class = JobcardServicesDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = JobcardServices.objects.filter(isDeleted=False)
            model = model.prefetch_related('serviceID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(serviceID__serviceName__icontains=search) | Q(serviceID__serviceType__icontains=search))            
            serializer = JobcardServicesDetailSerializer(model, many=True)
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
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n ")
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


class JobCardServiceDetailAPIView(generics.ListAPIView):

    queryset = JobcardServices.objects.all()
    serializer_class = JobcardServicesDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details ")
        try:
            model = JobcardServices.objects.filter(jobID=pk, isDeleted=False)
            model = model.prefetch_related('serviceID')
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(serviceID__serviceName__icontains=search) | Q(serviceID__serviceType__icontains=search))                        
            serializer = JobcardServicesDetailSerializer(model, many=True)
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
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardServicesDeleteAPIView(generics.DestroyAPIView):
    queryset = JobcardServices.objects.all()
    serializer_class = JobcardServicesDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for jobcardServidesID = {pk}\n\n ")
        try:
            model = JobcardServices.objects.get(jobcardServidesID=pk)
            jobid = model.jobID.jobID
            job = JobCardDetail.objects.get(jobID=jobid)

            reduceAmount = model.servicePrice
            initialAmount = job.totalServiceAmount
            finalAmount = initialAmount - reduceAmount

            job.totalServiceAmount = finalAmount
            job.total -= reduceAmount
            job.newTotal -= reduceAmount
            job.save()

            if model.isDeleted == True:
                status_code = http_status.OK
                response = {
                    'success': False,
                    "status_code": status_code,
                    "message": "Jobcard service details not found",
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
            else:
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
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")

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


class JobCardServicesUpdateAPIView(generics.UpdateAPIView):
    queryset = JobcardServices.objects.all()
    serializer_class = JobcardServicesDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n jobcardServidesID = {pk}\n\n ")
        try:
            model = JobcardServices.objects.get(jobcardServidesID=pk)
            if model.isDeleted == False:
                model = JobcardServices.objects.get(jobcardServidesID=pk)

                initial_servicePrice = model.servicePrice
                serializer = JobcardServicesDetailSerializer(
                    model, data=request.data)
                jobID = request.data.get("jobID")
                obj = JobCardDetail.objects.get(jobID=jobID)

                initial_total = obj.totalServiceAmount
                (initial_total)
                servicePrice = request.data.get("servicePrice")

                servicePrice = int(servicePrice)
                final_amount = initial_total + \
                    (servicePrice - initial_servicePrice)
                obj.totalServiceAmount = final_amount

                obj.total = final_amount + obj.totalPartsAmount

                obj.newTotal = final_amount + obj.totalPartsAmount - obj.discountAmount
                obj.due = (final_amount + obj.totalPartsAmount) - obj.paid

                obj.save()

                if serializer.is_valid() == True:
                    serializer.save()
                    status_code = http_status.OK
                    response = {
                        'success': True,
                        'status_code':  status_code,
                        'message': 'Jobcard service Data Updated Successfully',
                        'data': serializer.data
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
                else:
                    status_code = http_status.OK
                    response = {
                        'success': False,
                        'status_code': http_status.BAD_REQUEST,
                        'message': 'something is wrong',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Jobcard service details does not exists'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardPartsAPIView(generics.CreateAPIView):
    queryset = JobcardParts.objects.all()
    serializer_class = JobcardPartsSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n  ")
        try:
            job_card_service_obj = self.create(request, *args, **kwargs)

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Job card Parts successfully registered.",
                'data': request.data,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardPartsDetail(generics.ListAPIView):
    queryset = JobcardParts.objects.all()
    serializer_class = JobcardPartsDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = JobcardParts.objects.filter(isDeleted=False)
            model = model.prefetch_related('workshopInventoryID', 'workshopInventoryID__workshopID', 'workshopInventoryID__vendorInventoryID', 'workshopInventoryID__vendorInventoryID__partID', 'workshopInventoryID__vendorInventoryID__vendorID', 'workshopInventoryID__partID', 'workshopInventoryID__vendorID')
            serializer = JobcardPartsDetailSerializer(model, many=True)
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
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardPartsDetailAPIView(generics.ListAPIView):
    queryset = JobcardParts.objects.all()
    serializer_class = JobcardPartsDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details ")
        try:
            model = JobcardParts.objects.filter(jobID=pk, isDeleted=False)
            model = model.prefetch_related('workshopInventoryID', 'workshopInventoryID__workshopID', 'workshopInventoryID__vendorInventoryID', 'workshopInventoryID__vendorInventoryID__partID', 'workshopInventoryID__vendorInventoryID__vendorID', 'workshopInventoryID__partID', 'workshopInventoryID__vendorID')
            serializer = JobcardPartsDetailSerializer(model, many=True)
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
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class JobCardPartsDeleteAPIView(generics.DestroyAPIView):
    queryset = JobcardParts.objects.all()
    serializer_class = JobcardPartsDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for jobcardPartsID = {pk}\n\n ")
        try:
            model = JobcardParts.objects.get(jobcardPartsID=pk)
            jobid = model.jobID.jobID
            job = JobCardDetail.objects.get(jobID=jobid)

            reduceprice = model.partsPrice
            reduceQty = model.partQty
            reduceAmount = reduceprice * reduceQty
            initialAmount = job.totalPartsAmount
            finalAmount = initialAmount - reduceAmount

            job.totalPartsAmount = finalAmount
            job.total -= reduceAmount
            job.newTotal -= reduceAmount
            job.save()

            if model.isDeleted == True:
                status_code = http_status.OK
                response = {
                    'success': False,
                    "status_code": http_status.BAD_REQUEST,
                    "message": "Jobcard parts details not found",
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
            else:
                model.isDeleted = True
                model.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    "message": "Data deleted successfully.",
                    "status_code": status_code
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")

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


class JobCardPartsUpdateAPIView(generics.UpdateAPIView):
    queryset = JobcardParts.objects.all()
    serializer_class = JobcardPartsDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n jobcardPartsID = {pk}\n\n ")
        try:
            model = JobcardParts.objects.get(jobcardPartsID=pk)

            initial_PartQty = model.partQty
            initial_PartPrice = model.partsPrice
            initial_partTotal = initial_PartPrice * initial_PartQty

            jobID = request.data.get("jobID")
            obj = JobCardDetail.objects.get(jobID=jobID)
            db_partTotal = obj.totalPartsAmount
            partQty = request.data.get("partQty")
            partsPrice = request.data.get("partsPrice")
            partQty = int(partQty)
            partsPrice = int(partsPrice)

            partTotal = partQty * partsPrice

            final_amount = db_partTotal + (partTotal - initial_partTotal)

            obj.totalPartsAmount = final_amount
            obj.total = final_amount + obj.totalServiceAmount
            obj.newTotal = final_amount + obj.totalServiceAmount - obj.discountAmount
            obj.due = (final_amount + obj.totalServiceAmount) - obj.paid
            obj.save()

            if model.isDeleted == False:
                model = JobcardParts.objects.get(jobcardPartsID=pk)
                serializer = JobcardPartsDetailSerializer(
                    model, data=request.data)
                if serializer.is_valid() == True:
                    serializer.save()
                    status_code = http_status.OK
                    response = {
                        'success': True,
                        'status_code':  status_code,
                        'message': 'Jobcard parts Data Updated Successfully',
                        'data': serializer.data
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
                else:
                    status_code = http_status.OK
                    response = {
                        'success': False,
                        'status_code': http_status.BAD_REQUEST,
                        'message': 'something is wrong',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Jobcard service details does not exists'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class GeneratePdf(View):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = JobCardDetail.objects.all()
    serializer_class = JobCardDetailSerializer

    def get(self, request, pk):

        model = JobCardDetail.objects.get(jobID=pk, isDeleted=False)
        locale.setlocale(locale.LC_ALL, 'en_IN')
        totalPartsAmount = locale.format(
            "%d", model.totalPartsAmount, grouping=True)
        totalServiceAmount = locale.format(
            "%d", model.totalServiceAmount, grouping=True)
        total = locale.format("%d", model.total, grouping=True)
        createddate = model.createdAt

        userID = model.userID.userID
        workshop = WorkshopDetail.objects.get(userID=userID, isDeleted=False)

        cusID = model.cusID.cusID
        customer = CustomerDetail.objects.get(cusID=cusID, isDeleted=False)

        vehicleID = model.vehicleID.vehicleID
        vehicle = VehiclesDetail.objects.get(
            vehicleID=vehicleID, isDeleted=False)

        fuelID = model.fueltypeID.fuelID
        fueltypes = fueltype.objects.get(fuelID=fuelID, isDeleted=False)
        fuelname = fueltypes.fueltype

        JobcardService = []
        jobID = pk
        jobcardservice = JobcardServices.objects.filter(
            jobID=pk, isDeleted=False)
        jsserializer = JobcardServicesSerializer(jobcardservice, many=True)
        for serviceID in jobcardservice:
            servicename = serviceID.serviceID.serviceName
            servicetype = serviceID.serviceID.serviceType
            serviceprice = locale.format(
                "%d", serviceID.servicePrice, grouping=True)
            JobcardService.append(
                {"servicename": servicename, "servicetype": servicetype, "serviceprice": serviceprice})

        JobcardPart = []
        jobcardpart = JobcardParts.objects.filter(jobID=pk, isDeleted=False)
        jpserializer = JobcardPartsSerializer(jobcardpart, many=True)
        for jobcardPartsID in jobcardpart:
            partname = jobcardPartsID.workshopInventoryID.partID.partName
            parttype = jobcardPartsID.workshopInventoryID.partID.partType
            partqty = jobcardPartsID.partQty
            partprice = locale.format(
                "%d", jobcardPartsID.partsPrice, grouping=True)
            JobcardPart.append({"partname": partname, "parttype": parttype,
                                "partqty": partqty, "partprice": partprice})

        data = {
            'totalPartsAmount': totalPartsAmount,
            'totalServiceAmount': totalServiceAmount,
            'total': total,
            'createddate': createddate,
            'workshop': workshop,
            'customer': customer,
            'vehicle': vehicle,
            'fueltype': fuelname,
            'jobcardServices': JobcardService,
            'jobcardParts': JobcardPart,
        }

        pdf = render_to_pdf('index.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class CustomerCountbyDateRangeAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerSerializer

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date() + timedelta(days=1)
            models = CustomerDetail.objects.filter(userID=pk, isDeleted=False)

            job_count = JobCardDetail.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                    'date').annotate(count=Count('cusID'))

            counter_sale_count = CounterSale.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                    'date').annotate(count=Count('cusID'))

            job_count = list(job_count)

            counter_sale_count = list(counter_sale_count)

            model = job_count + counter_sale_count

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
                'message': 'Customer count data by Date Customer fetched successfully',
                'data': bwt_date,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class NewCustomerCountbyDateRangeAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerSerializer
    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date() + timedelta(days=1)
            models = CustomerDetail.objects.filter(userID=pk, isDeleted=False)

            job_count = WorkshopCustomer.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                    'date').annotate(count=Count('cusID'))

            job_count = list(job_count)

            c = defaultdict(int)

            for item in job_count:
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
                'message': 'New Customer count data by Date Customer fetched successfully',
                'data': bwt_date,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class CustomerbyMonthAPIView(views.APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            model = JobCardDetail.objects.filter(userID=pk, isDeleted=False)

            job_count = [v for v in
                         JobCardDetail.objects.filter(userID=pk, isDeleted=False).annotate(month=ExtractMonth('createdAt'),
                                                                                           year=ExtractYear('createdAt'),)
                         .order_by()
                         .values('month', 'year')
                         .annotate(total=Count('jobID'))
                         .values('month', 'year', 'total')
                         ]

            counter_sale_count = [v for v in
                                  CounterSale.objects.filter(userID=pk, isDeleted=False).annotate(month=ExtractMonth('createdAt'),
                                                                                                  year=ExtractYear('createdAt'),)
                                  .order_by()
                                  .values('month', 'year')
                                  .annotate(total=Count('countersaleID'))
                                  .values('month', 'year', 'total')
                                  ]

            model = job_count + counter_sale_count
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
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'Jobcard  count data by Month fetched successfully',
                'data': obj,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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


class NewCustomerbyMonthAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = JobCardSerializer
    queryset = JobCardDetail.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details userID = {pk}\n\n ")
        try:
            model = WorkshopCustomer.objects.filter(userID=pk, isDeleted=False)

            job_count = [v for v in
                         WorkshopCustomer.objects.filter(userID=pk, isDeleted=False).annotate(month=ExtractMonth('createdAt'),
                                                                                              year=ExtractYear('createdAt'),)
                         .order_by()
                         .values('month', 'year')
                         .annotate(total=Count('cusID'))
                         .values('month', 'year', 'total')
                         ]
            c = defaultdict(int)

            obj = []
            year = request.data.get('year')
            for data in job_count:
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
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code':  status_code,
                'message': 'New Customer count data by Month fetched successfully',
                'data': obj,
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo: {response}\n\n ")
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
