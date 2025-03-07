from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ambassador.models import Video
from ambassador.api.v1.validators import validate_location_field, validate_location


class VideoSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(validators=[validate_location_field])
    tg_link = serializers.SerializerMethodField()
    vk_link = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'duration', 'tg_link', 'vk_link']

    def validate_location(self, value):
        try:
            validate_location(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return value

    def get_tg_link(self, obj):
        return obj.user.tg_link if obj.user else None

    def get_vk_link(self, obj):
        return obj.user.vk_link if obj.user else None


class VideoUrlSerializer(serializers.Serializer):
    file_url = serializers.URLField()
