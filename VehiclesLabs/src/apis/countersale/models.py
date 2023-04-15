from django.db import models
from src.apis.customer.models import CustomerDetail
from src.apis.accounts.models import UserDetail
from src.apis.workshop.models import WorkshopDetail
from src.apis.services.models import ServiceDetails
from src.apis.workshopinventory.models import WorkshopInventory
from src.apis.parts.models import PartDetails


class CounterSale(models.Model):

    countersaleID   = models.AutoField(primary_key = True, unique = True)
    cusID           = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE, blank=True, null=True)
    userID          = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True)
    workshopID    = models.ForeignKey(WorkshopDetail, on_delete=models.CASCADE, blank=True, null=True)
    vehiclenumber = models.CharField(max_length = 120, null = True , blank = True)
    servicename   = models.CharField(max_length = 120, null = True , blank = True)
    serviceprice  = models.FloatField(default=0.00, null=True, blank=True)
    paid           =  models.FloatField(default=0.00, null=True, blank=True)
    due           =  models.FloatField(default=0.00, null=True, blank=True)
    isCompleted       = models.BooleanField(default = False,null=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['vehiclenumber', 'servicename', 'isCompleted', '-createdAt'])
        ]

class MinorServices(models.Model):
    mserviceID      = models.AutoField(primary_key = True, unique= True)
    mserviceName    = models.CharField(max_length = 200 , null = True , blank = True)
    mservicePrice   = models.FloatField(default= 0 , blank=True, null= True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

