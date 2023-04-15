from src.apis.customer.api.serializers import CustomerDetailSerailizer, CustomerSerializer
from rest_framework import serializers
from src.apis.admininquiry.models import AdminInquiry

class AdminInquiryRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminInquiry
        fields = [
            'address',
            'ownerPhone',
            'ownerName',
            'latitude',
            'longitude',
            'remarks',
            'usertype',
            'garageName',
            'workshopOwnership',
        ]


class AdminInquiryDetailSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = AdminInquiry
        fields = [
            'inquiryID',
            'address',
            'ownerPhone',
            'ownerName',
            'garageName',
            'workshopOwnership',
            'usertype',
            'latitude',
            'longitude',
            'remarks',
            'createdAt',
            'updatedAt',
        ]
        