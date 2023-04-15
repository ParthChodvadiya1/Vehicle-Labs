from django.contrib import admin
from django.urls import path
# from django.conf.urls import
from .views import *

urlpatterns = [
    path('register/', CounterSaleRegisterAPIView.as_view()),
    path('details/', CounterSaleList.as_view()),
    path('payment/<int:pk>/', CounterSalePayment.as_view()),
    path('completed/<int:pk>/', CounterSaleCompleted.as_view()),
    path('<int:pk>/', CounterSaleDetail.as_view()), 
    path('userID/<int:pk>/', CounterSaleDetailbyUserIDAPIView.as_view()),
    path('update/<int:pk>/', CounterSaleUpdateAPIView.as_view()), 
    path('delete/<int:pk>/', CounterSaleDeleteAPIView.as_view()),  
    path('countersalebydaterange/<int:pk>/', CounterSaleCountbyDateRangeAPIView.as_view()),  
    path('countersalebymonth/<int:pk>/', CounterSalebyMonthAPIView.as_view()),  

    path('ms/register/', MinorServiceRegisterAPIView.as_view()),
    path('ms/details/', MinorServiceListAPIView.as_view()),
    path('ms/<int:pk>/', MinorServiceDetailAPIView.as_view()),
    path('ms/update/<int:pk>/', MinorServiceUpdateAPIView.as_view()),
    path('ms/delete/<int:pk>/', MinorServiceDeleteAPIView.as_view()),
]