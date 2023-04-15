from django.db import models
from django.contrib.postgres.fields import JSONField

class fueltype(models.Model):

    fuelID          = models.AutoField(primary_key=True, unique=True)
    fueltype        = models.CharField(max_length=30, null=False, unique=True)
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)
    
    def __str__(self):
        return self.fueltype

    class Meta:
        indexes = [
            models.Index(fields=['fueltype', '-createdAt'])
        ]