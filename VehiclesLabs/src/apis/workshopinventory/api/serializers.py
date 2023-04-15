from rest_framework import serializers
from src.apis.workshopinventory.models import WorkshopInventory
from src.apis.parts.api.serializers import PartSerializer, PartNTSerializer
from src.apis.vendorinventory.api.serializers import VendorInventoryDetailSerializer
from src.apis.vendors.api.serializers import  VendorSerializer
from src.apis.workshop.api.serializers import WorkshopDetailSerializer
from src.apis.accounting_software.api.serializers import EntryBalanceSerializer
from src.apis.accounting_software.models import Accounting
from src.apis.accounts.models import UserDetail

class WorkshopInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'workshopID',
            'vendorInventoryID',
            'partID',
            'workshopPartQty',
            'workshopPartPrice',
            'total',
            'paid',
            'due',
            'delivered',
            'vendorID',
            'createdAt',
            'updatedAt'
        ]

class WorkshopInventoryDetailSerializer(serializers.ModelSerializer):
    workshopID = WorkshopDetailSerializer(read_only = True)
    vendorInventoryID = VendorInventoryDetailSerializer(read_only=True)
    partID = PartSerializer(read_only = True)
    vendorID = VendorSerializer(read_only=True)
    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'workshopID',
            'vendorInventoryID',
            'partID',
            'vendorID',
            'workshopPartQty',
            'workshopPartPrice',
            'total',
            'due',
            'paid',
            'delivered',
            'orderCompleted',
            'minimum_qty',
            'createdAt',
            'updatedAt'
        ]

class WorkshopInventoryPartQtySerializer(serializers.ModelSerializer):
    partID = PartNTSerializer(read_only = True)
    class Meta:
        model = WorkshopInventory
        fields = [
            'partID',
            'workshopPartQty',
        ]

class WorkshopInventoryRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'workshopPartQty',
            'workshopPartPrice',
            'workshopID',
            'vendorInventoryID',
            'vendorID',
            'partID',
            'orderCompleted',
            'delivered',
            'createdAt',
            'updatedAt'
        ]

    def create(self, validated_data):

        workshopPartQty = validated_data.get("workshopPartQty")
        workshopPartPrice = validated_data.get("workshopPartPrice")
        total = workshopPartQty * workshopPartPrice
        vendorInventoryID = validated_data.get("vendorInventoryID")
        vendorID = validated_data.get("vendorID")
        vendorPartQty = vendorInventoryID.vendorPartQty
        
        if vendorPartQty > 0:
            if vendorPartQty >= workshopPartQty:
                finalVenPartQty = vendorPartQty - workshopPartQty
                vendorInventoryID.vendorPartQty = finalVenPartQty 
                vendorInventoryID.save()
                WorkshopInventory.objects.update_or_create(
                    workshopPartQty = validated_data.get("workshopPartQty"),
                    workshopPartPrice = validated_data.get("workshopPartPrice"),
                    total = total,
                    due=total,
                    workshopID = validated_data.get("workshopID"),
                    vendorInventoryID = validated_data.get("vendorInventoryID"),
                    vendorID = validated_data.get("vendorID"),
                    partID = validated_data.get("partID"),
                    delivered= validated_data.get("delivered"),
                    orderCompleted = validated_data.get("orderCompleted")
                )
                return validated_data
            else:
                raise serializers.ValidationError(f"You can Buy {vendorPartQty} parts of this type form this vendor")
        else:
            raise serializers.ValidationError("This part is not available in vendor inventory")

class WorkshopRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'workshopPartQty',
            'workshopPartPrice',
            'workshopID',
            'partID',
            'orderCompleted',
            'createdAt',
            'updatedAt'
        ]

    def create(self, validated_data):
        

        workshop_obj = WorkshopInventory.objects.update_or_create(
            workshopPartQty = validated_data.get("workshopPartQty"),
            workshopPartPrice = validated_data.get("workshopPartPrice"),
            workshopID = validated_data.get("workshopID"),
            partID = validated_data.get("partID"),
            orderCompleted = validated_data.get("orderCompleted")
        )
        return workshop_obj

        
        # if vendorPartQty > 0:
        #     if vendorPartQty >= workshopPartQty:
        #         finalVenPartQty = vendorPartQty - workshopPartQty
        #         vendorInventoryID.vendorPartQty = finalVenPartQty 
        #         vendorInventoryID.save()
        #         WorkshopInventory.objects.update_or_create(
        #             workshopPartQty = validated_data.get("workshopPartQty"),
        #             workshopPartPrice = validated_data.get("workshopPartPrice"),
        #             workshopID = validated_data.get("workshopID"),
        #             vendorInventoryID = validated_data.get("vendorInventoryID"),
        #             vendorID = validated_data.get("vendorID"),
        #             partID = validated_data.get("partID")
        #         )
        #         return validated_data
        #     else:
        #         raise serializers.ValidationError(f"You can Buy {vendorPartQty} parts of this type form this vendor")
        # else:
        #     raise serializers.ValidationError("This part is not available in vendor inventory")

class InventoryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'paid',
        ]
    def update(self, instance, validated_data):
        paid = validated_data.get('paid')
        workshopInventoryID = instance.workshopInventoryID
        obj = WorkshopInventory.objects.get(workshopInventoryID=workshopInventoryID)
        obj.paid = obj.paid + paid
        obj.due = obj.total - obj.paid 
        obj.save()
        
        user_obj = Accounting.objects.filter(userID=obj.userID).order_by('-createdAt')[::-1]
        serializer = EntryBalanceSerializer(user_obj, many=True)
        vendorUserID = validated_data.get('vendorUserID')
        vendorUserID = UserDetail.objects.get(userID=vendorUserID)
        if user_obj:
            balance = serializer.data[0]["balance"]
            balance = balance + paid
        else:
            balance = paid
            
        obj_ = Accounting.objects.create(
            creditAmount = paid,
            balance = balance,
            userID=obj.userID,
            workshopUserID=vendorUserID,
            description="Vendor SaleCard Payment captured.",
            refType="VendorSaleCard",
            refID=vendorUserID
        )
        
        return instance

class OrderedInventoryCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'orderCompleted'
        ]

class OrderedInventoryDeliveredSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)
    class Meta:
        model = WorkshopInventory
        fields = [
            'workshopInventoryID',
            'delivered',
            'otp'
        ]


