from __future__ import annotations

from random import SystemRandom

from datetime import datetime, timezone
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from app import settings
from losb.api.v1 import exceptions
from losb.api.v1.serializers import (
    UserAvatarSerializer,
    UserSerializer,
    UserNameSerializer,
    UserCitySerializer,
    UserBirthdaySerializer,
    UserPhoneSerializer,
    CitySerializer,
    UserPhoneVerificationSerializer,
    PhoneSerializer,
    BotUrlSerializer,
)
from losb.api.v1.services.sms_verification import SmsVerificationService
from losb.api.v1.services.webhook_last_message_service import WebhookLastMessageService
from losb.models import City, MessageLog
from losb.schema import TelegramIdJWTSchema  # do not remove, needed for swagger

from losb.api.v1.filters import CityFilter


@extend_schema_view(
    get=extend_schema(
        responses={
            200: CitySerializer,
        },
        summary='Список городов России',
        description='Возвращает список городов России',
    ),
)
class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = LimitOffsetPagination
    queryset = City.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CityFilter


@extend_schema_view(
    get=extend_schema(
        responses={
            200: UserSerializer,
        },
        summary='Профиль пользователя',
        description='Возвращает профиль пользователя',
    ),
)
class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    update=extend_schema(
        responses={
            200: UserSerializer,
        },
        summary='Изменение имени пользователя',
    ),
)
class UserNameUpdateView(generics.UpdateAPIView):
    serializer_class = UserNameSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ["patch"]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data)


@extend_schema_view(
    patch=extend_schema(
        responses={
            200: UserSerializer,
        },
        summary='Изменение города пользователя',
    ),
)
class UserCityUpdateView(generics.UpdateAPIView):
    serializer_class = UserCitySerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ["patch"]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = UserSerializer(user)
        return Response(response_serializer.data)


class UserBirthdayAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated, ]

    @extend_schema(
        request=UserBirthdaySerializer,
        responses={
            200: UserSerializer,
        },
        summary='Установить дату рождения пользователя',
        description='Устанавливает дату рождения пользователя, если она ещё не была изменена',
    )
    def post(self, request):
        if self.request.user.birthday:
            raise exceptions.BirthdayAlreadyRegistered

        serializer = UserBirthdaySerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)

        response_serializer = UserSerializer(self.request.user)
        return Response(response_serializer.data)


class UserPhoneUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]
    http_method_names = ["post", "patch"]

    @staticmethod
    def get_otp():
        return "".join(SystemRandom().choice('123456789') for _ in range(settings.SMS_VERIFICATION_CODE_DIGITS))

    @extend_schema(
        request=UserPhoneSerializer,
        responses={
            200: {},
        },
        summary='Запросить код подтверждения',
        description='Отправляет otp код на указанный номер телефона',
    )
    def post(self, request):
        serializer = UserPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = SmsVerificationService(request.user)
            verification_code = service.request_verification(
                code=serializer.data['code'],
                number=serializer.data['number'],
            )
        except exceptions.SmsDeliveryError as e:
            raise exceptions.SmsDeliveryError(detail=f"Failed to send SMS: {e}")

        # TODO: remove otp from response, for debug only
        return Response(data={"otp": verification_code}, status=status.HTTP_200_OK)

    @extend_schema(
        request=UserPhoneVerificationSerializer,
        responses={
            200: UserSerializer,
        },
        summary='Верифицировать код подтверждения',
        description='Верифицирует код подтверждения, в случаи успеха обновляет номер телефона пользователя',
    )
    def patch(self, request):
        serializer = UserPhoneVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = SmsVerificationService(request.user)
        service.verify_code(
            otp=serializer.data['otp'],
            code=serializer.data['phone']['code'],
            number=serializer.data['phone']['number'],
        )

        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


@extend_schema_view(
    get=extend_schema(
        responses={
            200: BotUrlSerializer,
        },
        summary='Cсылка на бота поддержки',
    ),
)
class TechSupportAPIView(generics.RetrieveAPIView):
    serializer_class = BotUrlSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return {'url': settings.TECHSUPPORT_BOT_URL}


@extend_schema_view(
    post=extend_schema(
        request=UserAvatarSerializer,
        responses={
            200: UserSerializer,
        },
        summary='Загрузить аватар пользователя',
        description='Загружает новый аватар в профиль пользователя',
    ),
)
class UserAvatarUpdateView(generics.UpdateAPIView):
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated, ]
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['post']

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user.avatar_url = serializer.validated_data['avatar_url']
        user.save()

        return Response(UserSerializer(user).data)


@extend_schema_view(
    get=extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'avatar_url': {'type': 'string'},
                    'message': {'type': 'string'},
                    'time': {'type': 'string'},
                },
            },
        },
        summary='Получить последнее сообщение, аватар пользователя и время сообщения',
    ),
)
class LastMessageAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get']

    def get(self, request):
        service = WebhookLastMessageService(request.user.telegram_id)

        last_message_info, error = service.get_last_message()
        avatar_url = service.get_avatar_url()

        if error:
            return Response({'error': error}, status=400)

        return Response({
            'avatar_url': avatar_url,
            'message': last_message_info['message'] if last_message_info else None,
            'time': last_message_info['time'].strftime('%H:%M') if last_message_info else None,
        })


class TelegramWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        update = request.data

        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            timestamp = datetime.fromtimestamp(message['date'], tz=timezone.utc)

            MessageLog.objects.update_or_create(
                chat_id=chat_id,
                defaults={'text': text, 'sent_at': timestamp}
            )

        return Response({"status": "ok"}, status=200)

