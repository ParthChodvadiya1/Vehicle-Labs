from rest_framework import serializers
from src.apis.media.models import MediaDetails


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaDetails
        fields = [
                'mediaID',
                'mediaType',
                'mediaURL',
                'createdAt',
                'updatedAt',
        ]

class MediaDetailSerializer(serializers.ModelSerializer):
        
    mediaID = serializers.IntegerField(required=False)
    class Meta:
        model = MediaDetails
        fields = [
                'mediaID',
                'mediaType',
                'mediaURL',
                'createdAt',
                'updatedAt',
        ]

