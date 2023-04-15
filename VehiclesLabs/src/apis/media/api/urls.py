from django.urls import path
from .views import *

urlpatterns = [

    path('register/', MediaRegisterAPIView.as_view()),
    path('details/', MediaListAPIView.as_view()),
    path('<int:pk>/', MediaDetailAPIView.as_view()),
    path('delete/<int:pk>/', MediaDeleteAPIView.as_view()),
    path('update/<int:pk>/', MediaUpdateAPIView.as_view()),
]
