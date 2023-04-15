from django.db import models
from src.apis.customer.models import CustomerDetail
from src.apis.vehicles.models import VehiclesDetail
from src.apis.vehiclebrands.models import VehicleBrand
from src.apis.fueltype.models import fueltype
from src.apis.accounts.models import UserDetail
from src.apis.services.models import ServiceDetails
from src.apis.parts.models import PartDetails
from src.apis.vendorinventory.models import VendorInventory
from src.apis.workshopinventory.models import WorkshopInventory
from src.apis.workshop.models import WorkshopDetail
# Create your models here.

class BookAppointment(models.Model):
    appointID           = models.AutoField(primary_key=True, unique=True)    
    vehiclenumber   = models.CharField(max_length=18, null=False, blank=False)
    appointDate     = models.DateTimeField(null=False, blank=False)
    brandID         = models.ForeignKey(
                      VehicleBrand, on_delete=models.CASCADE, blank=False, null=False, default=150)
    cusID           = models.ForeignKey(
                      CustomerDetail, on_delete=models.CASCADE, blank=True, null=True)
    servicesID       = models.ManyToManyField(ServiceDetails, related_name='many_service')
    userID          = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True)
    workshopID      = models.ForeignKey(WorkshopDetail, on_delete=models.CASCADE,blank=True,null=True)
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['vehiclenumber', 'appointDate', '-createdAt'])
        ]

