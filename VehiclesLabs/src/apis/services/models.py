from django.db import models
from src.apis.accounts.models import UserDetail

class ServiceDetails(models.Model):
    serviceID       = models.AutoField(primary_key=True, unique=True)
    serviceName     = models.CharField(max_length=128, null=False)
    serviceType     = models.CharField(max_length=128, null=False)
    servicePrice      = models.FloatField(max_length=10, null=True)
    meta            = models.JSONField(encoder=None, null=True)
    excel_file          = models.FileField(blank= True, null = True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    def __str__(self):
        return self.serviceName

    class Meta:
        indexes = [
            models.Index(fields=['serviceName','serviceType','-createdAt'])
        ]
        