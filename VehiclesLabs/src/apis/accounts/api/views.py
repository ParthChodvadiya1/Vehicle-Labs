from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import ast
import datetime
import http.client
import logging
import operator
from functools import reduce
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from src.apis.accounts.models import PhoneOTP, SubscriptionRecord, UserDetail
from src.apis.countersale.models import CounterSale
from src.apis.customer.api.serializers import CustomerSerializer
from src.apis.customer.models import CustomerDetail
from src.apis.jobcards.models import JobCardDetail
from src.apis.rolepermission.api.serializers import (
    JobCardPermissionSerializer, MarketeerListSerializer)
from src.apis.rolepermission.api.views import JobCardPermissionSerializer
from src.apis.rolepermission.models import Marketeer, Permissions
from src.utils import http_status
from src.utils.pagination import StandardResultsSetPagination
from src.utils.main import JWT_AUTH
from src.utils.validators import (get_token, getDate, send_otp,
                                  subscriptionCaptured)

from .serializers import *

logger = logging.getLogger('watchtower-logger')

expire_delta = JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

conn = http.client.HTTPConnection("2factor.in")

UserDetail = get_user_model()


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Requesting Login \n\n ")
        data = request.data
        userphone = data.get('userphone')
        password = data.get('password')
        user = authenticate(userphone=userphone, password=password)
        qs = UserDetail.objects.filter(
            Q(userphone__iexact=userphone)
        )
        try:
            if qs.count() == 1:
                user_obj = qs.first()
                if user_obj.check_password(password):
                    user = user_obj
                    token = get_token(user)
                    user.token = token
                    user.save()
                    isActivated = user.isActivated
                    if user.expiredAt > timezone.now():
                        if isActivated == True:
                            status_code = http_status.OK
                            update_last_login(None, user)
                            userID = user.userID
                            usertype = user.utype
                            if usertype == "Admin":
                                status_code = http_status.OK
                                response = {
                                    'success': True,
                                    'status_code': status_code,
                                    'message': 'User Logged In successfully.',
                                    'data': {
                                        'user': UserDetailSerializer(user, context=self.get_serializer_context()).data,
                                        'token': token,
                                        'expires': timezone.now() + expire_delta - timedelta(seconds=200)
                                    }
                                }
                                logger.info(
                                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            elif (usertype == "Workshop Owner") or (usertype == "Vendor") or (usertype == "Workshop Manager") or (usertype == "Vendor Manager"):
                                status_code = http_status.OK
                                response = {
                                    'success': True,
                                    'status_code': status_code,
                                    'message': 'User Logged In successfully.',
                                    'data': {
                                        'user': UserDetailSerializer(user, context=self.get_serializer_context()).data,
                                        'token': token,
                                        'expires': timezone.now() + expire_delta - timedelta(seconds=200)
                                    }
                                }
                                logger.info(
                                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            elif usertype == "Customer":
                                model = CustomerDetail.objects.get(
                                    userID=userID)
                                serializer_cus = CustomerSerializer(model)
                                status_code = http_status.OK
                                response = {
                                    'success': True,
                                    'status_code': status_code,
                                    'message': 'User Logged In successfully.',
                                    'data': {
                                        'user': UserDetailSerializer(user, context=self.get_serializer_context()).data,
                                        'customer': serializer_cus.data,
                                        'token': token,
                                        'expires': timezone.now() + expire_delta - timedelta(seconds=200)
                                    }
                                }
                                logger.info(
                                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            elif usertype == "Workshop User":
                                model = Permissions.objects.get(
                                    user_workshop=userID)
                                serializer_perm = JobCardPermissionSerializer(
                                    model)
                                status_code = http_status.OK
                                response = {
                                    'success': True,
                                    'status_code': status_code,
                                    'message': 'User Logged In successfully',
                                    'data': {
                                        'user': UserDetailSerializer(user, context=self.get_serializer_context()).data,
                                        'permissions': serializer_perm.data,
                                        'token': token,
                                        'expires': timezone.now() + expire_delta - timedelta(seconds=200)
                                    }
                                }
                                logger.info(
                                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            elif usertype == "Marketeer":
                                model = Marketeer.objects.get(
                                    marketerID=userID)
                                serializer_marketeer = MarketeerListSerializer(
                                    model)
                                status_code = http_status.OK
                                response = {
                                    'success': True,
                                    'status_code': status_code,
                                    'message': 'User Logged In successfully',
                                    'data': {
                                        'user': UserDetailSerializer(user, context=self.get_serializer_context()).data,
                                        'marketeer': serializer_marketeer.data,
                                        'token': token,
                                        'expires': timezone.now() + expire_delta - timedelta(seconds=200)
                                    }
                                }
                                logger.info(
                                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            else:
                                status_code = http_status.OK
                                response = {
                                    'success': False,
                                    'status_code': http_status.BAD_REQUEST,
                                    'message': 'You cannot login. your acccount is deactivated. Please, contact SuperAdmin.',
                                }
                                logger.info(
                                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                        else:
                            status_code = http_status.OK
                            response = {
                                'success': False,
                                'status_code': http_status.BAD_REQUEST,
                                'message': 'You cannot login. your acccount is deactivated. Please, contact SuperAdmin.',
                            }
                            logger.info(
                                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    else:
                        userID = user.userID
                        user_obj = UserDetail.objects.get(userID=userID)
                        user_obj.isActivated = False
                        user_obj.save()
                        status_code = http_status.OK
                        response = {
                            'success': False,
                            'status_code': http_status.BAD_REQUEST,
                            'message': 'you cannot login, active subscription',
                        }
                        logger.info(
                            f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                else:
                    status_code = http_status.OK
                    response = {
                        'success': False,
                        'status_code': http_status.BAD_REQUEST,
                        'message': 'Phone Number and Password does not match.',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'User Does not exist.',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.UNAUTHORIZED,
                'message': "Something is Wrong.",
                'error': str(e)
                # 'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n registering : data = {request.data}\n ")
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = get_token(user)
            utype = request.data.get('utype')
            user.utype = utype
            user.token = token
            user.save()

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'You are registered successfully.',
                'data': {
                    'user': UserDetailSerializer(user, context=self.get_serializer_context()).data,
                    'token': token,
                    'expires': timezone.now() + expire_delta
                }
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

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ValidatePhoneSendOTP(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Requesting Send OTP \n\n ")
        phoneno = request.data.get('userphone')
        try:
            if phoneno:
                phone = str(phoneno)
                user = UserDetail.objects.filter(userphone__iexact=phone)
                if user.exists():
                    status_code = http_status.ALREADY_REPORTED
                    response = {
                        'success': False,
                        'status_code': status_code,
                        'message': 'Phone number is already exists.'
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    return Response(response, status=status_code)
                else:
                    key = send_otp(phone)
                    if key:
                        old = PhoneOTP.objects.filter(phone__iexact=phone)
                        if old.exists():
                            old = old.first()
                            count = old.count
                            # if count > 10:
                            #     status_code = http_status.OK
                            #     response = {
                            #         'success': False,
                            #         'status_code': http_status.UNAUTHORIZED,
                            #         'message': 'sending otp limit exceeded.'
                            #     }
                            #     logger.info(
                            #         f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            #     # return Response(response, status=status_code)
                            old.count = count + 1
                            old.otp = key
                            old.save()
                            status_code = http_status.OK
                            response = {
                                'success': True,
                                'status_code': status_code,
                                'message': 'OTP sent successfully.'
                            }
                            logger.info(
                                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                        else:
                            old = PhoneOTP.objects.create(
                                phone=phone,
                                otp=key,
                            )
                        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=10c0f6a1-fd6e-11ea-9fa5-0200cd936042&to=" +
                        #              phone+"&otpvalue="+str(key)+"&templatename=VLB")
                        # res = conn.getresponse()

                        # data = res.read()
                        # data = data.decode("utf-8")
                        # data = ast.literal_eval(data)
                        # if data["Status"] == 'Success':
                        #     old.otp_session_id = data["Details"]
                        #     old.save()
                            status_code = http_status.OK
                            response = {
                                'success': True,
                                'status_code': status_code,
                                'message': 'OTP sent successfully.'
                            }
                            logger.info(
                                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            # return Response(response, status_code)
                        # else:
                        #     status_code = http_status.BAD_REQUEST
                        #     response = {
                        #         'success': False,
                        #         'status_code': status_code,
                        #         'message': 'OTP sending Failed.',
                        #     }
                            # logger.info(
                            #     f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            # return Response(response, status=status_code)
                    else:
                        status_code = http_status.OK
                        response = {
                            'success': False,
                            'status_code': http_status.BAD_REQUEST,
                            'message': 'Sending otp error.'
                        }
                        logger.info(
                            f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                        # return Response(response, status=status_code)

            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.NOT_FOUND,
                    'message': 'Phone number is not given.'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                # return Response(response, status=status_code)
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


class ValidateOTP(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp',  False)
        try:
            if phone and otp_sent:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    otp = old.otp
                    if str(otp_sent) == str(otp):
                        old.validated = True
                        old.save()
                        status_code = http_status.OK
                        response = {
                            'success': True,
                            'status_code': http_status.ACCEPTED,
                            'message': 'OTP matched, please proceed for register',
                        }
                        logger.info(
                            f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                        return Response(response, status=status_code)
                    else:
                        status_code = http_status.OK
                        response = {
                            'success': False,
                            'status_code': http_status.UNAUTHORIZED,
                            'message': 'OTP incorect',
                        }
                        logger.info(
                            f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                        return Response(response, status=status_code)
                else:
                    status_code = http_status.BAD_REQUEST
                    response = {
                        'success': False,
                        'status_code': status_code,
                        'message': 'First proceed via sending OTP request',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    return Response(response, status=status_code)
            else:
                status_code = http_status.BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'message': 'Please provide both phone and otp for validation',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                return Response(response, status_code)
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


class UserList(generics.ListAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "userID",
        "email",
        "userphone",
        "username",
        "utype",
    ]

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = UserDetail.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('media')
            userRole = request.GET.get('userRole')
            if userRole:
                if userRole == 'wo':
                    model = model.filter(utype='Workshop User')
                elif userRole == 'wm':
                    model = model.filter(utype='Workshop Manager')
                elif userRole == 'v':
                    model = model.filter(utype='Vendor')
                elif userRole == 'vm':
                    model = model.filter(utype='Vendor Manager')
            else:
                model = model
            if request.GET.get('search'):
                search = request.GET.get('search')
                model = model.filter(Q(username__icontains=search) | Q(
                    email__icontains=search) | Q(userphone__icontains=search))

            serializer = UserDetailSerializer(model, many=True)

            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data

            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'User Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")

        return Response(response, status=status_code)


class UserDetails(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            logger.info(
                f"Enter log: Requesting {request.build_absolute_uri()} \n additionalInfo: Entered data: userID = {pk} ")
            model = UserDetail.objects.get(userID=pk, isDeleted=False)
            serializer = UserDetailSerializer(model)
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'user fetched successfully',
                'data': serializer.data
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
        return Response(response)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = UserDetail.objects.all()
    serializer_class = UserChangePasswordSerializer

    def put(self, request, userphone, format=None):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n changing the password\n\n ")
        user = UserDetail.objects.get(userphone=userphone)
        serializer = self.serializer_class(user, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                user.set_password(serializer.data.get('password'))
                user.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code': status_code,
                    'message': 'Password update successfully.'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                # return Response(response, status=status_code)
            else:
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Something is wrong.'
                }
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


class ForgotPasswordSendOTP(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n forgot password send OTP\n\n")
        phoneno = request.data.get('userphone')
        if phoneno:
            phone = str(phoneno)
            user = UserDetail.objects.filter(userphone__iexact=phone)
            if user.exists():
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 50:
                            status_code = http_status.UNAUTHORIZED
                            response = {
                                'success': False,
                                'status_code': status_code,
                                'message': 'sending otp limit exceeded.'
                            }
                            logger.info(
                                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                            return Response(response, status=status_code)
                        old.count = count + 1
                        old.otp = key
                        old.save()
                        status_code = http_status.OK
                        response = {
                            'success': True,
                            'status_code': status_code,
                            'message': 'OTP sent successfully.'
                        }
                        logger.info(
                            f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")

                    else:
                        old = PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        status_code = http_status.OK
                        response = {
                            'success': True,
                            'status_code': status_code,
                            'message': 'OTP sent successfully.'
                        }
                        logger.info(
                            f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")

                    # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=10c0f6a1-fd6e-11ea-9fa5-0200cd936042&to=" +
                    #              phone+"&otpvalue="+str(key)+"&templatename=VLB")
                    # res = conn.getresponse()
                    # data = res.read()
                    # data = data.decode("utf-8")
                    # data = ast.literal_eval(data)
                    # if data["Status"] == 'Success':
                    #     old.otp_session_id = data["Details"]
                    #     old.save()
                        # status_code = http_status.OK
                        # response = {
                        #     'success': True,
                        #     'status_code': status_code,
                        #     'message': 'OTP sent successfully.'
                        # }
                        # logger.info(
                        #     f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                        # return Response(response, status_code)
                    # else:
                    #     status_code = http_status.BAD_REQUEST
                    #     response = {
                    #         'success': False,
                    #         'status_code': status_code,
                    #         'message': 'OTP sending Failed.',
                    #     }
                    #     logger.info(
                    #         f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    #     return Response(response, status=status_code)
                else:
                    status_code = http_status.OK
                    response = {
                        'success': False,
                        'status_code': http_status.BAD_REQUEST,
                        'message': 'Sending otp error.'
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    # return Response(response, status=status_code)
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'Phone number does not exists.Please go for registration process.'
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                # return Response(response, status=status_code)
        else:
            status_code = http_status.OK
            response = {
                'success': False,
                'status_code': http_status.NOT_FOUND,
                'message': 'Phone number is not given.'
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            return Response(response, status=status_code)


class ForgotPasswordVerifyOTP(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Verifying OTP\n\n")
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp',  False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    status_code = http_status.ACCEPTED
                    response = {
                        'success': True,
                        'status_code': status_code,
                        'message': 'OTP matched, please proceed for login.',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    return Response(response, status=status_code)
                else:
                    status_code = http_status.UNAUTHORIZED
                    response = {
                        'success': False,
                        'status_code': status_code,
                        'message': 'OTP incorect',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                    return Response(response, status=status_code)
            else:
                status_code = http_status.BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'message': 'First proceed via sending OTP request',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                return Response(response, status=status_code)
        else:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': 'Please provide both phone and otp for validation',
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            return Response(response, status_code)


class AccountUpdateAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserUpdateSertializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Updating Account data for userID ={pk}\n\n")
        try:
            model = UserDetail.objects.get(userID=pk)
            user = model
            if model.isDeleted == False:
                model = UserDetail.objects.get(userID=pk)
                serializer = UserUpdateSertializer(model, data=request.data)
                if serializer.is_valid() == True:
                    token = get_token(user)
                    user.token = token
                    user.save()
                    serializer.save()
                    serializer1 = UserDetailSerializer(model)
                    status_code = http_status.OK
                    response = {
                        'success': True,
                        'status_code':  status_code,
                        'message': 'User Data Updated Successfully',
                        'data': serializer1.data,
                        'token': token
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                else:
                    status_code = http_status.BAD_REQUEST
                    response = {
                        'success': False,
                        'status_code': status_code,
                        'message': 'your entered data is already exist',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'message': 'User details does not exists',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status_code)


class AccountDeleteAPIView(generics.DestroyAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserUpdateSertializer

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for usermanageID = {pk}\n\n ")
        try:
            model = UserDetail.objects.get(userID=pk)
            if not model:
                status_code = http_status.NOT_FOUND
                response = {
                    'success': False,
                    "message": "User Not Found",
                    "status_code": status_code,
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                model.isDeleted = True
                model.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    "message": "User Data Deleted Successfully.",
                    "status_code": status_code,
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")

        except Exception as e:
            status_code = http_status.NOT_FOUND
            response = {
                'success': False,
                "status_code": status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status_code)


class AddSubsciptionAPIView(generics.UpdateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserUpdateSertializer

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n purchasing subscription for userID = {pk}\n\n ")
        try:
            model = UserDetail.objects.get(userID=pk)
            subusers = Permissions.objects.filter(userID=pk, isDeleted=False)
            tempserializer = SubUserSubscriptionUpdateSertializer(
                subusers, many=True)

            if model.isDeleted == False:
                model = UserDetail.objects.get(userID=pk)
                serializer = UserSubscriptionUpdateSertializer(
                    model, data=request.data)

                if serializer.is_valid() == True:
                    serializer.validated_data['expiredAt'] -= datetime.timedelta(
                        seconds=19800)
                    serializer.save()
                    for permID in subusers:
                        subuserID = Permissions.objects.get(
                            permID=permID.permID)
                        userid = permID.user_workshop.userID
                        userdetail = UserDetail.objects.get(userID=userid)
                        userdetail.expiredAt = request.data.get('expiredAt')
                        userdetail.save()

                    status_code = http_status.OK
                    response = {
                        'success': True,
                        'status_code':  status_code,
                        'message': 'User Subsciption Updated Successfully',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
                else:
                    status_code = http_status.OK
                    response = {
                        'success': False,
                        'status_code': http_status.BAD_REQUEST,
                        'message': 'Something is wrong.',
                    }
                    logger.info(
                        f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'User details does not exists',
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


class UserCountbyDateRangeAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n User count by date range for userID = {pk}\n\n ")
        try:
            start_date = request.data.get('start_date')
            startDate = datetime.strptime(
                start_date, '%Y-%m-%d').date()

            end_date = request.data.get('end_date')
            endDate = datetime.strptime(
                end_date, '%Y-%m-%d').date() + timedelta(days=1)

            models = Permissions.objects.filter(userID=pk, isDeleted=False).filter(createdAt__lte=endDate, createdAt__gt=startDate).\
                annotate(date=TruncDate('createdAt')).values(
                    'date').annotate(count=Count('userID'))

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
                'message': 'Jobcard  count data by Date fetched successfully',
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


class UserbyMonthAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = UserDetailSerializer
    queryset = UserDetail.objects.all()

    def post(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n User count by month for userID = {pk}\n\n ")
        try:
            model = Permissions.objects.filter(userID=pk, isDeleted=False)
            my = [v for v in
                  model.annotate(month=ExtractMonth('createdAt'),
                                 year=ExtractYear('createdAt'),)
                  .order_by()
                  .values('month', 'year')
                  .annotate(total=Count('userID'))
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
                data['month'] = datetime.strptime(
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
                'message': 'Jobcard  Details does not exists',
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response)


class AllDetailsCountbyDateRangeAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Permissions.objects.all()

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n All details count by date range for userID = {pk}\n\n ")
        try:
            models = Permissions.objects.filter(userID=pk, isDeleted=False)

            job_count = JobCardDetail.objects.filter(
                userID=pk, isDeleted=False).annotate(count=Count('jobID')).count()

            users_count = Permissions.objects.filter(
                userID=pk, isDeleted=False).annotate(count=Count('userID')).count()

            counter_sale_count = CounterSale.objects.filter(
                userID=pk, isDeleted=False).annotate(count=Count('countersaleID')).count()

            customer_count = job_count + counter_sale_count

            data = {
                'Job Count': job_count,
                'Counter Sale Count': counter_sale_count,
                'Users Count': users_count,
                'Customer Count': customer_count
            }

            status_code = http_status.OK

            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Jobcard  count data by Date fetched successfully.',
                'data': data,
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


class UserDetailsByUserIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = UserDetail.objects.get(userID=pk)
            if model.isDeleted == False:
                model = UserDetail.objects.get(userID=pk)
                serializer = UserDetailSerializer(model)
                userID = serializer.data['userID']
                model1 = UserDetail.objects.get(userID=userID)
                serializer1 = UserDetailByUserIDSerializer(model1)
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'user fetched successfully',
                    'data':  {
                        'user': serializer.data,
                        'token': serializer1.data['token']
                    }
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'user Details does not exists',
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


class DeactivateByUserIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n Deactivating user userID = {pk}\n\n ")
        try:
            model = UserDetail.objects.get(userID=pk)
            if model.isDeleted == False:
                user_obj = UserDetail.objects.get(userID=pk)
                user_obj.isActivated = False
                user_obj.save()
                rolepermission_obj = Permissions.objects.filter(
                    userID=pk, isDeleted=False)
                serializers = JobCardPermissionSerializer(
                    rolepermission_obj, many=True)
                userIDs = [i['user_workshop']['userID']
                           for i in serializers.data]
                for userID in userIDs:
                    user_obj = UserDetail.objects.get(userID=userID)
                    user_obj.isActivated = False
                    user_obj.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Deactivated account successfully.',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'user Details does not exists',
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


class ActivateByUserIDAPIView(generics.RetrieveAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n Activating user userID = {pk}\n\n ")
        try:
            model = UserDetail.objects.get(userID=pk)
            if model:
                user_obj = UserDetail.objects.get(userID=pk)
                user_obj.isActivated = True
                user_obj.save()
                rolepermission_obj = Permissions.objects.filter(
                    userID=pk, isDeleted=False)
                serializers = JobCardPermissionSerializer(
                    rolepermission_obj, many=True)
                userIDs = [i['user_workshop']['userID']
                           for i in serializers.data]
                for userID in userIDs:
                    user_obj = UserDetail.objects.get(userID=userID)
                    user_obj.isActivated = True
                    user_obj.save()
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Activate account successfully.',
                    # 'data': serializers.data
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'user Details does not exists',
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


class UserCountByUserIDAPIView(generics.RetrieveAPIView):

    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n user count by userID = {pk}\n\n ")
        try:
            model = UserDetail.objects.get(userID=pk)
            if model.isDeleted == False:
                rolepermission_obj = Permissions.objects.filter(
                    userID=pk, isDeleted=False).count()

                count = {
                    'Count': rolepermission_obj
                }
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Total user of this workshop',
                    'data': count
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.OK
                response = {
                    'success': False,
                    'status_code': http_status.BAD_REQUEST,
                    'message': 'user Details does not exists',
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


class SubscriptionPurchase(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = SubscriptionRecord.objects.all()
    serializer_class = SubscriptionRecordSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            subscription_obj = self.create(request, *args, **kwargs)
            model = UserDetail.objects.get(userID=request.data.get("userID"))
            serializer = UserDetailSerializer(model)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Purchase successfully.",
                "data":  serializer.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionPurchaseList(generics.ListAPIView):
    queryset = SubscriptionRecord.objects.all()
    serializer_class = SubscriptionRecordDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = SubscriptionRecord.objects.filter(
                isDeleted=False).order_by('-createdAt')
            model = model.prefetch_related('userID', 'userID__media')
            serializer = SubscriptionRecordDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):
                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Subscription Data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionPurchaseByID(generics.ListAPIView):
    queryset = SubscriptionRecord.objects.all()
    serializer_class = SubscriptionRecordDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving details for userID = {pk}\n\n ")
        try:
            model = SubscriptionRecord.objects.filter(
                userID=pk, isDeleted=False)
            if model:
                model = SubscriptionRecord.objects.filter(
                    userID=pk, isDeleted=False)
                model = model.prefetch_related('userID', 'userID__media')
                serializer = SubscriptionRecordDetailSerializer(
                    model, many=True)
                if request.GET.get('limit') and request.GET.get('offset'):

                    page = self.paginate_queryset(serializer.data)
                else:
                    page = serializer.data
                status_code = http_status.OK
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Data fetched successfully',
                    'count': model.count(),
                    'data': page
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'message': 'Details does not exists',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionTypeRegister(generics.CreateAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Entered data:{request.data}\n\n")
        try:
            fueltype_obj = self.create(request, *args, **kwargs)
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': "Subscription type added registered.",
                'data': fueltype_obj.data
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionTypeList(generics.ListAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Retrieving all details ")
        try:
            model = SubscriptionType.objects.filter(isDeleted=False)
            # model = model.prefetch_related('userID', 'userID__media')
            serializer = SubscriptionTypeDetailSerializer(model, many=True)
            if request.GET.get('limit') and request.GET.get('offset'):

                page = self.paginate_queryset(serializer.data)
            else:
                page = serializer.data
            status_code = http_status.OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Subscription type data fetched successfully',
                'count': model.count(),
                'data': page
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': http_status.BAD_REQUEST,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionCaptured(generics.RetrieveAPIView):
    queryset = SubscriptionRecord.objects.all()
    serializer_class = SubscriptionCapturedSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n subscription captured for subscriptionID = {pk}\n\n ")
        try:
            model = SubscriptionRecord.objects.get(
                subscriptionID=pk, isDeleted=False)
            status_code = http_status.OK
            serializer = SubscriptionCapturedSerializer(model)
            resp = subscriptionCaptured(
                serializer.data["paymentID"], serializer.data["amount"])
            model.razor_res = resp
            model.save()
            response = {
                'success': True,
                'status_code':  http_status.OK,
                'message': 'Payment Captured successfully',
                'data': resp
            }
            logger.info(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionTypeDetailAPIView(generics.RetrieveAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk):
        try:
            model = SubscriptionType.objects.get(subTypeID=pk)
            if model.isDeleted == False:
                model = SubscriptionType.objects.get(subTypeID=pk)
                status_code = http_status.OK
                serializer = SubscriptionTypeDetailSerializer(model)
                response = {
                    'success': True,
                    'status_code':  http_status.OK,
                    'message': 'Data fetched successfully',
                    'data': serializer.data
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
            else:
                status_code = http_status.BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'message': 'Details does not exists',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)


class SubscriptionTypeDeleteAPIView(generics.DestroyAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def delete(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n Deletation for subTypeID = {pk}\n\n ")
        try:
            model = SubscriptionType.objects.get(subTypeID=pk, isDeleted=False)
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
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")
        except Exception as e:
            status_code = http_status.NOT_FOUND
            response = {
                'success': False,
                "status_code": status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status_code)


class SubscriptionTypeUpdateAPIView(generics.UpdateAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeDetailSerializer
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def put(self, request, pk):
        logger.info(
            f"Enter log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n updating the data for subTypeID = {pk}\n\n ")
        try:
            model = SubscriptionType.objects.get(subTypeID=pk, isDeleted=False)
            serializer = SubscriptionTypeDetailSerializer(
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
                status_code = http_status.BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'message': 'something is wrong',
                }
                logger.info(
                    f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n {response}\n\n")

        except Exception as e:
            status_code = http_status.BAD_REQUEST
            response = {
                'success': False,
                'status_code': status_code,
                'message': "Something is Wrong.",
                'error': str(e)
            }
            logger.error(
                f"Exit log: Requesting {request.build_absolute_uri()} \n\n additionalInfo:\n\n  {str(e)}")
        return Response(response, status=status_code)
