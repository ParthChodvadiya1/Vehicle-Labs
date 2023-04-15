from src.apis.accounting_software.api.serializers import EntryBalanceSerializer
from rest_framework import serializers

from src.apis.customer.models import CustomerDetail
from src.apis.accounting_software.models import Accounting
from src.apis.accounts.models import UserDetail
from src.apis.customer.api.serializers import CustomerSerializer
from src.apis.vehicles.api.serializers import VehiclesSerializer
from src.apis.fueltype.api.serializers import FuelTypeSerializer
from src.apis.vehiclebrands.api.serializers import VehicleBrandSerializer
from src.apis.vehicles.models import VehiclesDetail
from src.apis.jobcards.models import JobCardDetail, JobcardServices, JobcardParts, JobCardImage, WorkshopCustomer
from src.apis.services.api.serializers import ServiceSerializer
from src.apis.services.models import ServiceDetails
from src.apis.services.api.serializers import ServiceSerializer
from src.apis.workshopinventory.models import WorkshopInventory
from src.apis.workshopinventory.api.serializers import WorkshopInventoryDetailSerializer
import re

class JobCardSerializer(serializers.ModelSerializer):
    cusID       = CustomerSerializer(read_only=True)
    vehicleID   = VehiclesSerializer(read_only=True)
    fueltypeID  = FuelTypeSerializer(read_only=True)
    brandID     = VehicleBrandSerializer(read_only=True)
    
    class Meta:
        model = JobCardDetail
        fields = [
            'userID',
            'jobID',
            'expectedAt',
            'deliveredAt',
            'totalServiceAmount',
            'totalPartsAmount',
            'total',
            'paid',
            'due',
            'isCompleted',
            'brandID',
            'fueltypeID',
            'vehicleID',
            'cusID',
            'createdAt',
            'updatedAt',
            'newTotal',
            'discountAmount',
        ]

class JobCardDetailSerializer(serializers.Serializer):

    class Meta:
        model = JobCardDetail
        fields = [
            'userID',
            'jobID',
            'totalServiceAmount',
            'totalPartsAmount',
            'brandID',
            'fueltypeID',
            'vehicleID',
            'cusID',
            'createdAt',
            'updatedAt',
            'newTotal',
            'discountAmount',
        ]
        fields = '__all__'

class JobCardPaymentSerializer(serializers.ModelSerializer):
    workshopUserID = serializers.CharField(required=False)
    class Meta:
        model = JobCardDetail
        fields = [
            'jobID',
            'paid',
            'discountAmount',
            'newTotal',
            'workshopUserID'
        ]
    def update(self, instance, validated_data):
        paid = validated_data.get('paid')
        discountAmount = validated_data.get('discountAmount')
        jobID = instance.jobID
        obj = JobCardDetail.objects.get(jobID=jobID)
        obj.discountAmount = discountAmount
        obj.newTotal = obj.total - discountAmount
        obj.paid = obj.paid + paid
        obj.due = obj.newTotal - obj.paid
        obj.save()
        user_obj = Accounting.objects.filter(userID=obj.userID).order_by('-createdAt')[::-1]
        workshopUserID = validated_data.get('workshopUserID')
        workshopUserID = UserDetail.objects.get(userID=workshopUserID)
        serializer = EntryBalanceSerializer(user_obj, many=True)
        if user_obj:
            balance = serializer.data[0]["balance"]
            balance = balance + paid
        else:
            balance = paid
            
        
        obj = Accounting.objects.create(
            creditAmount = paid,
            balance = balance,
            userID=obj.userID,
            workshopUserID=workshopUserID,
            description="Jobcard Payment captured.",
            refType="Jobcard",
            refID=jobID
        )
        return instance

class JobCardCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCardDetail
        fields = [
            'jobID',
            'isCompleted'
        ]

class JobCardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCardImage
        fields = ('image',)

class JobCardRegisterSerializer(serializers.ModelSerializer):

    vehicles = VehiclesSerializer(required=False)
    customer = CustomerSerializer(required=False)
    images = JobCardImageSerializer(many=True, read_only=True)
    class Meta:
        model = JobCardDetail
        fields = [
            'brandID',
            'fueltypeID',
            'expectedAt',
            'deliveredAt',
            'vehicles',
            'images',
            'customer',
            'userID',
        ]
    def create(self, validated_data):

        vehiclesdata = validated_data.pop('vehicles')
        vehicles_obj = VehiclesDetail.objects.update_or_create(
            vehiclenumber=vehiclesdata['vehiclenumber'],
            kilometer=vehiclesdata['kilometer'],
            chasisnumber=vehiclesdata['chasisnumber'],
            enginenumber=vehiclesdata['enginenumber'],
            fuelIndicator=vehiclesdata['fuelIndicator'],
        )
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
                userID=validated_data.get('userID')
            )            
        customer_obj.save()
        job_obj = JobCardDetail.objects.create(
            brandID=validated_data.get("brandID"),
            fueltypeID=validated_data.get("fueltypeID"),
            expectedAt=validated_data.get("expectedAt"),
            deliveredAt=validated_data.get("deliveredAt"),
            vehicleID=vehicles_obj[0],
            cusID=customer_obj,
            userID=validated_data.get("userID")
        )
        try:
            workshop_customer = WorkshopCustomer.objects.get(cusID = customer_obj,userID=validated_data.get("userID"))
        except:
            workshop_customer = WorkshopCustomer.objects.create(
                cusID = customer_obj,
                userID=validated_data.get("userID")
            )
        images_data = self.context.get('view').request.FILES
        for image_data in images_data.values():
            JobCardImage.objects.create(task=job_obj,  image=image_data)
        return job_obj
        
class JobCardUpdateSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False)
    vehicles = VehiclesSerializer(required=False)

    class Meta:
        model = JobCardDetail
        fields = [
            'jobID',
            'brandID',
            'fueltypeID',
            'expectedAt',
            'deliveredAt',
            'vehicles',
            'customer',
        ]
        
    def update(self, instance, validated_data):
        instance.brandID = validated_data.get('brandID', instance.brandID)
        instance.fueltypeID = validated_data.get('fueltypeID', instance.fueltypeID)
        instance.expectedAt = validated_data.get('expectedAt', instance.expectedAt)
        instance.deliveredAt = validated_data.get('deliveredAt', instance.deliveredAt)
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
                customer_obj.remraks = customers['remarks']
                customer_obj.cussignature = customers['cussignature']
                customer_obj.save()
        vehicles = validated_data.get('vehicles')
        for vehicle in vehicles:
            veh_id = vehicles["vehicleID"]
            if veh_id:
                vehicle_obj =  VehiclesDetail.objects.get(vehicleID=veh_id)
                vehicle_obj.vehiclenumber = vehicles['vehiclenumber']
                vehicle_obj.kilometer = vehicles['kilometer']
                vehicle_obj.chasisnumber = vehicles['chasisnumber']
                vehicle_obj.enginenumber = vehicles['enginenumber']
                vehicle_obj.fuelIndicator = vehicles['fuelIndicator']
                vehicle_obj.save()
        return instance

class JobcardServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobcardServices
        fields = [
            'jobcardServidesID',
            'jobID',
            'services',
            'servicePrices',
        ]
   
        
    def create(self, validated_data):
        service = validated_data.get("services")
        serviceprice = validated_data.get("servicePrices")
        temp = re.split(',',service)
        temp2 = re.split(',',serviceprice)  
        nums = list(map(int, temp2))
        update_total = sum(nums) 
        
        obj = validated_data.get("jobID")
        intital_total = obj.totalServiceAmount        
        obj.totalServiceAmount = update_total + intital_total
        totalPartsAmount = obj.totalPartsAmount
        total = update_total + intital_total + totalPartsAmount
        obj.total = total
        obj.newTotal = total - obj.discountAmount
        obj.due = total - obj.paid
        obj.save()
        loop=0
        for serviceID in temp:
            JobcardServices.objects.update_or_create(
            jobID=validated_data.get("jobID"),
            servicePrice=temp2[loop],
            serviceID=ServiceDetails.objects.get(serviceID=serviceID),            
            )

            loop += 1
        
        return validated_data
      
class JobcardServicesDetailSerializer(serializers.ModelSerializer):
    serviceID = ServiceSerializer(read_only=True)
    
    class Meta:
        model = JobcardServices
        fields = [
            'jobcardServidesID',
            'jobID',
            'serviceID',
            'servicePrice',
        ]

class JobcardPartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobcardParts
        fields = [
            'jobcardPartsID',
            'jobID',
            'workshopInventoryIDs',
            'partsPrices',
            'partQtys'
        ]
   
        
    def create(self, validated_data):
        workshopInventoryIDs = validated_data.get("workshopInventoryIDs")
        partsPrices = validated_data.get("partsPrices")
        partQtys = validated_data.get("partQtys")
        temp = re.split(',',workshopInventoryIDs)
        temp2 = re.split(',',partsPrices)
        temp3 = re.split(',',partQtys)
        qty = list(map(int,temp3))
        nums = list(map(float, temp2))
        update_total = sum([a*b for a,b in zip(qty,nums)]) 
        
        obj = validated_data.get("jobID")

        intital_total = obj.totalPartsAmount        
        obj.totalPartsAmount = update_total + intital_total
        totalServicesAmount = obj.totalServiceAmount
        total = update_total + intital_total + totalServicesAmount

        obj.total = total
        obj.newTotal = total - obj.discountAmount
        obj.due = total - obj.paid
        obj.save()

        loop=0

        for workshopInventoryID in temp:

            partQtys = temp3[loop]
            workshopPartQTY = int(partQtys)
            workshopPartQty = validated_data.get("workshopPartQTY")
            
            workshopInventoryID = WorkshopInventory.objects.get(workshopInventoryID = workshopInventoryID)

            oldQty = workshopInventoryID.workshopPartQty
            finalWSPartQty = oldQty - workshopPartQTY

            workshopInventoryID.workshopPartQty = finalWSPartQty 
            workshopInventoryID.save()


            JobcardParts.objects.update_or_create(
            jobID=validated_data.get("jobID"),
            workshopInventoryID = WorkshopInventory.objects.get(workshopInventoryID=temp[loop]),
            partsPrice = temp2[loop],
            partQty = temp3[loop],
            )
            loop += 1
        
        return validated_data
        
class JobcardPartsDetailSerializer(serializers.ModelSerializer):
    workshopInventoryID = WorkshopInventoryDetailSerializer(read_only=True)
    class Meta:
        model = JobcardParts
        fields = [
            'jobcardPartsID',
            'jobID',
            'workshopInventoryID',
            'partsPrice',
            'partQty',
        ]

class WorkshopCustomerbyUserIDSerializer(serializers.ModelSerializer):
    cusID       = CustomerSerializer(read_only=True)
    
    class Meta:
        model = WorkshopCustomer
        fields = [
            'userID',
            'cusID',
            'createdAt',
            'updatedAt',
        ]
