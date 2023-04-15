from django.db import models
from src.apis.customer.models import CustomerDetail
from src.apis.vendorinventory.models import VendorInventory
from src.apis.vendors.models import VendorDetail
# from src.apis.vendorcustomer.models import PartDetails
# Create your models here.
class VendorCustomer(models.Model):
    vendorCustomerID   = models.AutoField(primary_key=True, unique=True)
    cusID              = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE, blank=True, null=True)
    vendorInventoryID  = models.ForeignKey(VendorInventory, on_delete=models.CASCADE, blank=True, null=True)
    partID            = models.ForeignKey("parts.PartDetails", on_delete=models.CASCADE, blank=True, null=True)
    cusPartQty         = models.IntegerField(null = True, blank=True)
    cusPartPrice       = models.FloatField(max_length = 15,  null = True ,blank=True)
    vendorID           = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, blank=True, null=True)
    delivered =  models.BooleanField(default = False,null=True,blank=True)

    meta               = models.JSONField(encoder=None, null=True)
    createdAt          = models.DateTimeField(auto_now_add=True)
    updatedAt          = models.DateTimeField(auto_now=True)
    isDeleted          = models.BooleanField(default = False,null=True)
    createdBy          = models.CharField(max_length=120)
    updatedBy          = models.CharField(max_length=120)


    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]
