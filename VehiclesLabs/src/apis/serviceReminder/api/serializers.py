from rest_framework import serializers

from src.apis.services.models import ServiceDetails
from src.apis.serviceReminder.models import ServiceReminder
from src.apis.customer.api.serializers import CustomerDetailSerailizer
from src.apis.services.api.serializers import ServiceSerializer
from src.apis.workshop.api.serializers import WorkshopSerializer




class ServiceReminderListSerializer(serializers.ModelSerializer):
    cusID       = CustomerDetailSerailizer(read_only=True)
    workshopID = WorkshopSerializer(read_only=True)
    serviceID     = ServiceSerializer(many=True,read_only=True)
    class Meta:
        model = ServiceReminder 
        fields = [
            'sdID',
            'serviceID',
            'userID',
            'workshopID',
            'reminderDate',
            'cusID',
            'createdAt',
            'updatedAt',
        ]

class ServiceReminderEmail(serializers.ModelSerializer):
    cusID       = CustomerDetailSerailizer(read_only=True)
    class Meta:
        model = ServiceReminder 
        fields = [
            'sdID',
            'reminderDate',
            'cusID',
        ]



class ServiceReminderRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReminder
        fields = [
            'reminderDate',
            'cusID',
            'serviceID',
            'userID',
            'workshopID'
        ]
    def create(self,validated_data):

        service_reminder_obj = ServiceReminder.objects.create(
            reminderDate=validated_data.get("reminderDate"),
            cusID=validated_data.get("cusID"),
            userID=validated_data.get("userID"),
            workshopID=validated_data.get("workshopID"),
        )
        service_reminder_obj.serviceID.set(validated_data.get("serviceID"))
        service_reminder_obj.save()

        return validated_data
        
class ServiceReminderUpdateSerializer(serializers.ModelSerializer):
    serviceID = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=ServiceDetails.objects.all())
    class Meta:
        model = ServiceReminder
        fields = [
            'reminderDate',
            'cusID',
            'serviceID',
            'userID',
            'workshopID'
        ]