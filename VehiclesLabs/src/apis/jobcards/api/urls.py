from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('details/', JobCardList.as_view()),
    path('payment/<int:pk>/', JobCardPayment.as_view()),
    path('completed/<int:pk>/', JobCardCompleted.as_view()),
    path('<int:pk>/', JobCardDetails.as_view()),
    path('userID/<int:pk>/', JobCardDetailbyUserIDAPIView.as_view()),
    path('update/<int:pk>/', JobCardUpdateAPIView.as_view()),
    path('delete/<int:pk>/', JobCardDeleteAPIView.as_view()),
    path('lastfive/<int:pk>/', JobCardLastFiveDataAPIView.as_view()),
    path('dateamount/<int:pk>/', JobCardLastAmountbyDateAPIView.as_view()),
    path('countbydate/<int:pk>', JobCardCountbyDateAPIView.as_view()),
    path('jobcardbydate/<int:pk>', JobCardbyDateAPIView.as_view()),
    path('jobcardbydetails/<int:pk>', JobCardbyDateDetailsAPIView.as_view()),
    path('jobcardbydaterange/<int:pk>/',
         JobCardCountbyDateRangeAPIView.as_view()),
    path('customerbydaterange/<int:pk>/',
         CustomerCountbyDateRangeAPIView.as_view()),
    path('newcustomerbydaterange/<int:pk>/',
         NewCustomerCountbyDateRangeAPIView.as_view()),
    path('jobcardbymonth/<int:pk>/', JobCardbyMonthAPIView.as_view()),
    path('customerbymonth/<int:pk>/', CustomerbyMonthAPIView.as_view()),
    path('newcustomerbymonth/<int:pk>/', NewCustomerbyMonthAPIView.as_view()),
    path('workshopcustomer/<int:pk>/', WorkshopCustomerbyUserIDAPIView.as_view()),
    path('jobcardpdf/<int:pk>/', GeneratePdf.as_view()),

    path('jobcardservice/register/', JobCardServicesAPIView.as_view()),
    path('jobcardservice/details/', JobCardServicesDetail.as_view()),
    path('jobcardservice/<int:pk>/', JobCardServiceDetailAPIView.as_view()),
    path('jobcardservice/update/<int:pk>/',
         JobCardServicesUpdateAPIView.as_view()),
    path('jobcardservice/delete/<int:pk>/',
         JobCardServicesDeleteAPIView.as_view()),

    path('jobcardpart/register/', JobCardPartsAPIView.as_view()),
    path('jobcardpart/details/', JobCardPartsDetail.as_view()),
    path('jobcardpart/<int:pk>/', JobCardPartsDetailAPIView.as_view()),
    path('jobcardpart/update/<int:pk>/', JobCardPartsUpdateAPIView.as_view()),
    path('jobcardpart/delete/<int:pk>/', JobCardPartsDeleteAPIView.as_view()),
]
