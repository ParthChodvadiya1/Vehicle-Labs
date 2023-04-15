from rest_framework import serializers
from src.apis.media.models import MediaDetails
from src.apis.accounts.models import UserDetail
from src.apis.vendors.models import VendorDetail,VendorManager
from src.apis.media.api.serializers import MediaDetailSerializer
from src.apis.accounts.api.serializers import UserDetailSerializer,UserWorkshopManagerDetailSerializer

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = [
            'vendorID',
            'vendorname',
            'vendoremail',
            'vendorphone',
            'vendoraddress',
            'expectedDay',
            'gst_per',
            'gst_no',
            'invoice_title',
            'logo',
            'media',
            'userID',
            'createdAt',
            'updatedAt',
            'latitude',
            'longitude',
        ]
    def create(self, validated_data):
        vendor_obj = VendorDetail.objects.create(
            vendorname=validated_data.get('vendorname'),
            vendoremail=validated_data.get('vendoremail'),
            vendorphone=validated_data.get('vendorphone'),
            vendoraddress=validated_data.get('vendoraddress'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            logo=validated_data.get('logo'),
        )
        return vendor_obj

class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = '__all__'


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = '__all__'


class VendorUpdateSerializer(serializers.ModelSerializer):
    media = MediaDetailSerializer(required = False)  
    class Meta:
        model = VendorDetail
        fields = [
            'vendorID',
            'vendorname',
            'vendoraddress',
            'logo',
            'media',
            'expectedDay',
            'gst_per',
            'gst_no',
            'invoice_title',
            'userID',
            'latitude',
            'longitude',
        ]


    def update(self, instance, validated_data):

        instance.vendorname = validated_data.get('vendorname', instance.vendorname)
        instance.vendoraddress = validated_data.get('vendoraddress', instance.vendoraddress)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.expectedDay = validated_data.get('expectedDay', instance.expectedDay)
        instance.gst_per = validated_data.get('gst_per', instance.gst_per)
        instance.gst_no = validated_data.get('gst_no', instance.gst_no)
        instance.invoice_title = validated_data.get('invoice_title', instance.invoice_title)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()

        media = validated_data.get('media')

        if "mediaID" in media.keys():
            media_obj = MediaDetails.objects.get(
                mediaID=media["mediaID"]
                )
            media_obj.mediaType = media['mediaType']
            media_obj.mediaURL = media['mediaURL']
            media_obj.save()
        else:
            media_obj = MediaDetails.objects.create(
                mediaType = media['mediaType'],
                mediaURL = media['mediaURL']
                )

        vendor_obj = VendorDetail.objects.get(
            vendorID = instance.vendorID
        )
        vendor_obj.media=media_obj
        vendor_obj.save()

        return vendor_obj

class VendorManagerSerilizer(serializers.ModelSerializer):
    userID  = UserDetailSerializer(read_only=True)
    usermanageID  = UserDetailSerializer(read_only=True)
    vendorID = VendorListSerializer(read_only=True)
    class Meta:
        model = VendorManager
        fields = [
            'vendormanageID',
            'userID',
            'usermanageID',
            'vendorID',
        ]


class VendorManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        fields = [
            'vendorname',
            'vendoremail',
            'vendorphone',
            'vendoraddress',
            'latitude',
            'longitude'
        ]

class VendorMangerRegisterSerializer(serializers.ModelSerializer):
    vendor = VendorManageSerializer(required = False)
    user_vendor = UserWorkshopManagerDetailSerializer(required = False)
    class Meta:
        model = VendorManager
        fields = [
            'vendormanageID',
            'vendor',
            'user_vendor',
            'usermanageID'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user_vendor')
        vendor = validated_data.pop('vendor')

        user_obj = UserDetail.objects.create(
            utype = user_data['utype'],
            username = user_data['username'],
            email = user_data['email'],
            userphone = user_data['userphone'],
            useraddress = user_data['useraddress'],
            latitude = user_data['latitude'],
            longitude = user_data['longitude']
        )
        user_obj.set_password(user_data['password'])
        user_obj.save()

        vendor_obj = VendorDetail.objects.create(
            vendorname = vendor['vendorname'],
            vendoremail = vendor['vendoremail'],
            vendorphone = vendor['vendorphone'],
            vendoraddress = vendor['vendoraddress'],
            latitude = vendor['latitude'],
            longitude = vendor['longitude'],
            userID = user_obj
        )
        
        vendormanager_obj = VendorManager.objects.create(
            vendorID=vendor_obj,
            userID=user_obj,
            usermanageID=validated_data.get('usermanageID')
        )
        return vendormanager_obj

