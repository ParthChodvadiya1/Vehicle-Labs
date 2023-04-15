from django.db import models
from django.contrib.postgres.fields import JSONField
from src.apis.accounts.models import UserDetail
from src.apis.media.models import MediaDetails
from src.apis.workshop.models import WorkshopDetail
# Create your models here.

class SoftDeleteManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        query_set = super(SoftDeleteManager, self).get_query_set()
        return query_set.filter(isDeleted__isnull = True)

class VendorDetail(models.Model):
    vendorID          = models.AutoField(primary_key=True, unique=True)
    userID              = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True)
    vendorname        = models.CharField(max_length=20, null=False)
    vendoremail       = models.EmailField(null=False)
    vendorphone       = models.CharField(max_length=10, null=False)
    vendoraddress     = models.CharField(max_length=200, null=False)
    logo                = models.ImageField(null=True)
    media               = models.ForeignKey(MediaDetails, on_delete=models.CASCADE, blank=True, null=True)
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

    objects = SoftDeleteManager()

    class Meta:
        indexes = [
            models.Index(fields=['vendorname','vendoremail','vendorphone','-createdAt'])
        ]

    def __str__(self):
        return "{} -{}".format(self.vendorname, self.vendorphone)

    @property
    def imageURL(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url

class VendorManager(models.Model):
    vendormanageID   = models.AutoField(primary_key=True, unique=True)
    userID           = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='vendor_created_user')
    usermanageID     = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='vendor_user_manager')
    vendorID         = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, blank=True, null=True)

    meta             = models.JSONField(encoder=None, null=True)
    createdAt        = models.DateTimeField(auto_now_add=True)
    updatedAt        = models.DateTimeField(auto_now=True)
    isDeleted        = models.BooleanField(default = False,null=True)
    createdBy        = models.CharField(max_length=120)
    updatedBy        = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]