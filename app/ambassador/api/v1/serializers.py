from rest_framework import serializers
from ambassador.models import Video
from ambassador.api.v1.validators import validate_location_field


class VideoSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(validators=[validate_location_field])

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'duration']


class VideoUrlSerializer(serializers.Serializer):
    file_url = serializers.URLField()
