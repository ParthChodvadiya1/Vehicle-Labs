from django.urls import path
from .views import *


urlpatterns = [
    path('register/', ServiceReminderRegisterAPIView.as_view()),
    path('details/', ServiceReminderList.as_view()),
    path('<int:pk>/', ServiceReminderbysdIDAPIView.as_view()),
    path('workshop/<int:pk>/', ServiceReminderbyworkshopIDAPIView.as_view()),
    path('customer/<int:pk>/', ServiceReminderbycusIDAPIView.as_view()),
    path('update/<int:pk>/', ServiceReminderUpdatebyAppointIDAPIView.as_view()),
    path('delete/<int:pk>/', ServiceReminderDeletebyAppointIDAPIView.as_view()),
]
