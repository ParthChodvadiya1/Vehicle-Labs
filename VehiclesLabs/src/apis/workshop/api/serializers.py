from rest_framework.serializers import ModelSerializer
from src.apis.workshop.models import WorkshopDetail, WorkShopManager
from src.apis.media.models import MediaDetails
from src.apis.media.api.serializers import MediaSerializer
from src.apis.accounts.api.serializers import UserDetailSerializer,UserWorkshopManagerDetailSerializer

from src.apis.accounts.models import UserDetail
class WorkshopSerializer(ModelSerializer):
    class Meta:
        model = WorkshopDetail
        fields = [
            'workshopID',
            'workshopname',
            'workshopemail',
            'workshopphone',
            'workshopaddress',
            'expectedDay',
            'gst_per',
            'gst_no',
            'invoice_title',
            'logo',
            'userID',
            'createdAt',
            'updatedAt',
            'latitude',
            'longitude',
        ]

    def create(self, validated_data):
        workshop_obj = WorkshopDetail.objects.create(
            workshopname=validated_data.get('workshopname'),
            workshopemail=validated_data.get('workshopemail'),
            workshopphone=validated_data.get('workshopphone'),
            workshopaddress=validated_data.get('workshopaddress'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            logo=validated_data.get('logo'),
            userID=validated_data.get('userID'),
        )
        
        return workshop_obj


class WorkshopListSerializer(ModelSerializer):
    media = MediaSerializer(read_only=True)
    class Meta:
        model = WorkshopDetail
        fields = [
            'workshopID',
            'workshopname',
            'workshopemail',
            'workshopphone',
            'workshopaddress',
            'logo',
            'expectedDay',
            'gst_per',
            'gst_no',
            'invoice_title',
            'media',
            'userID',
            'createdAt',
            'updatedAt',
            'latitude',
            'longitude',
        ]

class WorkshopManagerSerilizer(ModelSerializer):
    userID  = UserDetailSerializer(read_only=True)
    usermanageID  = UserDetailSerializer(read_only=True)
    workshopID = WorkshopListSerializer(read_only=True)
    class Meta:
        model = WorkShopManager
        fields = [
            'workshopmanageID',
            'workshopID',
            'userID',
            'usermanageID',
        ]

class WorkshopDetailSerializer(ModelSerializer):
    class Meta:
        model = WorkshopDetail
        fields = '__all__'

class WorkshopUpdateSerializer(ModelSerializer):
    media = MediaSerializer(required=False)
    class Meta:
        model = WorkshopDetail
        fields = [
            'workshopID',
            'workshopname',
            'workshopaddress',
            'logo',
            'expectedDay',
            'gst_per',
            'gst_no',
            'invoice_title',
            'media',
            'userID',
            'latitude',
            'longitude',
        ]
    def update(self, instance, validated_data):

        instance.workshopname = validated_data.get('workshopname', instance.workshopname)
        instance.workshopaddress = validated_data.get('workshopaddress', instance.workshopaddress)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.expectedDay = validated_data.get('expectedDay', instance.expectedDay)
        instance.gst_per = validated_data.get('gst_per', instance.gst_per)
        instance.gst_no = validated_data.get('gst_no', instance.gst_no)
        instance.invoice_title = validated_data.get('invoice_title', instance.invoice_title)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()

        media = validated_data.get('media')
        if media:
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

            workshop_obj = WorkshopDetail.objects.get(
                workshopID = instance.workshopID
            )

            workshop_obj.media=media_obj
            workshop_obj.save()
        workshop_obj = WorkshopDetail.objects.get(
            workshopID = instance.workshopID
        )
        return workshop_obj

class WorkshopManageSerializer(ModelSerializer):
    # media = MediaSerializer(read_only=True)
    class Meta:
        model = WorkshopDetail
        fields = [
            'workshopname',
            'workshopemail',
            'workshopphone',
            'workshopaddress',
            'latitude',
            'longitude'
        ]

class WorkshopMangerRegisterSerializer(ModelSerializer):
    workshop = WorkshopManageSerializer(required = False)
    user_workshop = UserWorkshopManagerDetailSerializer(required = False)
    class Meta:
        model = WorkShopManager
        fields = [
            'workshopmanageID',
            'workshop',
            'user_workshop',
            'usermanageID'
        ]

    def create(self, validated_data):
        workshop = validated_data.pop('workshop')
        user_data = validated_data.pop('user_workshop')

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
        workshop_obj = WorkshopDetail.objects.create(
            workshopname = workshop['workshopname'],
            workshopemail = workshop['workshopemail'],
            workshopaddress = workshop['workshopaddress'],
            workshopphone = workshop['workshopphone'],
            latitude = workshop['latitude'],
            longitude = workshop['longitude'],
            userID = user_obj
        )
        workshopmanager_obj = WorkShopManager.objects.create(
            workshopID=workshop_obj,
            userID=user_obj,
            usermanageID=validated_data.get('usermanageID')
        )
        return workshopmanager_obj
        