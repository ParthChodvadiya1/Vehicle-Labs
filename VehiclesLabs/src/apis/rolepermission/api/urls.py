from django.urls import path 
from .views import *

urlpatterns = [
    path('register/', PermissionRegisterAPIView.as_view()),
    path('details/', PermissionListAPIView.as_view()),
    path('<int:pk>/', PermissionDetailsByUserWorkshopAPIView.as_view()),
    path('update/<int:pk>/', PermissionUpdateAPIView.as_view()),
    path('delete/<int:pk>/', PermissionDeleteAPIView.as_view()),    
    path('permID/<int:pk>/', PermissionDetailsBypermIDAPIView.as_view()),    
    path('userID/<int:pk>/', PermissionDetailsByUserIDAPIView.as_view()),    
    path('marketeer/register/', MarketeerRegisterAPIView.as_view()),
    path('marketeer/details/', MarketeerListAPIView.as_view()),
    path('marketeer/<int:pk>/', MarketeerDetailsBymarketerIDAPIView.as_view()),
    path('marketeer/update/<int:pk>/', MarketeerUpdateAPIView.as_view()),
    path('marketeer/delete/<int:pk>/', MarketeerDeleteAPIView.as_view()),    
    path('marketeer/mID/<int:pk>/', MarketeerDetailsBymIDAPIView.as_view()),    
    path('marketeer/userID/<int:pk>/', MarketeerDetailsByUserIDAPIView.as_view()),    
]
