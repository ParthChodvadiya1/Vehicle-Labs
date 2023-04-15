from datetime import timedelta, datetime
from django.utils import timezone

from rest_framework_jwt.settings import api_settings
from rest_framework import serializers

from src.apis.accounts.models import UserDetail, SubscriptionRecord, SubscriptionType
from src.apis.media.api.serializers import MediaSerializer, MediaDetailSerializer
from src.apis.media.models import MediaDetails
from src.apis.customer.models import CustomerDetail
from src.apis.rolepermission.models import Permissions
from src.utils.main import JWT_AUTH

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expire_delta = JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


class UserDetailSerializer(serializers.ModelSerializer):
    media = MediaSerializer(read_only=True)

    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'isActivated',
            'utype',
            'username',
            'email',
            'userphone',
            'useraddress',
            'media',
            'token',
            'latitude',
            'longitude',
            'createdAt',
            'updatedAt',
            'expiredAt'
        ]

class UserAccountingSerializer(serializers.ModelSerializer):
    media = MediaSerializer(read_only=True)

    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'isActivated',
            'utype',
            'username',
            'email',
            'userphone',
            'useraddress',
            'media',
            'latitude',
            'longitude',
            'createdAt',
            'updatedAt',
            'expiredAt'
        ]


class UserWorkshopManagerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'isActivated',
            'utype',
            'username',
            'email',
            'userphone',
            'useraddress',
            'token',
            'latitude',
            'longitude',
            'password',
            'createdAt',
            'updatedAt',
            'expiredAt'
        ]


class UserDetailByUserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [
            'token',
        ]


class SubscriptionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionRecord
        fields = [
            'amount',
            'userID',
            'timePeriod',
            'paymentID',
            'subscriptionID',
            'createdAt',
        ]

    def create(self, validated_data):
        userid = validated_data.get("userID")
        user = UserDetail.objects.get(userID=userid.userID)
        oldExpiry = user.expiredAt
        newExpiry = oldExpiry + \
            timedelta(days=validated_data.get("timePeriod"))
        user.expiredAt = newExpiry
        user.save()

        sub_obj = SubscriptionRecord.objects.create(
            amount=validated_data.get("amount"),
            userID=validated_data.get("userID"),
            timePeriod=validated_data.get("timePeriod"),
            paymentID=validated_data.get("paymentID"),
        )
        return sub_obj


class SubscriptionRecordDetailSerializer(serializers.ModelSerializer):
    userID = UserDetailSerializer(read_only=True)

    class Meta:
        model = SubscriptionRecord
        fields = [
            'userID',
            'razor_res',
            'amount',
            'timePeriod',
            'paymentID',
            'subscriptionID',
            'createdAt',
        ]


class SubscriptionTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = [
            'subTypeID',
            'amount',
            'timePeriod',
            'description',
            'subName',
        ]


class SubscriptionCapturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionRecord
        fields = [
            'subscriptionID',
            'amount',
            'paymentID',
        ]


class UserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'userphone',
            'password',
            'createdAt',
            'updatedAt',
            'expiredAt'
        ]


class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'utype',
            'username',
            'email',
            'userphone',
            'useraddress',
            'latitude',
            'longitude',
            'password',
            'password2',
            'token',
            'expires',
            'message',
            'createdAt',
            'updatedAt',
            'expiredAt'

        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate_email(self, value):
        qs = UserDetail.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this email already exists")
        return value

    def validate_userphone(self, value):
        qs = UserDetail.objects.filter(userphone__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this userphone already exists")
        return value

    def validate_username(self, value):
        qs = UserDetail.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this username already exists")
        return value

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = UserDetail(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            userphone=validated_data.get('userphone'),
            useraddress=validated_data.get('useraddress'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.isActivated = True
        user_obj.save()
        if validated_data.get('utype') == "Customer":
            cus_obj = CustomerDetail(
                cusname=validated_data.get('username'),
                cusemail=validated_data.get('email'),
                cusphone=validated_data.get('userphone'),
                cusaddress=validated_data.get('useraddress'),
                latitude=validated_data.get('latitude'),
                longitude=validated_data.get('longitude'),
                userID=user_obj
            )
            cus_obj.save()
        return user_obj


class UserUpdateSertializer(serializers.ModelSerializer):

    media = MediaDetailSerializer(required=False)

    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'username',
            'useraddress',
            'media',
        ]
        extra_kwargs = {
            'username': {'validators': []},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.useraddress = validated_data.get(
            'useraddress', instance.useraddress)

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
                    mediaType=media['mediaType'],
                    mediaURL=media['mediaURL']
                )

            user_obj = UserDetail.objects.get(
                userID=instance.userID
            )
            user_obj.media = media_obj
            user_obj.save()

        user_obj = UserDetail.objects.get(
            userID=instance.userID
        )

        return user_obj


class UserSubscriptionUpdateSertializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'expiredAt'

        ]


class SubUserSubscriptionUpdateSertializer(serializers.ModelSerializer):

    class Meta:
        model = Permissions
        fields = [
            'permID',
        ]
