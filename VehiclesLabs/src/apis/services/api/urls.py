from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterServicesAPIView.as_view()),
    path('details/', ServicesListAPIView.as_view()),
    path('<int:pk>/', ServicesDetailsAPIView.as_view()),
    path('update/<int:pk>/', ServicesUpdateAPIView.as_view()),
    path('delete/<int:pk>/', ServicesDeleteAPIView.as_view()),
    path('sheetupload/', AdminServiceSheetUploadAPIView.as_view()),
]
