from django.db import models
from django.contrib.postgres.fields import JSONField

class VehicleBrand(models.Model):

    brandID         = models.AutoField(primary_key=True, unique=True)
    brandname       = models.CharField(max_length=50, null=True)
    brandmodel      = models.CharField(max_length=40, null= True)
    meta            = models.JSONField(encoder=None, null=True)
    excel_file          = models.FileField(blank= True, null = True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)
    
    def __str__(self):
        return self.brandname 

    class Meta:
        indexes = [
            models.Index(fields=['brandname','brandmodel','-createdAt'])
        ]
