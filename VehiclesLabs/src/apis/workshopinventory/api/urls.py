from django.urls import path
from .views import *

urlpatterns = [

    path('register/', WorkshopInventoryRegisterAPIView.as_view()),
    path('workshop_register/', WorkshopRegisterAPIView.as_view()),
    path('details/', WorkshopInventoryListAPIView.as_view()),
    path('<int:pk>/', WorkshopInventoryDetailAPIView.as_view()),
    path('vendor/<int:pk>/', WorkshopInventoryVendorDetailAPIView.as_view()),
    path('delete/<int:pk>/', WorkshopInventoryDeleteAPIView.as_view()),
    path('update/<int:pk>/', WorkshopInventoryUpdateAPIView.as_view()),
    path('workshoppartqty/<int:pk>/', WorkshopInventoryPartQtyAPIView.as_view()),
    path('payment/<int:pk>/', WorkshopInventoryPayment.as_view()),
    path('completed/<int:pk>/', InventoryOrderedCompleted.as_view()),
    path('workshopdelivered/<int:pk>/', InventoryOrderedDelivered.as_view()),
]