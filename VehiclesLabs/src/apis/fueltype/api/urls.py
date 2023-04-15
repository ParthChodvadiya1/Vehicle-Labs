from django.urls import path
from .views import *


urlpatterns = [
    path('register/', FuelTypeRegisterAPIView.as_view()),
    path('details/', FuelTypeListAPIView.as_view()),
    path('<int:pk>/', FuelTypeDetailAPIView.as_view()),
    path('update/<int:pk>/', FuelTypeUpdateAPIView.as_view()),
    path('delete/<int:pk>/', FuelTypeDeleteAPIView.as_view()),
]
