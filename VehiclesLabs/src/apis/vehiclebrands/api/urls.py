from django.urls import path
from .views import *


urlpatterns = [
    path('register/', VehicleBrandRegisterAPIView.as_view()),
    path('details/', VehicleBrandListAPIView.as_view()),
    path('<int:pk>/', VehicleBrandDetailAPIView.as_view()),
    path('update/<int:pk>/',VehicleBrandUpdateAPIView.as_view()),
    path('delete/<int:pk>/',VehicleBrandDeleteAPIView.as_view()),
    path('sheetupload/', AdminBrandSheetUploadAPIView.as_view()),
]