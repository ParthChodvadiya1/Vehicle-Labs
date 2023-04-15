from django.urls import path
from .views import *

urlpatterns = [

    path('register/', VendorInventoryRegisterAPIView.as_view()),
    path('details/', VendorInventoryListAPIView.as_view()),
    path('vendor/<int:pk>/', VendorInventoryDetailAPIView.as_view()),
    path('<int:pk>/', VendorInventoryDetailByVenIDAPIView.as_view()),
    path('delete/<int:pk>/', VendorInventoryDeleteAPIView.as_view()),
    path('update/<int:pk>/', VendorInventoryUpdateAPIView.as_view()),
    path('parts/upload/', PartsUploadAPIView.as_view()),
    path('partsqty/<int:pk>/', VendorInventoryPartQtyAPIView.as_view()),
    
]