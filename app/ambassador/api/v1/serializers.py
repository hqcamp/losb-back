from rest_framework import serializers
from ambassador.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'duration', 'thumbnail']


class VideoUrlSerializer(serializers.Serializer):
    file_url = serializers.URLField()
