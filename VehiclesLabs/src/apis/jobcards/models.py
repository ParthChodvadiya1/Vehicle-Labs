from django.contrib.postgres.fields import JSONField
from django.db import models
from src.apis.accounts.models import UserDetail
from src.apis.customer.models import CustomerDetail
from src.apis.fueltype.models import fueltype
from src.apis.services.models import ServiceDetails
from src.apis.vehiclebrands.models import VehicleBrand
from src.apis.vehicles.models import VehiclesDetail
from src.apis.workshop.models import WorkshopDetail
from src.apis.workshopinventory.models import WorkshopInventory


class JobCardDetail(models.Model):
    jobID           = models.AutoField(primary_key=True, unique=True)
    vehicleID       = models.ForeignKey(
                      VehiclesDetail, on_delete=models.CASCADE, blank=True, null=True)
    brandID         = models.ForeignKey(
                      VehicleBrand, on_delete=models.CASCADE, blank=False, null=False, default=150)
    cusID           = models.ForeignKey(
                      CustomerDetail, on_delete=models.CASCADE, blank=True, null=True)
    fueltypeID      = models.ForeignKey(
                      fueltype, on_delete=models.CASCADE, blank=False, null=False, default=5)
    userID          = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True)
    totalServiceAmount     = models.FloatField(default=0.00, null=True, blank=True)
    totalPartsAmount       = models.FloatField(default=0.00, null=True, blank=True)
    total              =  models.FloatField(default=0.00, null=True, blank=True)
    paid               =  models.FloatField(default=0.00, null=True, blank=True)
    due                =  models.FloatField(default=0.00, null=True, blank=True)
    discountAmount     =  models.FloatField(default=0.00, null=True, blank=True)
    newTotal           =  models.FloatField(default=0.00, null=True, blank=True)
    isCompleted        =  models.BooleanField(default = False,null=True)
    expectedAt         =  models.DateTimeField(blank=True, null=True)
    deliveredAt        =  models.DateTimeField(blank=True, null=True)
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['expectedAt','deliveredAt','-createdAt'])
        ]

    def __str__(self):
        return "{} - {}".format(self.jobID, self.vehicleID)

class JobCardImage(models.Model):
    task = models.ForeignKey(JobCardDetail, on_delete=models.CASCADE)
    image = models.FileField(blank=True)

class JobcardServices(models.Model):
    jobcardServidesID = models.AutoField(primary_key=True, unique=True)
    jobID             = models.ForeignKey(JobCardDetail, on_delete=models.CASCADE, blank=True, null=True)
    serviceID         = models.ForeignKey(ServiceDetails, on_delete=models.CASCADE, blank=True, null=True)
    services          = models.CharField(max_length= 120, blank = True, null= True)
    servicePrice      = models.FloatField(max_length= 15, blank = True, null= True)
    servicePrices     = models.CharField(max_length= 120, blank = True, null= True)

    meta              = models.JSONField(encoder=None, null=True)
    createdAt         = models.DateTimeField(auto_now_add=True)
    updatedAt         = models.DateTimeField(auto_now=True)
    isDeleted         = models.BooleanField(default= False,null=True)
    createdBy         = models.CharField(max_length=120)
    updatedBy         = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]

    def __str__(self):
        return f'{self.jobID} - {self.serviceID}'


class JobcardParts(models.Model):
    jobcardPartsID    = models.AutoField(primary_key=True, unique=True)
    jobID             = models.ForeignKey(JobCardDetail, on_delete=models.CASCADE, blank=True, null=True)
    workshopInventoryID = models.ForeignKey(WorkshopInventory, on_delete=models.CASCADE, blank=True, null=True)
    workshopInventoryIDs= models.CharField(max_length= 120, blank = True, null= True)
    partsPrice        = models.FloatField(max_length= 15, blank = True, null= True)
    partsPrices       = models.CharField(max_length= 120, blank = True, null= True)
    partQty           = models.IntegerField(blank = True, null= True)
    partQtys          = models.CharField(max_length= 120, blank = True, null= True)


    meta              = models.JSONField(encoder=None, null=True)
    createdAt         = models.DateTimeField(auto_now_add=True)
    updatedAt         = models.DateTimeField(auto_now=True)
    isDeleted         = models.BooleanField(default= False,null=True)
    createdBy         = models.CharField(max_length=120)
    updatedBy         = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]

    def __str__(self):
        return f'{self.jobID} - {self.partQty}'

class WorkshopCustomer(models.Model):
    workshopCustomerID           = models.AutoField(primary_key=True, unique=True)
    userID         = models.ForeignKey(
                      UserDetail, on_delete=models.CASCADE, blank=True, null=True, default=150)
    cusID           = models.ForeignKey(
                      CustomerDetail, on_delete=models.CASCADE, blank=True, null=True)
    
    meta              = models.JSONField(encoder=None, null=True)
    createdAt         = models.DateTimeField(auto_now_add=True)
    updatedAt         = models.DateTimeField(auto_now=True)
    isDeleted         = models.BooleanField(default= False,null=True)
    createdBy         = models.CharField(max_length=120)
    updatedBy         = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]