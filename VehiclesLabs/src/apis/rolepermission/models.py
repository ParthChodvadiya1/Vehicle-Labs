from django.db import models
from src.apis.accounts.models import UserDetail
from src.apis.workshop.models import WorkshopDetail
from multiselectfield import MultiSelectField




DEMO_CHOICES = [
    ("Create", "Create"), 
    ("Update", "Update"),  
    ("Delete", "Delete"),
    ("View", "View"), 
]
class Permissions(models.Model):
    permID = models.AutoField(primary_key=True, unique=True)
    jobcard = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    inventory = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    user = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    workshop = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    counter_sale = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    user_workshop = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True, related_name='wokrshop_user')
    userID = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True, related_name='wokrshop_owner')
    workshopID = models.ForeignKey(WorkshopDetail, on_delete=models.CASCADE,blank=True,null=True)
    
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120,blank=True, null=True)
    updatedBy       = models.CharField(max_length=120,blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]
        

class Marketeer(models.Model):
    mID = models.AutoField(primary_key=True, unique=True)
    admin_report = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    subscription_plan = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    user = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    capture_payment = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    requested_parts = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    service = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    part = MultiSelectField(choices=sorted(DEMO_CHOICES), max_choices=4,blank=True, null=True)
    marketerID = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True, related_name='marketeer')
    userID = models.ForeignKey(UserDetail, on_delete=models.CASCADE,blank=True,null=True, related_name='admin_owner')
    
    meta            = models.JSONField(encoder=None, null=True)
    createdAt       = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    isDeleted       = models.BooleanField(default= False,null=True)
    createdBy       = models.CharField(max_length=120,blank=True, null=True)
    updatedBy       = models.CharField(max_length=120,blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['-createdAt'])
        ]