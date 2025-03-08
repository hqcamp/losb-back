from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ambassador.api.v1.views import (
    VideoViewSet,
    UserStoriesView,
    SendToTelegramView,
    VideoSwiperView,
)

app_name = 'ambassador'

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
    path('stories/', UserStoriesView.as_view(), name='user-stories'),
    path('send-video-url/', SendToTelegramView.as_view(), name='send_video_url'),
    path('videos/<int:video_id>/swiper/', VideoSwiperView.as_view(), name='video-swiper'),
]
