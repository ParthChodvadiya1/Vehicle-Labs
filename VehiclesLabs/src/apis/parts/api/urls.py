from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterPartAPIView.as_view()),
    path('details/', PartListAPIView.as_view()),
    path('<int:pk>/', PartDetailsAPIView.as_view()),
    path('update/<int:pk>/', PartUpdateAPIView.as_view()),
    path('delete/<int:pk>/', PartDeleteAPIView.as_view()),    
    path('requestpart/register/', RequestedPartRegisterAPIView.as_view()),   
    path('requestpart/admin/register/', RequestedPartAdminRegisterAPIView.as_view()),   
    path('requestpart/details/', RequestedPartListAPIView.as_view()),   
    path('requestpart/details/vendorID/<int:pk>', RequestedPartByVendorIDAPIView.as_view()),   
    path('requestpart/<int:pk>/', RequestedPartDetailsAPIView.as_view()),   
    path('requestpart/update/<int:pk>/', RequestedPartUpdateAPIView.as_view()),   
    path('requestpart/delete/<int:pk>/', RequestedPartDeleteAPIView.as_view()),

    
    path('image/register/', PartImageRegiaterAPIView.as_view()),
    path('image/details/', PartImageListAPIView.as_view()),
    path('image/delete/<int:pk>/', PartImageDeleteAPIView.as_view()),    
    
    path('video/register/', PartVideoRegiaterAPIView.as_view()),
    path('video/details/', PartVideoListAPIView.as_view()),
    path('video/delete/<int:pk>/', PartVideoDeleteAPIView.as_view()),

    path('sheetupload/', AdminPartsSheetUploadAPIView.as_view()),
]