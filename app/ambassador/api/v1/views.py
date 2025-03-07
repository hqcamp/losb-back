from __future__ import annotations

import requests
from datetime import timedelta
from django.utils import timezone
from app.settings import AMBASSADOR_BOT_TOKEN
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ambassador.api.v1.serializers import (
VideoSerializer,
VideoUrlSerializer
)
from ambassador.models import Video
from ambassador.api.v1.services.radius_calculation import CoordinatesService

import logging

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve videos within a radius",
        description=(
            "Get a list of videos filtered by the specified latitude, longitude, and radius parameters."
            "The limit parameter can be used to adjust the number of results returned (optional)"
            "Requires authentication."
        ),
        responses={200: VideoSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Create a new video",
        description="Upload a new video. Requires authentication.",
        responses={201: VideoSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete a video",
        description="Delete a video by its ID. Requires authentication.",
        responses={204: "No Content"},
    ),
)
class VideoViewSet(ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        threshold = timezone.now() - timedelta(hours=25)
        queryset = Video.objects.filter(created_at__gt=threshold)

        if self.request.method == 'GET':
            try:
                latitude = float(self.request.query_params.get('latitude'))
                longitude = float(self.request.query_params.get('longitude'))
                radius = float(self.request.query_params.get('radius'))

                queryset = CoordinatesService.calculate_radius(queryset, latitude, longitude, radius)
            except (TypeError, ValueError):
                raise ValidationError({
                    "detail": "Invalid or missing query parameters. "
                              "Ensure 'latitude', 'longitude', and 'radius' are provided as valid float values."
                })

        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except Exception as e:
            logger.error(f"Error in create method: {str(e)}", exc_info=True)
            raise e


@extend_schema_view(
    get=extend_schema(
        responses={
            200: VideoSerializer,
        },
        summary='Список историй пользователя',
        description='Возвращает список историй пользователя',
    ),
)
class UserStoriesView(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Video.objects.filter(user=self.request.user)


@extend_schema(
    request=VideoUrlSerializer,
    responses={
        200: {"type": "object", "properties": {"message": {"type": "string"}}},
    },
    summary="Отправка URL видео в Telegram",
    description="Отправляет URL видео в чат Telegram"
)
class SendToTelegramView(APIView):
    serializer_class = VideoUrlSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file_url = serializer.validated_data['file_url']

            user = request.user
            telegram_id = user.telegram_id

            telegram_api_url = f"https://api.telegram.org/bot{AMBASSADOR_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': telegram_id,
                'text': file_url
            }

            try:
                response = requests.post(telegram_api_url, json=payload)
                if response.status_code == 200:
                    return Response({"message": "URL sent successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": f"Failed to send message to Telegram. Response: {response.text}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoSwiperView(APIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @extend_schema(
        summary="Retrieve a video and nearby videos",
        description=(
            "Get a specific video by its ID and other videos within the specified radius from the video's location." 
            "The radius is passed as a query parameter." 
            "The limit parameter can be used to adjust the number of results returned (optional)"
            "Requires authentication."
        ),
        responses={200: VideoSerializer(many=True)}
    )
    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        radius = request.query_params.get('radius')
        if radius is None:
            return Response({"detail": "Missing 'radius' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            radius = float(radius)
        except ValueError:
            return Response({"detail": "Invalid 'radius' parameter, must be a float."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = video.location["latitude"]
            longitude = video.location["longitude"]
        except KeyError:
            return Response({"detail": "Invalid video location data."}, status=status.HTTP_400_BAD_REQUEST)

        threshold = timezone.now() - timedelta(hours=25)
        queryset = Video.objects.filter(created_at__gt=threshold)
        nearby_videos = CoordinatesService.calculate_radius(queryset, latitude, longitude, radius)

        all_videos = nearby_videos | Video.objects.filter(id=video_id)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(all_videos, request)

        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
