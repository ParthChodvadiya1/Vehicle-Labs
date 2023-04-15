from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('details/', CustomerList.as_view()),
    path('<int:pk>/', CustomerDetails.as_view()),
    path('delete/<int:pk>/', CustomerDeleteAPIView.as_view()),
    path('update/<int:pk>/', CustomerUpdateAPIView.as_view()),
]
