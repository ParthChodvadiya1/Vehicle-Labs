from rest_framework import serializers
from src.apis.vendorinventory.models import VendorInventory
from src.apis.parts.api.serializers import PartSerializer , PartNTSerializer
from src.apis.vendors.api.serializers import VendorSerializer 
from src.apis.parts.models import PartDetails, RequestedParts
import io 
import csv
import re


class VendorInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorInventory
        fields = [
            'vendorInventoryID',
            'partID',
            'vendorPartQty',
            'vendorPartPrice',
            'vendorID',
            'createdAt',
            'updatedAt',
        ]
    def create(self, validated_data):
        vendorPart_obj = VendorInventory.objects.create(
            partID=validated_data.get('partID'),
            vendorPartQty=validated_data.get("vendorPartQty"),
            vendorPartPrice=validated_data.get("vendorPartPrice"),
            vendorID=validated_data.get("vendorID")     
        )
        return vendorPart_obj

    def update_vendorPartQty(self):
        workshopPartQty = self.workshopinventory.workshopPartQty
        vendorPartQty = self.vendorinventory.vendorPartQty
        new_vendorPartQty = vendorPartQty - workshopPartQty
        self.vendorPartQty = new_vendorPartQty
        self.save()
        return vendorPartQty

class VendorInventoryDetailSerializer(serializers.ModelSerializer):
    vendorID = VendorSerializer(read_only=True)
    partID = PartSerializer(read_only = True)

    class Meta:    
        model = VendorInventory
        fields = [
            'vendorInventoryID',
            'vendorPartQty',
            'vendorPartPrice',
            'partID',
            'vendorID',
            'createdAt',
            'updatedAt',    
        ]

class VendorInventoryUpdateSerializer(serializers.ModelSerializer):
    # vendorID = VendorSerializer(read_only=True)
    # partID = PartSerializer(read_only = True)
    class Meta:    
        model = VendorInventory
        fields = [
            'vendorInventoryID',
            'vendorPartQty',
            'vendorPartPrice'   
        ]

class VendorPartsSerializer(serializers.ModelSerializer):
    resp_dict = serializers.DictField(required=False)

    class Meta:
        model = VendorInventory
        fields = [
            'excel_file',
            'vendorID',
            'resp_dict',
        ]

    def create(self,validated_data):
        import openpyxl
        excel_file = validated_data.get('excel_file')
        ext  = str(excel_file)

        if ext.endswith('.xls') | ext.endswith('.xlsx'):

            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb["Sheet1"]

            uploaded_part = [ ]
            reqested_part = [ ]

            for (i,part) in enumerate(worksheet.iter_rows()):
                if(i==0):
                    partHeader = [data.value for data in part]
                else:
                    part = {partHeader[i] : data.value for (i,data) in enumerate(part)}
                    pname = part["partName"]
                    pnumber = part["partNumber"]
                    cname = part["companyName"]
                    try:
                        existPart = PartDetails.objects.get(partName=pname, partNumber=pnumber,companyName=cname)
                        partID = existPart.partID

                        if existPart:
                            vendorinventory_obj = VendorInventory.objects.create(
                                partID=PartDetails.objects.get(partID = partID),
                                vendorPartQty=part['vendorPartQty'],
                                vendorPartPrice=part['vendorPartPrice'],
                                vendorID=validated_data.get('vendorID')
                            )
                            uploaded_part = list(uploaded_part)
                            uploaded_part.append(part)


                    except:

                            part_obj = RequestedParts.objects.create(
                                partName = part["partName"],
                                partType=part["partType"],
                                partPrice=part["partPrice"],
                                partNumber=part['partNumber'],
                                rackNumber=part['rackNumber'],
                                HSNNumber=part['HSNNumber'],
                                companyName=part['companyName'],
                                partNote=part['partNote'],
                                vendorPartQty=part['vendorPartQty'],
                                vendorPartPrice=part['vendorPartPrice'],
                                vehicleModel=part["vehicleModel"],
                                modelNumber=part["modelNumber"],
                                varient=part["varient"],
                                vendorID=validated_data.get('vendorID')  
                            )
                            reqested_part = list(reqested_part)
                            reqested_part.append(part)
                            part_obj.save()

            resp_dict={"uploaded_part": uploaded_part, "requested_part":reqested_part}
            validated_data['resp_dict'] = resp_dict

            return validated_data

        # elif ext.endswith('.csv'):
        #     data = excel_file.read().decode('UTF-8')
        #     io_string = io.StringIO(data)

        #     next(io_string)
        #     for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #         part_obj = PartDetails.objects.create(
        #             partName = column[0],
        #             partType=column[1],
        #             partNumber=column[2],
        #             rackNumber=column[3],
        #             HSNNumber=column[4],
        #             companyName=column[5],
        #             partPrice=column[8],
        #             partNote=column[9]
        #         )
        #         part_obj.save()
        #         VendorInventory.objects.create(
        #             partID=part_obj,
        #             vendorPartQty=column[6],
        #             vendorPartPrice=column[7],
        #             vendorID=validated_data.get('vendorID')     
        #         )
        #     return part_obj
        else:
            raise serializers.ValidationError("unsupported file")

    

class VendorInventoryPartQtySerializer(serializers.ModelSerializer):
    partID = PartNTSerializer(read_only = True)
    class Meta:
        model = VendorInventory
        fields = [
            'partID',
            'vendorPartQty',
        ]
