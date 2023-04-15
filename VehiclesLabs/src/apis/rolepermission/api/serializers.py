from rest_framework import serializers, fields

from src.apis.accounts.models import UserDetail
from src.apis.rolepermission.models import Permissions, Marketeer, DEMO_CHOICES
from src.apis.accounts.api.serializers import UserDetailSerializer


class UserRolePermissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        fields = [
            'userID',
            'utype',
            'username',
            'email',
            'userphone',
            'useraddress',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_userphone(self, value):
        qs = UserDetail.objects.filter(userphone__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this userphone already exists")
        return value

    def validate_email(self, value):
        qs = UserDetail.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this email already exists")
        return value

    def validate_username(self, value):
        qs = UserDetail.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this username already exists")
        return value


class JobCardPermissionSerializer(serializers.ModelSerializer):
    user_workshop = UserDetailSerializer(read_only=True)
    jobcard = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    inventory = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    workshop = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    counter_sale = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Permissions
        fields = [
            'permID',
            'userID',
            'jobcard',
            'inventory',
            'user',
            'user_workshop',
            'workshop',
            'counter_sale',
            'workshopID',
            'createdAt',
            'updatedAt',
        ]


class JobCardPermissionRegisterSerializer(serializers.ModelSerializer):
    user_workshop = UserRolePermissionsSerializer(required=False)
    jobcard = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    inventory = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    workshop = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    counter_sale = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Permissions
        fields = [
            'userID',
            'jobcard',
            'inventory',
            'user',
            'user_workshop',
            'workshop',
            'counter_sale',
            'workshopID'
        ]

    def create(self, validated_data):

        user_data = validated_data.pop('user_workshop')
        userid = validated_data.get("userID")
        userid = userid.userID
        userdetail = UserDetail.objects.get(userID=userid)
        expiredAt = userdetail.expiredAt

        user_obj = UserDetail.objects.create(
            utype=user_data['utype'],
            username=user_data['username'],
            email=user_data['email'],
            userphone=user_data['userphone'],
            expiredAt=expiredAt
        )
        user_obj.set_password(user_data['password'])
        user_obj.save()
        perm_obj = Permissions.objects.create(
            user_workshop=user_obj,
            userID=validated_data.get("userID"),
            workshopID=validated_data.get("workshopID"),
            jobcard=validated_data.get("jobcard"),
            inventory=validated_data.get("inventory"),
            user=validated_data.get("user"),
            workshop=validated_data.get("workshop"),
            counter_sale=validated_data.get("counter_sale")

        )
        return perm_obj


class JobCardUpdatePermissionSerializer(serializers.ModelSerializer):
    jobcard = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    inventory = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    counter_sale = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Permissions
        fields = [
            'permID',
            'userID',
            'jobcard',
            'inventory',
            'user',
            'counter_sale'
        ]


class JobCardPermissionSerializer(serializers.ModelSerializer):
    user_workshop = UserDetailSerializer(read_only=True)
    jobcard = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    inventory = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    workshop = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    counter_sale = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Permissions
        fields = '__all__'


class MarketeerRegisterSerializer(serializers.ModelSerializer):
    marketerID = UserRolePermissionsSerializer(required=False)
    admin_report = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    subscription_plan = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    capture_payment = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    requested_parts = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    service = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    part = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Marketeer
        fields = [
            'marketerID',
            'userID',
            'admin_report',
            'subscription_plan',
            'user',
            'capture_payment',
            'requested_parts',
            'part',
            'service'
        ]

    def create(self, validated_data):

        user_data = validated_data.pop('marketerID')
        userid = validated_data.get("userID")
        userid = userid.userID
        userdetail = UserDetail.objects.get(userID=userid)
        expiredAt = userdetail.expiredAt

        user_obj = UserDetail.objects.create(
            utype=user_data['utype'],
            username=user_data['username'],
            email=user_data['email'],
            userphone=user_data['userphone'],
            expiredAt=expiredAt
        )
        user_obj.set_password(user_data['password'])
        user_obj.save()
        marketeer_obj = Marketeer.objects.create(
            marketerID=user_obj,
            userID=validated_data.get("userID"),
            admin_report=validated_data.get("admin_report"),
            subscription_plan=validated_data.get("subscription_plan"),
            user=validated_data.get("user"),
            capture_payment=validated_data.get("capture_payment"),
            requested_parts=validated_data.get("requested_parts"),
            service=validated_data.get("service"),
            part=validated_data.get("part"),

        )
        return marketeer_obj


class MarketeerListSerializer(serializers.ModelSerializer):
    marketerID = UserRolePermissionsSerializer(required=False)
    admin_report = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    subscription_plan = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    capture_payment = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    requested_parts = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    service = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    part = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Marketeer
        fields = '__all__'


class MarketeerUpdateSerializer(serializers.ModelSerializer):
    admin_report = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    subscription_plan = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    user = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    capture_payment = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    requested_parts = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    service = fields.MultipleChoiceField(choices=DEMO_CHOICES)
    part = fields.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = Marketeer
        fields = [
            'mID',
            'admin_report',
            'subscription_plan',
            'user',
            'capture_payment',
            'requested_parts',
            'part',
            'service'
        ]
