from django.contrib import admin
from src.apis.jobcards.models import JobCardDetail

# Register your models here.

admin.site.register(JobCardDetail)


# from django.contrib import admin
# from django.urls import path, include
# from rest_framework import permissions
# from drf_yasg2.views import get_schema_view
# from drf_yasg2 import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="CGPIT API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# path('', schema_view.with_ui('swagger', cache_timeout=0),
#           name='schema-swagger-ui'),