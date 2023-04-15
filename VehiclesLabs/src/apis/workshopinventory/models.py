from django.db import models

from src.apis.parts.models import PartDetails
from src.apis.services.models import ServiceDetails
from src.apis.workshop.models import WorkshopDetail
from src.apis.vendorinventory.models import VendorInventory
from src.apis.vendors.models import VendorDetail

class WorkshopInventory(models.Model):

    workshopInventoryID = models.AutoField(primary_key=True, unique=True)
    workshopID          = models.ForeignKey(WorkshopDetail, on_delete=models.CASCADE, blank=True, null=True)
    vendorInventoryID   = models.ForeignKey(VendorInventory, on_delete=models.CASCADE, blank=True, null=True)
    partID              = models.ForeignKey(PartDetails, on_delete=models.CASCADE, blank=True, null=True)
    workshopPartQty     = models.IntegerField(null=True, blank=True)
    minimum_qty             = models.IntegerField(null=True, blank=True, default=5)
    workshopPartPrice   = models.FloatField(max_length= 10, null=True)
    total              = models.FloatField(default=0.00, null=True, blank=True)
    vendorID            = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, blank=True, null=True)
    paid           =  models.FloatField(default=0.00, null=True, blank=True)
    due           =  models.FloatField(default=0.00, null=True, blank=True)
    orderCompleted       = models.BooleanField(default = False,null=True)
    delivered =  models.BooleanField(default = False,null=True,blank=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]