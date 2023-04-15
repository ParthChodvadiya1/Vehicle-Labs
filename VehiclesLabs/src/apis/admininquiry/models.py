from django.db import models

USER_TYPE_CHOICES = (
      ("Vendor", "vendor"),
      ("Workshop Owner", "workshop_owner"),
      ("Other", "other")
    )


class AdminInquiry(models.Model):
    inquiryID   = models.AutoField(primary_key = True, unique = True)
    usertype    = models.CharField(max_length=128, choices=USER_TYPE_CHOICES, null=True, blank=True)
    address     = models.CharField(max_length=450, null=True, blank=True)
    workshopOwnership = models.CharField(max_length=450, null=True, blank=True)
    ownerPhone  = models.CharField(max_length=10, null=True, blank=True)
    ownerName   = models.CharField(max_length=250, null=True, blank=True)
    garageName  = models.CharField(max_length=250, null=True, blank=True)
    latitude    = models.FloatField(null=True, blank=True)
    longitude   = models.FloatField(null=True, blank=True)
    remarks     = models.CharField(max_length=1200, blank=True, null=True )

    meta        = models.JSONField(encoder=None, null=True)
    createdAt   = models.DateTimeField(auto_now_add=True)
    updatedAt   = models.DateTimeField(auto_now=True)
    isDeleted   = models.BooleanField(default= False,null=True)
    createdBy   = models.CharField(max_length=120)
    updatedBy   = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.inquiryID} - {self.address} - {self.ownerPhone} - {self.ownerName} - {self.ownerName} - {self.remarks} - {self.workshopOwnership}'

    class Meta:
        indexes = [
            models.Index(fields=['usertype', 'workshopOwnership', 'ownerPhone', 'ownerName', 'garageName','-createdAt'])
        ]