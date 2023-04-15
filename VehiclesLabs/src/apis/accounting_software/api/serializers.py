from rest_framework import serializers
from src.apis.accounting_software.models import Accounting
from src.apis.accounts.api.serializers import UserAccountingSerializer


class EntryRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounting
        fields = '__all__'


class EntryBalanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Accounting
        fields = [
            "balance",
        ]


class EntryListSerializer(serializers.ModelSerializer):
    userID = UserAccountingSerializer(read_only=True)
    class Meta:
        model = Accounting
        fields = '__all__'
