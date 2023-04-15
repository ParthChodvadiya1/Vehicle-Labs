from rest_framework import serializers

from src.apis.customer.models import CustomerDetail


class CustomerRegisterSerializer(serializers.ModelSerializer):
    cusID = serializers.IntegerField(required=False)

    class Meta:
        model = CustomerDetail
        fields = [
            'cusID',
            'cusname',
            'cusemail',
            'cusphone',
            'cusaddress',
            'remarks',
            'cussignature',
            'userID',
        ]
        extra_kwargs = {
            'cusphone': {'validators': []},
        }


class CustomerSerializer(serializers.ModelSerializer):
    cusID = serializers.IntegerField(required=False)

    class Meta:
        model = CustomerDetail
        fields = [
            'cusID',
            'cusname',
            'cusemail',
            'cusphone',
            'cusaddress',
            'remarks',
            'cussignature',
            'userID',
            'createdAt',
            'updatedAt',
        ]
        extra_kwargs = {
            'cusphone': {'validators': []},
        }

class CustomerSerializerCounter(serializers.ModelSerializer):
    cusID = serializers.IntegerField(required=False)

    class Meta:
        model = CustomerDetail
        fields = [
            'cusID',
            'cusname',
            'cusemail',
            'cusphone',
            'cusaddress',
            'userID',
            'createdAt',
            'updatedAt',
        ]
        extra_kwargs = {
            'cusphone': {'validators': []},
        }


class CustomerAppointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = [
            'cusname',
            'cusemail',
            'cusphone',
            'cusaddress',
            'remarks',
            'cussignature',
            'createdAt',
            'updatedAt',
        ]
        extra_kwargs = {
            'cusphone': {'validators': []},
        }


class CustomerDetailSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = [
            'cusID',
            'cusname',
            'cusemail',
            'cusphone',
            'cusaddress',
            'remarks',
            'cussignature',
            'userID',
            'createdAt',
            'updatedAt',
        ]
