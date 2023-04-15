from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('details/', NotificationsListAPIView.as_view()),
    path('<int:pk>/', NotificationsDetailsAPIView.as_view()),
    path('userID/<int:pk>/', NotificationsDetailbyUserIDAPIView.as_view()),
    path('delete/<int:pk>/', NotificationsDeleteAPIView.as_view()),
    path('update/<int:pk>/', NotificationsUpdateAPIView.as_view()),
]
