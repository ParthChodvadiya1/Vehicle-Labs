from src.apis.workshop.models import WorkshopDetail
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from src.apis.vendorsalecard.models import VendorSaleCard, VendorPartSale
from src.apis.workshop.api.serializers import WorkshopDetailSerializer
from src.apis.customer.api.serializers import CustomerSerializer
from src.apis.parts.api.serializers import PartSerializer
from src.apis.vendorinventory.api.serializers import VendorInventoryDetailSerializer
from src.apis.vendorinventory.models import VendorInventory
from src.apis.customer.models import CustomerDetail
from src.apis.jobcards.models import WorkshopCustomer
from src.apis.accounting_software.api.serializers import EntryBalanceSerializer
from src.apis.accounting_software.models import Accounting
from src.apis.accounts.models import UserDetail


class VendorPartSaleRegisterSerializer(ModelSerializer):
    class Meta:
        model = VendorPartSale
        fields = [
            'partID',
            'partPrice',
            'partQty',
            'vendorInventoryID',
            'vendorPartSaleID',
        
        ]
        
class VendorPartSaleCard(ModelSerializer):
    class Meta:
        model = VendorPartSale
        fields = [
            'partID',
            'partPrice',
            'partQty',
            'vendorInventoryID'
        ]


class VendorSaleCardRegisterSerializer(ModelSerializer):
    partsale = VendorPartSaleCard(many= True, required=False)
    customer = CustomerSerializer(required=False)
    class Meta:
        model = VendorSaleCard
        fields = [
            'saleType',
            'workshopID',
            'cusID',
            'vendorID',
            'partsale',
            'customer',
            'userID',
        ]

    def create(self, validated_data):
        saleType = validated_data.get('saleType')

        if saleType == "Workshop":
            salecard_obj = VendorSaleCard.objects.create(
                saleType = validated_data.get('saleType'),
                workshopID = validated_data.get('workshopID'),
                vendorID= validated_data.get('vendorID'),
                delivered=validated_data.get('delivered'),
                userID=validated_data.get("userID")
            )
        elif saleType == "Customer":
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
                    userID=validated_data.get('userID')
                )            
            customer_obj.save()
            
            salecard_obj = VendorSaleCard.objects.create(
                saleType = validated_data.get('saleType'),
                cusID = customer_obj,
                vendorID= validated_data.get('vendorID'),
                delivered=validated_data.get('delivered'),
                userID=validated_data.get("userID")
            )

            try:
                workshop_customer = WorkshopCustomer.objects.get(cusID = customer_obj,userID=validated_data.get("userID"))
            except:
                workshop_customer = WorkshopCustomer.objects.create(
                    cusID = customer_obj,
                    userID=validated_data.get("userID")
                )
                
        partsaleID = validated_data.pop("partsale")
        totallist = 0

        for part in partsaleID:
            salepart_obj = VendorPartSale.objects.create(
                partID = part['partID'],
                partPrice = part['partPrice'],
                partQty = part['partQty'], 
                vendorInventoryID = part['vendorInventoryID']
            )
            parts = part['partPrice'] * part['partQty']
            totallist += parts
            
            venInvObj  = VendorInventory.objects.get(vendorInventoryID = part["vendorInventoryID"].vendorInventoryID)
            oldQty = venInvObj.vendorPartQty
            newQty = oldQty - part['partQty']
            venInvObj.vendorPartQty = newQty
            venInvObj.save()
            
        salecard_obj.partSaleID = salepart_obj
        salecard_obj.total = totallist
        salecard_obj.due = totallist
        salecard_obj.newTotal = totallist
        salecard_obj.delivered = False
        salecard_obj.save()


        return validated_data



class VendorPartSaleDetailSerializer(ModelSerializer):
    partID = PartSerializer(read_only = True)
    vendorInventoryID = VendorInventoryDetailSerializer(read_only = True)

    class Meta:
        model = VendorPartSale
        fields =[
            'vendorPartSaleID',
            'vendorInventoryID',
            'partID',
            'partQty',
            'partPrice',
            'createdAt',
            'updatedAt',            
        ]


