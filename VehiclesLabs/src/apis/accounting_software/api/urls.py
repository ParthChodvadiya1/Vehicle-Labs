from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterEntery.as_view()),
    path('details/', EntryList.as_view()),
    path('<int:pk>/', EntryDetails.as_view()),
    path('update/<int:pk>/', EntryUpdate.as_view()),
    path('delete/<int:pk>/', EntryDelete.as_view()),
]