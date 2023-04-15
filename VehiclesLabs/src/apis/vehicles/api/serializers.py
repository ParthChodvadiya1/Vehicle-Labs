from rest_framework import serializers
from src.apis.vehicles.models import VehiclesDetail


class VehiclesSerializer(serializers.ModelSerializer):
    vehicleID = serializers.IntegerField(required=False)

    class Meta:
        model = VehiclesDetail
        fields = [
            'vehicleID',
            'vehiclenumber',
            'kilometer',
            'chasisnumber',
            'enginenumber',
            'fuelIndicator',
            'createdAt',
            'updatedAt'
        ]


class VehiclesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclesDetail
        fields = '__all__'
