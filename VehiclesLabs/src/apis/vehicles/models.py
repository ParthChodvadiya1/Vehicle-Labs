from django.db import models
from django.contrib.postgres.fields import JSONField
from src.apis.accounts.models import UserDetail
from src.apis.customer.models import CustomerDetail 
# Create your models here.


class VehiclesDetail(models.Model):
    vehicleID       = models.AutoField(primary_key=True, unique=True)
    userID          = models.ForeignKey(
                          UserDetail, on_delete=models.CASCADE, blank=True, null=True)
    vehiclenumber   = models.CharField(max_length=18, null=False)
    kilometer       = models.FloatField(max_length=18, null=True)
    chasisnumber    = models.CharField(max_length=17, null=True)
    enginenumber    = models.CharField(max_length=17, null=True)
    fuelIndicator   = models.FloatField(max_length= 15, null=True, blank= True)
    
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)
    
    def __str__(self):
        return "{} -{}".format(self.vehicleID, self.vehiclenumber)
    class Meta:
        indexes = [
            models.Index(fields=['vehiclenumber','chasisnumber','enginenumber','-createdAt'])
        ]
