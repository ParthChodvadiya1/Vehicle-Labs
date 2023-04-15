from rest_framework import serializers
# from VehiclesLabs.src.apis.services.models import ServiceDetails

from src.apis.jobcards.models import WorkshopCustomer
from src.apis.customer.models import CustomerDetail
from src.apis.countersale.models import CounterSale, MinorServices
from src.apis.customer.api.serializers import CustomerDetailSerailizer, CustomerSerializer, CustomerSerializerCounter
from src.apis.accounting_software.api.serializers import EntryBalanceSerializer
from src.apis.accounting_software.models import Accounting
from src.apis.accounts.models import UserDetail
from src.apis.services.models import ServiceDetails


class CounterSaleSerializer(serializers.ModelSerializer):
    cusID = CustomerDetailSerailizer(required=False)

    class Meta:
        model = CounterSale
        fields = [
            'countersaleID',
            'cusID',
            'userID',
            'workshopID',
            'vehiclenumber',
            'servicename',
            'serviceprice',
            'paid',
            'due',
            'isCompleted',
            'createdAt',
            'updatedAt',
        ]


class CounterSaleDateSerializer(serializers.ModelSerializer):
    start_date = serializers.CharField(write_only=True)
    end_date = serializers.CharField(write_only=True)

    class Meta:
        model = CounterSale
        fields = [
            'start_date',
            'end_date',
        ]


class CounterSaleCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterSale
        fields = [
            'countersaleID',
            'isCompleted'
        ]


class CounterSalePaymentSerializer(serializers.ModelSerializer):
    counterUserID = serializers.CharField(required=False)

    class Meta:
        model = CounterSale
        fields = [
            'countersaleID',
            'paid',
            'due',
            'counterUserID'
        ]

    def update(self, instance, validated_data):
        instance.paid = validated_data.get(
            'paid', instance.paid)
        instance.due = validated_data.get(
            'due', instance.due)
        instance.save()
        paid = instance.paid
        countersaleID = instance.countersaleID
        counter_obj = CounterSale.objects.get(countersaleID=countersaleID)
        user_obj = Accounting.objects.filter(
            userID=counter_obj.userID).order_by('-createdAt')[::-1]
        counterUserID = validated_data.get('counterUserID')
        workshopUserID = UserDetail.objects.get(userID=counterUserID)
        serializer = EntryBalanceSerializer(user_obj, many=True)
        if user_obj:
            balance = serializer.data[0]["balance"]
            balance = balance + paid
        else:
            balance = paid

        obj = Accounting.objects.create(
            creditAmount=paid,
            balance=balance,
            userID=counter_obj.userID,
            workshopUserID=workshopUserID,
            description="CounterSale Payment captured.",
            refType="CounterSale",
            refID=countersaleID
        )

        return instance


class CounterSaleRegisterSerializer(serializers.ModelSerializer):

    customer = CustomerSerializerCounter(required=False)

    class Meta:
        model = CounterSale
        fields = [
            'customer',
            'userID',
            'workshopID',
            'vehiclenumber',
            'servicename',
            'serviceprice',
            'userID',
            'workshopID',
        ]

    def create(self, validated_data):

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
                userID=validated_data.pop('userID')
            )
            customer_obj.save()

        try:
            workshop_customer = WorkshopCustomer.objects.get(
                cusID=customer_obj, userID=validated_data.get('userID'))
        except:
            workshop_customer = WorkshopCustomer.objects.create(
                cusID=customer_obj, 
                userID=validated_data.get('userID')
            )
            workshop_customer.save()

        cs_object = CounterSale.objects.create(
            cusID=customer_obj,
            userID=validated_data.get('userID'),
            workshopID=validated_data.get('workshopID'),
            vehiclenumber=validated_data.get('vehiclenumber'),
            servicename=validated_data.get('servicename'),
            serviceprice=validated_data.get('serviceprice')
        )
        cs_object.save()
        return validated_data


class CounterSaleUpdateSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)

    class Meta:
        model = CounterSale
        fields = [
            'customer',
            'vehiclenumber',
            'servicename',
            'serviceprice',
        ]

    def update(self, instance, validated_data):

        instance.vehiclenumber = validated_data.get(
            'vehiclenumber', instance.vehiclenumber)
        instance.servicename = validated_data.get(
            'servicename', instance.servicename)
        instance.serviceprice = validated_data.get(
            'serviceprice', instance.serviceprice)
        instance.save() 

        customers = validated_data.get('customer')
    
        for customer in customers:
            cus_id = customers["cusID"]
            if cus_id:
                customer_obj = CustomerDetail.objects.get(cusID=cus_id)
                customer_obj.cusname = customers['cusname']
                customer_obj.cusemail = customers['cusemail']
                customer_obj.cusphone = customers['cusphone']
                customer_obj.cusaddress = customers['cusaddress']
                customer_obj.save()
        return instance


class MinorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinorServices
        fields = [
            'mserviceName',
            'mservicePrice',
        ]


class MinorServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinorServices
        fields = [
            'mserviceName',
            'mservicePrice',
            'createdAt',
            'updatedAt',
        ]
