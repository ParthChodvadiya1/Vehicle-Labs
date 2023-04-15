from django.db import models
from src.apis.accounts.models import UserDetail
# Create your models here.

class Notifications(models.Model):
    notifyID        = models.AutoField(primary_key=True, unique=True) 
    userID          = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True)
    message         = models.CharField(max_length=256, blank=True, null=True)
    is_read          = models.BooleanField(default = False, blank=True, null=True)
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]