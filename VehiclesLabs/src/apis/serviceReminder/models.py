from django.db import models
from src.apis.customer.models import CustomerDetail
from src.apis.accounts.models import UserDetail
from src.apis.services.models import ServiceDetails
from src.apis.workshop.models import WorkshopDetail

class ServiceReminder(models.Model):
    sdID           = models.AutoField(primary_key=True, unique=True)
    reminderDate     = models.DateTimeField(null=False, blank=False)
    cusID           = models.ForeignKey(
                      CustomerDetail, on_delete=models.CASCADE, blank=True, null=True)
    serviceID       = models.ManyToManyField(ServiceDetails, related_name='many_services')
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
            models.Index(fields=['reminderDate', '-createdAt'])
        ]