class VendorSaleCardDetail(ModelSerializer):
    workshopID = WorkshopDetailSerializer(read_only = True)
    cusID = CustomerSerializer(read_only = True)
    partSaleID = VendorPartSaleDetailSerializer(read_only = True)
    class Meta:
        model = VendorSaleCard
        fields=[
            'vendorsalecardID',
            'saleType',
            'total',
            'paid',
            'due',
            'newTotal',
            'discountAmount',
            'delivered',
            'completed',
            'createdAt',
            'updatedAt',  
            'partSaleID',
            'cusID',
            'vendorID',
            'workshopID',
            'userID',  
        ]




class VendorSaleCardPaymentSerializer(ModelSerializer):
    vendorUserID = serializers.CharField(required=False)
    class Meta:
        model = VendorSaleCard
        fields = [
            'total',
            'paid',
            'due',
            'newTotal',
            'discountAmount',
            'vendorsalecardID',
            'vendorUserID',
            'workshopID',
        ]

    def update(self,instance, validated_data):
        paid = validated_data.get('paid')
        discountAmount = validated_data.get('discountAmount')
        vensalecardID = instance.vendorsalecardID
        obj = VendorSaleCard.objects.get(vendorsalecardID = vensalecardID)
        obj.discountAmount = discountAmount
        obj.newTotal = obj.total - discountAmount
        obj.paid = obj.paid + paid
        obj.due = obj.newTotal - obj.paid
        obj.save()
        
        user_obj = Accounting.objects.filter(userID=obj.userID).order_by('createdAt')[::-1]
        
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
            refID=vensalecardID
        )
        
        workshopID = validated_data.get('workshopID')
        balance_workshop = Accounting.objects.filter(userID=workshopID.userID).order_by('createdAt')[::-1]
        serializer_workshop = EntryBalanceSerializer(balance_workshop, many=True) 
        if balance_workshop:
            balance_workshop = serializer_workshop.data[0]["balance"]
            balance_workshop = balance_workshop + paid
        else:
            balance_workshop = paid
        obj__ = Accounting.objects.create(
            debitAmount = paid,
            balance = balance_workshop,
            userID=workshopID.userID,
            workshopUserID=vendorUserID,
            description="Buy parts from vendor.",
            refType="VendorSaleCard",
            refID=vensalecardID
        )
            
        return obj

class VendorSaleCardDeliveredSerializer(ModelSerializer):
    class Meta:
        model = VendorSaleCard
        fields = [
              'vendorsalecardID',
            'delivered',
        ]

class VendorSaleCardUpdeateSerializer(ModelSerializer):

    class Meta:
        model = VendorPartSale
        fields = [
            'partID',
            'partQty',
            # 'vendorsalecardID',
        ]
        
    def update(self, instance, validated_data):
        salecardID = validated_data.get('vendorsalecardID')
        partqty = validated_data.get('partQty')
        partID = validated_data.get('partID')
        partSaleID = validated_data.get('partSaleID')
        partID = partID.partID
        # vendorsalecardID = instance.vendorsalecardID

        partsale_obj = VendorPartSale.objects.get(partSaleID=partSaleID.partSaleID, partID = partID)

        oldqty = partsale_obj.partQty
        oldprice = partsale_obj.partPrice
        oldtotal = oldqty*oldprice
        partsale_obj.partQty = partqty
        partsale_obj.save()


        partprice = partsale_obj.partPrice
        salecard_obj = VendorSaleCard.objects.get(vendorsalecardID = salecardID.vendorsalecardID)
        cardtotal = salecard_obj.total
        newtotal = (cardtotal - oldtotal) + (partprice*partqty)
        salecard_obj.total = newtotal
        salecard_obj.save()

        return partsale_obj
