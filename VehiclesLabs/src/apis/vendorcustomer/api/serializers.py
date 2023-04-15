from rest_framework import serializers

from src.apis.customer.models import CustomerDetail
from src.apis.vendorcustomer.models import VendorCustomer
from src.apis.parts.api.serializers import PartSerializer
from src.apis.customer.api.serializers import CustomerDetailSerailizer, CustomerSerializer
from src.apis.vendorinventory.api.serializers import VendorInventoryDetailSerializer


class VendorCustomerRegisterSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required = False)

    class Meta:
        model = VendorCustomer
        fields = [
            'customer',
            'cusPartQty',
            'cusPartPrice',
            'vendorInventoryID',
            'vendorID',
            'delivered',
            'partID',
        ]

    def create(self, validated_data):

        cusPartQty         = validated_data.    get('cusPartQty')
        vendorInventoryID  = validated_data.get('vendorInventoryID')
        initialQty         = vendorInventoryID.vendorPartQty
        finalQty           = initialQty - cusPartQty
        vendorInventoryID.vendorPartQty = finalQty
        vendorInventoryID.save()

        customerdata = validated_data.pop('customer')
        cusphone = customerdata["cusphone"]
        try:
            customer_obj = CustomerDetail.objects.get(cusphone=cusphone)
        except:
             
            customer_obj = CustomerDetail.objects.create(
                cusname=customerdata['cusname'],
                cusaddress=customerdata['cusaddress'],
                cusemail=customerdata['cusemail'],
                cusphone=customerdata['cusphone'],
                remarks=customerdata['remarks'],
                cussignature=customerdata['cussignature'],
            )            
        customer_obj.save()
        VendorCustomer.objects.create(
            cusPartQty=validated_data.get("cusPartQty"),
            cusPartPrice=validated_data.get("cusPartPrice"),
            vendorInventoryID=validated_data.get("vendorInventoryID"),
            partID=validated_data.get("partID"),
            cusID=customer_obj,
            delivered=validated_data.get("delivered"),
            vendorID= validated_data.get('vendorID')
        )
        return customer_obj


class VendorCustomerSerializer(serializers.ModelSerializer):
    
    cusID = CustomerDetailSerailizer(required = False)
    vendorInventoryID = VendorInventoryDetailSerializer(required = False)
    partID = PartSerializer(required=False)

    class Meta:
        model = VendorCustomer
        fields = [
            'vendorCustomerID',
            'cusPartQty',
            'cusPartPrice',
            'vendorInventoryID',
            'cusID',
            'partID',
            'delivered',
            'createdAt',
            'updatedAt'
        ]

class VendorCustomerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorCustomer
        fields = [
            'vendorCustomerID',
            'cusPartQty',
            'cusPartPrice',
        ]


class CustomerDeliveredSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCustomer
        fields = [
            'vendorCustomerID',
            'delivered'
        ]

