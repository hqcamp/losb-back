from __future__ import annotations

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ambassador.api.v1.serializers import (
VideoSerializer
)
from ambassador.models import Video
from ambassador.api.v1.services.radius_calculation import CoordinatesService


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
        queryset = Video.objects.filter()

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
        serializer.save(user=self.request.user)
