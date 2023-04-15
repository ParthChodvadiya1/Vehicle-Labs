from django.db.models import fields
from rest_framework import serializers

from src.apis.customer.api.serializers import CustomerDetailSerailizer
from src.apis.vehiclebrands.api.serializers import VehicleBrandSerializer
from src.apis.customerBookAppointment.models import BookAppointment
from src.apis.services.api.serializers import ServiceSerializer
from src.apis.services.models import ServiceDetails
from src.apis.services.api.serializers import ServiceSerializer
from src.apis.workshop.api.serializers import WorkshopSerializer




class BookAppointmentListSerializer(serializers.ModelSerializer):
    cusID       = CustomerDetailSerailizer(read_only=True)
    brandID     = VehicleBrandSerializer(read_only=True)
    workshopID = WorkshopSerializer(read_only=True)
    servicesID     = ServiceSerializer(many=True,read_only=True)
    class Meta:
        model = BookAppointment 
        fields = [
            'appointID',
            'servicesID',
            'userID',
            'workshopID',
            'vehiclenumber',
            'appointDate',
            'cusID',
            'brandID',
            'createdAt',
            'updatedAt',
        ]



class BookAppointmentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAppointment
        fields = [
            'vehiclenumber',
            'appointDate',
            'brandID',
            'cusID',
            'servicesID',
            'userID',
            'workshopID'
        ]
    def create(self,validated_data):

        book_appoint_obj = BookAppointment.objects.create(
            vehiclenumber=validated_data.get("vehiclenumber"),
            appointDate=validated_data.get("appointDate"),
            brandID=validated_data.get("brandID"),
            cusID=validated_data.get("cusID"),
            userID=validated_data.get("userID"),
            workshopID=validated_data.get("workshopID"),
        )
        book_appoint_obj.servicesID.set(validated_data.get("servicesID"))
        book_appoint_obj.save()

        return validated_data
        
class BookAppointmentUpdateSerializer(serializers.ModelSerializer):
    servicesID = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=ServiceDetails.objects.all())
    class Meta:
        model = BookAppointment
        fields = [
            'vehiclenumber',
            'appointDate',
            'brandID',
            'cusID',
            'servicesID',
            'userID',
            'workshopID'
        ]