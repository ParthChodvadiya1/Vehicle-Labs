from django.urls import path
from .views import *

urlpatterns = [
    path('register/', WorkshopRegisterAPIView.as_view()),
    path('details/', WorkshopListAPIView.as_view()),
    path('<int:pk>/', WorkshopDetailAPIView.as_view()),
    path('delete/<int:pk>/', WorkshopDeleteAPIView.as_view()),
    path('update/<int:pk>/', WorkshopUpdateAPIView.as_view()),
    path('manager/register/', WorkshopManagerRegisterAPIView.as_view()),
    path('manager/details/', WorkshopManagerListAPIView.as_view()),
    path('manager/<int:pk>/', WorkshopManagerListByManageIDAPIView.as_view()),
    path('manager/delete/<int:pk>/', WorkshopManagerDeleteAPIView.as_view()),
]

