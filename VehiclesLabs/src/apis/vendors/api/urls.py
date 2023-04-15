from django.urls import path
from .views import *


urlpatterns = [
    path('register/', VendorRegisterAPIView.as_view()),
    path('details/', VendorListAPIView.as_view()),
    path('<int:pk>/', VendorDetailAPIView.as_view()),
    path('delete/<int:pk>/', VendorDeleteAPIView.as_view()),
    path('update/<int:pk>/', VendorUpdateAPIView.as_view()),
    path('lastfive/<int:pk>/', VendorSalesLastFiveDataAPIView.as_view()),
    path('dateamount/<int:pk>/', VendorSalesAmountbyDateAPIView.as_view()),
    path('countbydate/<int:pk>', VendorSalesCountbyDateAPIView.as_view()),
    path('manager/register/', VendorManagerRegisterAPIView.as_view()),
    path('manager/details/', VendorManagerListAPIView.as_view()),
    path('manager/<int:pk>/', WorkshopManagerListByManageIDAPIView.as_view()),
    path('manager/delete/<int:pk>/', WorkshopManagerDeleteAPIView.as_view()),
]
