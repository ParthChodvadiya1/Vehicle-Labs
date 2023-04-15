from rest_framework import serializers
from src.apis.services.models import ServiceDetails

import openpyxl
class ServiceRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceDetails
        fields = [
            'serviceID',
            'serviceName',
            'serviceType',
            'servicePrice',
            'createdAt',
            'updatedAt',
        ]

    def create(self, validated_data):

        serviceName = validated_data.get('serviceName')
        servicePrice = validated_data.get('servicePrice')
        serviceType = validated_data.get('serviceType')  
        
        service_obj = ServiceDetails.objects.filter(
             serviceName=serviceName, isDeleted = False)
      
        if service_obj:
            raise Exception("Service with this name already exists")  
            
        else:            
            servObj = ServiceDetails.objects.create(
            serviceName=serviceName,
            servicePrice=servicePrice,
            serviceType=serviceType
            )
            servObj.save()
             

        return validated_data


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceDetails
        fields = [
            'serviceID',
            'serviceName',
            'serviceType',
            'servicePrice',
            'createdAt',
            'updatedAt',
            # 'userID'
        ]


class JobServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceDetails
        fields = [
            'serviceID',
            # 'serviceName',
            # 'serviceType',
            # 'servicePrice',
            # 'userID'
        ]

class serviceSheetUploadSerializer(serializers.ModelSerializer):
    resp_dict = serializers.DictField(required=False)
    class Meta:
        model = ServiceDetails
        fields = [
            'excel_file',
            'resp_dict',
        ]
    def create(self,validated_data):
        excel_file = validated_data.get('excel_file')
        ext  = str(excel_file)
        if ext.endswith('.xls') | ext.endswith('.xlsx'):
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb["Sheet1"]
            unuploaded_service = [ ]
            uploaded_service = [ ]
            for (i,service) in enumerate(worksheet.iter_rows()):
                if(i==0):
                    serviceHeader = [data.value for data in service]
                else:
                    service = {serviceHeader[i] : data.value for (i,data) in enumerate(service)}
                    sname = service["serviceName"]
                    stype = service["serviceType"]
                    sprice = service["servicePrice"]
                    try:
                        existservice = ServiceDetails.objects.get(serviceName=sname, serviceType=stype,servicePrice=sprice)
                        if existservice:
                            unuploaded_service = list(unuploaded_service)
                            unuploaded_service.append(service)
                    except:
                            service_obj = ServiceDetails.objects.create(
                                serviceName=service["serviceName"],
                                serviceType = service["serviceType"],
                                servicePrice=service["servicePrice"],
                            )
                            uploaded_service = list(uploaded_service)
                            uploaded_service.append(service)
                            service_obj.save()
            resp_dict={"unuploaded_service": unuploaded_service, "uploaded_service":uploaded_service}
            validated_data['resp_dict'] = resp_dict
            return validated_data
        else:
            raise serializers.ValidationError("unsupported file")