from django.db import models
from src.apis.parts.models import PartDetails
from src.apis.vendors.models import VendorDetail
from src.apis.customer.models import CustomerDetail
# from src.apis.workshopinventory.models import WorkshopInventory

class VendorInventory(models.Model):

    vendorInventoryID   = models.AutoField(primary_key= True, unique = True)
    partID              = models.ForeignKey(PartDetails, on_delete=models.CASCADE, blank=True, null=True)
    vendorPartQty       = models.IntegerField(null = True, blank = True)
    vendorPartPrice     = models.FloatField(max_length=12, null = True, blank = True)
    vendorID            = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, null = True , blank = True)
    excel_file          = models.FileField(blank= True, null = True)
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