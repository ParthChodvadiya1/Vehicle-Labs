from django.db import models

from src.apis.accounts.models import UserDetail

class Accounting(models.Model):
    
    TYPE_CHOICES = (
      ("Jobcard", "jobcard"),
      ("CounterSale", "countersale"),
      ("VendorSaleCard", "vendorsalecard"),
    )

    transactionID    = models.AutoField(primary_key=True, unique=True)
    
    creditAmount     = models.FloatField(null=True, blank=True)
    debitAmount      = models.FloatField(null=True, blank=True)
    balance          = models.FloatField(null=True, blank=True)
    
    userID           = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='sub_user')
    workshopUserID   = models.ForeignKey(UserDetail, on_delete=models.CASCADE, blank=True, null=True, related_name='workshop_user')
    
    description      = models.CharField(max_length=256, blank=True, null=True)
    
    refType         = models.CharField(max_length=128, choices=TYPE_CHOICES, null=True, blank=True)
    refID           = models.IntegerField(null=True, blank=True)
    
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default = False,null=True)
    isActivated     = models.BooleanField(default = True,null=True)
    createdBy       = models.CharField(max_length=120, null=True, blank=True)
    updatedBy       = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['refType', 'refID', '-createdAt'])
        ]

