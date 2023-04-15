from rest_framework import serializers

from src.apis.notifications.models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = [
            'userID',
            'message',
            'is_read',
            'createdAt',
            'updatedAt',
        ]


class NotificationsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = [
            'notifyID',
            'userID',
            'message',
            'is_read',
            'createdAt',
            'updatedAt'
        ]


class NotificationsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = [
            'notifyID',
            'userID',
            'message',
            'is_read'
        ]
