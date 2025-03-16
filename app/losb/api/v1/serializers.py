from rest_framework import serializers
from losb.models import User, City, Phone, SMSVerification, TGVerification


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('code', 'number')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class UserSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('tg_link', 'vk_link')


class UserSerializer(serializers.ModelSerializer):
    location = CitySerializer()
    phone = PhoneSerializer()
    social = UserSocialMediaSerializer(source="*")

    class Meta:
        model = User
        fields = ('telegram_id', 'avatar_url', 'full_name', 'phone', 'location', 'birthday', 'social')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('phone') is None:
            representation['phone'] = {"code": "7", "number": ""}
        return representation


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name',)


class UserCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'location')


class UserBirthdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('birthday',)


class UserPhoneSerializer(serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = Phone
        fields = ('code', 'number')


class SMSVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSVerification
        fields = ('otp',)


class UserPhoneVerificationSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer()

    class Meta:
        model = SMSVerification
        fields = ('otp', 'phone')


class UserPhoneTGVerificationSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer()
    otp = serializers.CharField(write_only=True)
    request_id = serializers.CharField(read_only=True)

    class Meta:
        model = TGVerification
        fields = ('request_id', 'phone', 'otp')


class BotUrlSerializer(serializers.Serializer):
    url = serializers.CharField()


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar_url',)
