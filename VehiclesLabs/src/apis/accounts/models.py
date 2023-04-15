from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from src.apis.media.models import MediaDetails
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
def get_expiredAt():
    return timezone.now() + timedelta(days=15)

class UserDetail(AbstractUser):

    TYPE_CHOICES = (
      ("Admin", "admin"),
      ("Workshop Owner", "workshop_owner"),
      ("Workshop User", "workshop_user"),
      ("Vendor", "vendor"),
      ("Customer", "customer"),
      ("Workshop Manager","workshop_manager"),
      ("Vendor Manager","vendor_manager"),
      ("Marketeer","marketeer")
    )

    utype           = models.CharField(max_length=128, choices=TYPE_CHOICES, null=True, blank=True)
    userID          = models.AutoField(primary_key=True, unique=True)
    username        = models.CharField(max_length=128, null=False, unique=True)
    email           = models.EmailField(null=False)
    userphone       = models.CharField(max_length=10, null=True)
    useraddress     = models.CharField(max_length=200, null=True,blank=True)
    media           = models.ForeignKey(MediaDetails, on_delete=models.CASCADE, blank=True, null=True)
    profileimage    = models.ImageField(null=True, blank=True,  upload_to='')
    latitude        = models.FloatField(null=True, blank=True)
    longitude       = models.FloatField(null=True, blank=True)
    password        = models.CharField(max_length=255, null=False)
    token           = models.CharField(max_length=1000, null=True)
    resetpasswordtoken           = models.CharField(max_length=1000, null=True)
    trialendAt        = models.DateTimeField(null= True, blank = True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    expiredAt       = models.DateTimeField(default=get_expiredAt)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    isActivated     = models.BooleanField(default = True,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    REQUIRED_FIELDS = ['userphone']

    class Meta:
        indexes = [
            models.Index(fields=['utype', 'username', 'email', 'userphone', 'expiredAt', 'isActivated','-createdAt'])
        ]

    def __str__(self):
        return f"{self.userID} - {self.username} - {self.userphone} - {self.useraddress}"

    @property
    def imageURL(self):
        try:
            url = self.profileImage.url
        except:
            url = ''
        return url



class PhoneOTP(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    count = models.IntegerField(default=0)
    validated = models.BooleanField(default= False)
    otp_session_id = models.CharField(max_length=120, null=True, default = "")
    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


class SubscriptionRecord(models.Model):

    subscriptionID  =  models.AutoField(primary_key=True, unique=True)
    amount          =  models.IntegerField(null=False, blank=False)
    userID          =  models.ForeignKey(UserDetail,on_delete=models.CASCADE, blank=False, null=False)
    timePeriod      =  models.IntegerField(null=False, blank=False)
    paymentID       =  models.CharField(max_length=256,blank=True, null=True)
    razor_res       = models.JSONField(encoder=None, null=True)
    meta            = models.JSONField(encoder=None, null=True)
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)




class SubscriptionType(models.Model):


    subTypeID       =  models.AutoField(primary_key=True, unique=True)
    amount          =  models.IntegerField(null=False, blank=False)
    timePeriod      =  models.IntegerField(null=False, blank=False)
    description     =  models.CharField(max_length=200,null=True,blank=True)
    subName         = models.CharField(max_length=128, null=True, blank=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.subTypeID} - {self.amount} - {self.description} - {self.timePeriod}"

