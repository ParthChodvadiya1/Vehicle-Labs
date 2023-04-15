from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from src.apis.accounts.models import UserDetail
from django.contrib.postgres.fields import JSONField

class CustomerDetail(models.Model):
    cusID           = models.AutoField(primary_key=True, unique=True)
    cusname         = models.CharField(max_length=255, null=False)
    cusemail        = models.EmailField(blank=True, null=True)
    cusphone        = models.CharField(max_length=10, null=False)
    cusaddress      = models.CharField(max_length=255, blank=True, null=True)
    userID          = models.ForeignKey(UserDetail,blank=True,null=True,on_delete=models.CASCADE)
    remarks         = models.CharField(max_length=255, blank=True, null=True)
    cussignature    = models.FileField(blank = True , null=True)
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)
    latitude        = models.FloatField(null=True, blank=True)
    longitude       = models.FloatField(null=True, blank=True)


    def __str__(self):
        return "{} - {}".format(self.cusID, self.cusname)

    @property
    def imageURL(self):
        try:
            url = self.signature.url
        except:
            url = ''
        return url

    class Meta:
        indexes = [
            models.Index(fields=['cusname', 'cusemail', 'cusphone', '-createdAt'])
        ]
