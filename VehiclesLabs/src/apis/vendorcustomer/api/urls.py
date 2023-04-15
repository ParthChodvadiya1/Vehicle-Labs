from django.urls import path
from .views import *
urlpatterns = [

    path('register/', VendorCustomerRegisterAPIView.as_view()),
    path('details/', VendorCustomerListAPIView.as_view()),
    path('<int:pk>/', VendorCustomerDetailAPIView.as_view()),
    path('delete/<int:pk>/', VendorCustomerDeleteAPIView.as_view()),
    path('update/<int:pk>/', VendorCustomerUpdateAPIView.as_view()),
    path('customerdelivered/<int:pk>/', CustomerDelivered.as_view()),
]