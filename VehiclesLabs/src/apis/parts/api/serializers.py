from rest_framework import serializers

from src.apis.parts.models import PartDetails, RequestedParts, PartImage, PartVideo
from src.apis.vendors.api.serializers import VendorDetailSerializer
from src.apis.vendorinventory.models import VendorInventory


class PartRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartDetails
        fields = [
            'partID',
            'partName',
            'partType',
            'partPrice',
            'partNumber',
            'HSNNumber',
            'companyName',
            'partNote',
            'partMedia',
            "vehicleModel",
            "varient",
            'createdAt',
            'updatedAt',
            "page",
            "refNo",
            "blockIndex",
            "localName"
        ]


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartDetails
        fields = [
            'partID',
            'partName',
            'partType',
            'partPrice',
            'partNumber',
            'HSNNumber',
            'companyName',
            'partMedia',
            "vehicleModel",
            "varient",
            'partNote',
            'createdAt',
            'updatedAt',
            "page",
            "refNo",
            "blockIndex",
            "localName"
        ]


class PartNTSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartDetails
        fields = [
            'partName',
            'partType',
            'partMedia',
        ]


class RequestedPartsDeliveredSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestedParts
        fields = [
            'isAdded',
        ]


class RequestedPartListSerializer(serializers.ModelSerializer):
    vendorID = VendorDetailSerializer(required=False)

    class Meta:
        model = RequestedParts
        fields = [
            'reqpartID',
            'partName',
            'partType',
            'partPrice',
            'partNumber',
            'rackNumber',
            'HSNNumber',
            'companyName',
            "vehicleModel",
            "varient",
            'partNote',
            'vendorPartQty',
            'vendorPartPrice',
            'partMedia',
            'vendorID',
            'createdAt',
            'updatedAt',
        ]


class RequestedPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedParts
        fields = [
            'reqpartID',
            'partName',
            'partType',
            'partPrice',
            'partNumber',
            'HSNNumber',
            'partMedia',
            "vehicleModel",
            "varient",
            'companyName',
            'partNote',
            'vendorPartQty',
            'vendorPartPrice',
            'vendorID',
            "page",
            "refNo",
            "blockIndex",
            "localName",
            'createdAt',
            'updatedAt',
        ]

    def create(self, validated_data):
        existPart = PartDetails.objects.filter(partName=validated_data.get(
            'partName'), partNumber=validated_data.get('partNumber'), companyName=validated_data.get('companyName'))
        if existPart:
            partID = existPart[0].partID
            part_obj = VendorInventory.objects.create(
                partID=PartDetails.objects.get(partID=partID),
                vendorPartQty=validated_data.get('vendorPartQty'),
                vendorPartPrice=validated_data.get('vendorPartPrice'),
                vendorID=validated_data.get('vendorID')
            )
        else:
            part_obj = RequestedParts.objects.create(
                partName=validated_data.get('partName'),
                partType=validated_data.get('partType'),
                partPrice=validated_data.get('partPrice'),
                partNumber=validated_data.get('partNumber'),
                HSNNumber=validated_data.get('HSNNumber'),
                partNote=validated_data.get('partNote'),
                companyName=validated_data.get('companyName'),
                vendorPartQty=validated_data.get('vendorPartQty'),
                vendorPartPrice=validated_data.get('vendorPartPrice'),
                vendorID=validated_data.get('vendorID'),
                partMedia=validated_data.get('partMedia'),
                vehicleModel = validated_data.get("vehicleModel"),
                varient = validated_data.get("varient"),
                page=validated_data.get("page"),
                refNo=validated_data.get("refNo"),
                blockIndex=validated_data.get("blockIndex"),
                localName=validated_data.get("localName"),
            )
        return part_obj


class ApprovePartAdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedParts
        fields = [
            'reqpartID',
            'partName',
            'partType',
            'partPrice',
            'partNumber',
            'HSNNumber',
            'companyName',
            'partMedia',
            "vehicleModel",
            "varient",
            'partNote',
            'vendorPartQty',
            'vendorPartPrice',
            'vendorID',
            "page",
            "refNo",
            "blockIndex",
            "localName"
        ]

    def create(self, validated_data):
        part_obj = PartDetails.objects.create(
            partName=validated_data.get('partName'),
            partType=validated_data.get('partType'),
            partPrice=validated_data.get('partPrice'),
            partNumber=validated_data.get('partNumber'),
            HSNNumber=validated_data.get('HSNNumber'),
            partNote=validated_data.get('partNote'),
            companyName=validated_data.get('companyName'),
            partMedia=validated_data.get('partMedia'),
            vehicleModel = validated_data.get("vehicleModel"),
            varient = validated_data.get("varient"),
            page=validated_data.get("page"),
            refNo=validated_data.get("refNo"),
            blockIndex=validated_data.get("blockIndex"),
            localName=validated_data.get("localName"),
        )

        vendorInventory_obj = VendorInventory.objects.create(
            vendorPartQty=validated_data.get('vendorPartQty'),
            vendorPartPrice=validated_data.get('vendorPartPrice'),
            vendorID=validated_data.get('vendorID'),
            partID=part_obj
        )

        return part_obj


class PartImageSerializer(serializers.ModelSerializer):
    images      = serializers.ListField(required=False)
    imagesNames = serializers.ListField(required=False)
    class Meta:
        model = PartImage
        fields = [
            'images',
            'imagesNames',
        ]
    def create(self, validated_data):
        images = validated_data.get('images')
        imagesNames = validated_data.get('imagesNames')

        for (image,imagesName) in zip(images,imagesNames):
            img_obj = PartImage.objects.create(
                partImgName= imagesName,
                partImage= image
            )
        return img_obj


class PartImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartImage
        fields = [
            'partImgID',
            'partImage',
            'partImgName',
            'createdAt',
            'updatedAt',
        ]


class PartVideoSerializer(serializers.ModelSerializer):
    videos      = serializers.ListField(required=False)
    videosNames = serializers.ListField(required=False)
    class Meta:
        model = PartVideo
        fields = [
            'videos',
            'videosNames',
        ]
    def create(self, validated_data):
        videos = validated_data.get('videos')
        videosNames = validated_data.get('videosNames')

        for (video,videosName) in zip(videos,videosNames):
            vid_obj = PartVideo.objects.create(
                partVidName= videosName,
                PartVideo= video
            )
        return vid_obj


class PartVideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartVideo
        fields = [
            'partVidID',
            'PartVideo',
            'partVidName',
            'createdAt',
            'updatedAt',
        ]

import re
class PartsSheetUploadSerializer(serializers.ModelSerializer):
    resp_dict = serializers.DictField(required=False)

    class Meta:
        model = VendorInventory
        fields = [
            'excel_file',
            'resp_dict',
        ]

    def create(self,validated_data):
        import openpyxl
        excel_file = validated_data.get('excel_file')
        ext  = str(excel_file)

        if ext.endswith('.xls') | ext.endswith('.xlsx'):

            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb["Sheet1"]
            unuploaded_part = [ ]
            uploaded_part = [ ]

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

                        if existPart:
                            unuploaded_part = list(unuploaded_part)
                            unuploaded_part.append(part)

                    except:
                            part_obj = PartDetails.objects.create(
                                partType=part["partType"], 
                                partName = part["partName"],
                                partPrice=part["partPrice"],
                                partNumber=part['partNumber'],
                                HSNNumber=part['HSNNumber'],
                                companyName=part['companyName'],
                                partNote=part['partNote'],
                                vehicleModel=part["vehicleModel"],
                                varient=part["varient"],
                                page=part["page"],
                                refNo=part["refNo"],
                                blockIndex=part["blockIndex"],
                                localName=part["localName"],
                                partMedia={
                                    "image": re.split(",", part['partImages']) if part['partImages'] else [],
                                    "video":  re.split(",", part['partVideos']) if part['partVideos'] else [],
                                }
                            )
                            uploaded_part = list(uploaded_part)
                            uploaded_part.append(part)
                            part_obj.save()

            resp_dict={"unuploaded_part": unuploaded_part, "uploaded_part":uploaded_part}
            validated_data['resp_dict'] = resp_dict

            return validated_data

        else:
            raise serializers.ValidationError("unsupported file")

