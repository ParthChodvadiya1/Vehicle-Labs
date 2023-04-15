from django.db import models
from django.contrib.postgres.fields import JSONField
from src.apis.accounts.models import UserDetail
from src.apis.media.models import MediaDetails
# Create your models here.


class WorkshopDetail(models.Model):
    workshopID          = models.AutoField(primary_key=True, unique=True)
    userID              = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True)
    workshopname        = models.CharField(max_length=20, null=False)
    workshopemail       = models.EmailField(null=False)
    workshopphone       = models.CharField(max_length=10, null=False)
    workshopaddress     = models.CharField(max_length=200, null=False)
    media               = models.ForeignKey(MediaDetails, on_delete=models.CASCADE, blank=True, null=True)
    logo                = models.ImageField(null=True)
    expectedDay        = models.IntegerField(blank=True, null=True)
    gst_per             = models.FloatField(default=0.00, null=True, blank=True)
    gst_no              = models.CharField(max_length=128, blank=True, null=True)
    invoice_title       = models.CharField(max_length=128, blank=True, null=True)
    latitude        = models.FloatField(null=True, blank=True)
    longitude       = models.FloatField(null=True, blank=True)

    meta                = models.JSONField(encoder=None, null=True)
    createdAt           = models.DateTimeField(auto_now_add=True)
    updatedAt           = models.DateTimeField(auto_now=True)
    isDeleted           = models.BooleanField(default = False,null=True)
    createdBy           = models.CharField(max_length=120)
    updatedBy           = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['workshopname','workshopemail','workshopphone', '-createdAt'])
        ]

class WorkShopManager(models.Model):
    workshopmanageID          = models.AutoField(primary_key=True, unique=True)
    userID          = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='created_user')
    usermanageID    = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='user_manager')
    
    workshopID          = models.ForeignKey(WorkshopDetail, on_delete=models.CASCADE, blank=True, null=True)
    meta                = models.JSONField(encoder=None, null=True)
    createdAt           = models.DateTimeField(auto_now_add=True)
    updatedAt           = models.DateTimeField(auto_now=True)
    isDeleted           = models.BooleanField(default = False,null=True)
    createdBy           = models.CharField(max_length=120)
    updatedBy           = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]