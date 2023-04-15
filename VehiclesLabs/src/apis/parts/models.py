from django.db import models
from src.apis.vendors.models import VendorDetail
from VehiclesLabs.aws.utils import MediaRootS3BotoStorage

# Create your models here.

class PartDetails(models.Model):
    partID        = models.AutoField(primary_key=True, unique=True)
    partName      = models.CharField(max_length=128, blank=True, null=True)
    partType      = models.CharField(max_length=128, blank=True, null=True)
    partPrice     = models.FloatField(max_length=10, blank=True, null=True)
    partNumber    = models.CharField(max_length=128, blank=True, null=True)
    HSNNumber     = models.CharField(max_length=128, blank=True, null=True)
    companyName   = models.CharField(max_length=128, blank=True, null=True)
    partNote      = models.CharField(max_length=128, blank=True, null=True)
    partMedia     = models.JSONField(encoder=None,   blank=True, null=True)
    vehicleModel  = models.CharField(max_length=128, blank=True, null=True)
    varient       = models.CharField(max_length=128, blank=True, null=True)
    page          = models.CharField(max_length=128, blank=True, null=True)
    refNo         = models.CharField(max_length=128, blank=True, null=True)
    blockIndex    = models.CharField(max_length=128, blank=True, null=True)
    localName     = models.CharField(max_length=128, blank=True, null=True)

    
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,blank=True, null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['partName', 'partType', 'partNumber', 'HSNNumber', 'companyName', 'vehicleModel', 'varient', '-createdAt'])
        ]

    def __str__(self):
        return f'{self.partName}, {self.partNumber}, {self.companyName}, {self.partID}, {self.partPrice}'

class RequestedParts(models.Model):
    reqpartID     = models.AutoField(primary_key=True, unique=True)
    partName      = models.CharField(max_length=128, blank=True, null=True)
    partType      = models.CharField(max_length=128, blank=True, null=True)
    partPrice     = models.FloatField(max_length=10, blank=True, null=True)
    partNumber    = models.CharField(max_length=128, blank=True, null=True)
    rackNumber    = models.CharField(max_length=128, blank=True, null=True)
    HSNNumber     = models.CharField(max_length=128, blank=True, null=True)
    companyName   = models.CharField(max_length=128, blank=True, null=True)
    partNote      = models.CharField(max_length=128, blank=True, null=True)
    partMedia     = models.JSONField(encoder=None, null=True)
    vehicleModel  = models.CharField(max_length=128,blank=True, null=True)
    varient       = models.CharField(max_length=128,blank=True, null=True)
    page          = models.CharField(max_length=128,blank=True, null=True)
    refNo        = models.CharField(max_length=128,blank=True, null=True)
    blockIndex    = models.CharField(max_length=128,blank=True, null=True)
    localName     = models.CharField(max_length=128,blank=True, null=True)
    
    vendorPartQty       = models.IntegerField(null = True, blank = True)
    vendorPartPrice     = models.FloatField(max_length=12, null = True, blank = True)
    vendorID            = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, null = True , blank = True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,blank=True, null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['partName', 'partType', 'partNumber', 'HSNNumber', 'companyName', 'vehicleModel', 'varient', '-createdAt'])
        ]


class ReuestPartPhoneOTP(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    validated = models.BooleanField(default= False)
    otp_session_id = models.CharField(max_length=120, null=True, default = "")
    
    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


class PartImage(models.Model):
    partImgID     = models.AutoField(primary_key=True, unique=True)
    partImgName   = models.CharField(max_length=256,null=True, blank=True)
    partImage     = models.FileField(upload_to='', storage=MediaRootS3BotoStorage, blank = True , null=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True,blank=True, null=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.partImgID} - {self.partImgName} - {self.partImage}'

    class Meta:
        indexes = [
            models.Index(fields=['partImgName', '-createdAt'])
        ]

class PartVideo(models.Model):
    partVidID     = models.AutoField(primary_key=True, unique=True)
    partVidName   = models.CharField(max_length=256,null=True, blank=True)
    PartVideo     = models.FileField(upload_to='', storage=MediaRootS3BotoStorage, blank = True , null=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True,blank=True, null=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.partVidID} - {self.partVidName} - {self.PartVideo}'

    class Meta:
        indexes = [
            models.Index(fields=['partVidName', '-createdAt'])
        ]