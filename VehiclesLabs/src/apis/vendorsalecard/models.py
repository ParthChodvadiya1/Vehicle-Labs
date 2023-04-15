from django.db import models
from src.apis.workshop.models import WorkshopDetail
from src.apis.customer.models import CustomerDetail
from src.apis.vendors.models import VendorDetail
from src.apis.vendorinventory.models import VendorInventory
from src.apis.parts.models import PartDetails
from src.apis.accounts.models import UserDetail
# from .models import VendorPartSale
CHOICES = (
      ("Workshop", "Workshop"),
      ("Customer", "Customer")
      )



class VendorPartSale(models.Model):

    vendorPartSaleID     = models.AutoField(primary_key=True, unique=True)
    # vendorsalecardID     = models.ForeignKey(VendorSaleCard, on_delete=models.CASCADE, null=True, blank=True)
    vendorInventoryID    = models.ForeignKey(VendorInventory, on_delete=models.CASCADE, null=True, blank=True)
    partID               = models.ForeignKey(PartDetails, on_delete=models.CASCADE, null=True, blank=True)
    partQty              = models.IntegerField(null = True, blank = True)
    partPrice            = models.FloatField(default=0.00, null=True, blank=True)

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

    def __str__(self):
        return  f'{self.vendorPartSaleID} - {self.vendorInventoryID} - {self.partID} - {self.partQty} - {self.partPrice}'

class VendorSaleCard(models.Model):
    vendorsalecardID =  models.AutoField(primary_key=True, unique=True)
    saleType         = models.CharField(max_length=128, choices=CHOICES, null=True, blank=True)
    workshopID       = models.ForeignKey(WorkshopDetail, on_delete=models.CASCADE, null=True, blank=True)
    cusID            = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE, null=True, blank=True)
    vendorID         = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, null=True, blank=True)
    userID           = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True)
    partSaleID       = models.ForeignKey(VendorPartSale, on_delete=models.CASCADE,blank=True,null=True)

    total           =  models.FloatField(default=0.00, null=True, blank=True)
    paid            =  models.FloatField(default=0.00, null=True, blank=True)
    due             =  models.FloatField(default=0.00, null=True, blank=True)
    discountAmount  =  models.FloatField(default=0.00, null=True, blank=True)
    newTotal        =  models.FloatField(default=0.00, null=True, blank=True)

    delivered       =  models.BooleanField(default=False, blank=True, null=True)
    deliveredAt     =  models.DateTimeField(blank=True, null=True)
    completed       =  models.BooleanField(default=False,null=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)


    class Meta:
        indexes = [
            models.Index(fields=['deliveredAt', '-createdAt'])
        ]

    def __str__(self):
        return  f'{self.vendorsalecardID} - {self.saleType} - {self.workshopID} - {self.cusID} - {self.vendorID} - {self.total} - {self.paid} - {self.due} - {self.discountAmount} - {self.newTotal} - {self.deliveredAt} - {self.createdAt}'

