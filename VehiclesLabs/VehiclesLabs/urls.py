from django.contrib import admin
from django.urls import path, include

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('api/auth/', include("src.apis.accounts.api.urls")),
    path('api/customer/', include("src.apis.customer.api.urls")),
    path('api/workshop/', include("src.apis.workshop.api.urls")),
    path('api/vehicles/', include("src.apis.vehicles.api.urls")),
    path('api/fueltype/', include("src.apis.fueltype.api.urls")),
    path('api/vehiclesbrand/', include("src.apis.vehiclebrands.api.urls")),
    path('api/jobcard/',include("src.apis.jobcards.api.urls")),
    path('api/rolepermission/',include("src.apis.rolepermission.api.urls")),
    path('api/services/',include("src.apis.services.api.urls")),
    path('api/parts/',include("src.apis.parts.api.urls")),
    path('api/vendorinventory/',include("src.apis.vendorinventory.api.urls")),
    path('api/workshopinventory/',include("src.apis.workshopinventory.api.urls")),
    path('api/media/',include("src.apis.media.api.urls")),
    path('api/vendor/',include("src.apis.vendors.api.urls")),
    path('api/countersale/',include("src.apis.countersale.api.urls")),
    path('api/vendorcustomer/',include("src.apis.vendorcustomer.api.urls")),
    path('api/bookAppointment/',include("src.apis.customerBookAppointment.api.urls")),
    path('api/notifications/',include("src.apis.notifications.api.urls")),
    path('api/servicereminder/',include("src.apis.serviceReminder.api.urls")),
    path('api/vendorsalecard/',include("src.apis.vendorsalecard.api.urls")),
    path('api/admininquiry/',include("src.apis.admininquiry.api.urls")),
    path('api/accounting/',include("src.apis.accounting_software.api.urls")),
]

from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated

schema_view = get_schema_view(
    openapi.Info(
        title="Vehicles Labs APIs",
        default_version="v1",
        description="VLB API",
        contact=openapi.Contact(email=""),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    url(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
    url(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    url(
        r"^api/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=None),
        name="schema-redoc",
    ),

]
