from django.contrib import admin
from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('register/', VendorSaleCardRegisterAPIView.as_view()),
    path('details/', VendorSaleCardListAPIView.as_view()),
    path('<int:pk>/', VendorSaleCardDetailAPIView.as_view()),
    path('vendor/<int:pk>/', VendorSaleCardDetailByVendorIDAPIView.as_view()),
    path('delete/<int:pk>/', VendorSaleCardDeleteAPIView.as_view()),
    path('update/<int:pk>/', VendorSaleCardUpdateAPIView.as_view()),
    path('payment/<int:pk>/', VendorSaleCardPaymentAPIView.as_view()),
    path('delivered/<int:pk>/', VendorSaleCardDelivered.as_view()),
    
    path('salecardbydate/<int:pk>', SaleCardbyDateAPIView.as_view()),
    path('salecardbydaterange/<int:pk>/',VendorSaleCardCountbyDateRangeAPIView.as_view()),
    path('salecardcus/<int:pk>/',VenorSaleCustomerCountbyDateRangeAPIView.as_view()),
    path('salecardbymonth/<int:pk>/', SaleCardbyMonthAPIView.as_view()),
    path('salecardcusbymonth/<int:pk>/', SaleCardCustomerbyMonthAPIView.as_view()),

    path('part/register/', VendorSaleCardPartRegisterAPIView.as_view()),
    path('part/details/', VendorSaleCardPartListAPIView.as_view()),
    path('part/<int:pk>/', VendorSaleCardPartDetailAPIView.as_view()),
    path('part/delete/<int:pk>/', VendorSaleCardPartDeleteAPIView.as_view()),
    path('part/update/<int:pk>/', VendorSaleCardPartUpdateAPIView.as_view()),
    path('part/salecard/<int:pk>/', VendorsalePartsByCardID.as_view()),
]
