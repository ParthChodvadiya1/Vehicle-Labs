from django.urls import path
from .views import *


urlpatterns = [
    path('register/', VehiclesRegisterAPIView.as_view()),
    path('details/', VehiclesListAPIView.as_view()),
    path('<int:pk>/', VehiclesDetailAPIView.as_view()),
    path('delete/<int:pk>/', VehiclesDeleteAPIView.as_view()),
    path('update/<int:pk>/', VehiclesUpdateAPIView.as_view()),
]
