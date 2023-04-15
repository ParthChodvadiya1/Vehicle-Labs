from django.db import models
from VehiclesLabs.aws.utils import MediaRootS3BotoStorage

mediaType_choices = ( 
    ("Image", "Image"), 
    ("Video", "Video"), 
)

class MediaDetails(models.Model):
    mediaID     = models.AutoField(primary_key=True, unique=True)
    mediaType   = models.CharField(max_length=15, choices= mediaType_choices, null=True, blank=True)
    mediaURL    = models.FileField(upload_to='', storage=MediaRootS3BotoStorage, blank = True , null=True)

    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True,blank=True, null=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120)
    updatedBy       = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=['mediaType', '-createdAt'])
        ]

    def __str__(self):
        return f'{self.mediaID} - {self.mediaType} - {self.mediaURL}'