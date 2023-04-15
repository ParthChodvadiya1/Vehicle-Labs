from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('register/', AdminInquiryRegisterAPIView.as_view()),
    path('details/', AdminInquiryDetailAPIView.as_view()),
    path('<int:pk>/', AdminInquiryDetailByIDAPIView.as_view()),
    path('delete/<int:pk>/', AdminInquiryDeleteAPIView.as_view()),
    path('update/<int:pk>/', AdminInquiryUpdateAPIView.as_view()),
]