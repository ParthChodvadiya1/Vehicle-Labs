from rest_framework import serializers
from src.apis.fueltype.models import fueltype


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = fueltype
        fields = [
            'fuelID',
            'fueltype',
            'createdAt',
            'updatedAt',
        ]


class FuelTypeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = fueltype
        fields = [
            'fuelID',
            'fueltype',
            'createdAt',
            'updatedAt',
        ]

    def validate_fuelname(self, value):
        qs = fueltype.objects.filter(fuelname__ixact=value)
        if qs.exists():
            raise serializers.validationerror("This fuel type already exist")
        else:
            return value
