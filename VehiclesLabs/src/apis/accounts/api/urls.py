from django.urls import path, re_path
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token, verify_jwt_token
from .views import *


urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('details/', UserList.as_view()),
    path('userID/<int:pk>/', UserDetailsByUserIDAPIView.as_view()),
    path('deactivate/<int:pk>/', DeactivateByUserIDAPIView.as_view()),
    path('activate/<int:pk>/', ActivateByUserIDAPIView.as_view()),
    path('usercount/<int:pk>/', UserCountByUserIDAPIView.as_view()),
    path('<int:pk>/', UserDetails.as_view()),
    re_path('change-password/(?P<userphone>\d+)/', ChangePasswordView.as_view()),
    re_path('change-password-validate-otp/', ForgotPasswordSendOTP.as_view()),
    re_path('change-password-varify-otp/', ForgotPasswordVerifyOTP.as_view()),
    re_path('jwt/', obtain_jwt_token),
    re_path('jwt/refresh/', refresh_jwt_token),
    re_path('api-token-verify/', verify_jwt_token),
    path('update/<int:pk>/', AccountUpdateAPIView.as_view()),
    path('delete/<int:pk>/', AccountDeleteAPIView.as_view()),
    path('update_sub/<int:pk>/', AddSubsciptionAPIView.as_view()),
    path('usercountbydaterange/<int:pk>/', UserCountbyDateRangeAPIView.as_view()),
    path('alldetailsbydaterange/<int:pk>/', AllDetailsCountbyDateRangeAPIView.as_view()),
    path('subscription/register/', SubscriptionPurchase.as_view()),
    path('subscription/details/', SubscriptionPurchaseList.as_view()),
    path('subscription/<int:pk>/', SubscriptionPurchaseByID.as_view()),
    path('subscriptioncap/<int:pk>/', SubscriptionCaptured.as_view()),

    path('subscriptiontype/register/', SubscriptionTypeRegister.as_view()),
    path('subscriptiontype/details/', SubscriptionTypeList.as_view()),
    path('subscriptiontype/<int:pk>/', SubscriptionTypeDetailAPIView.as_view()),
    path('subscriptiontype/update/<int:pk>/', SubscriptionTypeUpdateAPIView.as_view()),
    path('subscriptiontype/delete/<int:pk>/', SubscriptionTypeDeleteAPIView.as_view()),
    
    path('userbymonth/<int:pk>/', UserbyMonthAPIView.as_view()),
]
