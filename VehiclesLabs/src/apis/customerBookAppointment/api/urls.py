from django.contrib import admin
from django.urls import path, re_path
# from django.conf.urls import
from .views import BookAppointmentRegisterAPIView, BookAppointUpdatebyAppointIDAPIView ,BookAppointmentList, AppointDetailbyAppointIDAPIView,BookAppointDeletebyAppointIDAPIView, AppointDetailbyworkshopIDAPIView, AppointDetailbycusIDAPIView


urlpatterns = [
    path('register/', BookAppointmentRegisterAPIView.as_view()),
    path('details/', BookAppointmentList.as_view()),
    path('<int:pk>/', AppointDetailbyAppointIDAPIView.as_view()),
    path('workshop/<int:pk>/', AppointDetailbyworkshopIDAPIView.as_view()),
    path('customer/<int:pk>/', AppointDetailbycusIDAPIView.as_view()),
    path('update/<int:pk>/', BookAppointUpdatebyAppointIDAPIView.as_view()),
    path('delete/<int:pk>/', BookAppointDeletebyAppointIDAPIView.as_view()),
]
