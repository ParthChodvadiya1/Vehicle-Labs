from rest_framework import serializers
from src.apis.vehiclebrands.models import VehicleBrand
            
import openpyxl
class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = [
            'brandID',
            'brandname',
            'brandmodel',
            'createdAt',
            'updatedAt',
        ]


class BrandSheetUploadSerializer(serializers.ModelSerializer):
    resp_dict = serializers.DictField(required=False)
    class Meta:
        model = VehicleBrand
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
            unuploaded_brand = [ ]
            uploaded_brand = [ ]
            for (i,brand) in enumerate(worksheet.iter_rows()):
                if(i==0):
                    brandHeader = [data.value for data in brand]
                else:
                    brand = {brandHeader[i] : data.value for (i,data) in enumerate(brand)}
                    bname = brand["brandname"]
                    bmodel = brand["brandmodel"]
                    try:
                        existBrand = VehicleBrand.objects.get(brandmane=bname, brandmodel=bmodel,)
                        if existBrand:
                            unuploaded_brand = list(unuploaded_brand)
                            unuploaded_brand.append(brand)
                    except:
                            brand_obj = VehicleBrand.objects.create(
                                brandname=brand["brandname"],
                                brandmodel = brand["brandmodel"],
                            )
                            uploaded_brand = list(uploaded_brand)
                            uploaded_brand.append(brand)
                            brand_obj.save()
            resp_dict={"unuploaded_brand": unuploaded_brand, "uploaded_brand":uploaded_brand}
            validated_data['resp_dict'] = resp_dict
            return validated_data
        else:
            raise serializers.ValidationError("unsupported file")



















