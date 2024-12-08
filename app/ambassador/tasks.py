from __future__ import annotations

from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from ambassador.models import Video
import logging

logger = logging.getLogger(__name__)


@shared_task
def delete_outdated_videos():
    threshold = timezone.now() - timedelta(hours=24)
    outdated_videos = Video.objects.filter(created_at__lte=threshold)

    for video in outdated_videos:
        try:
            if video.file_url:
                video.file_url.delete(save=False)

            if video.thumbnail:
                video.thumbnail.delete(save=False)

            video.delete()
            logger.info(f"Video ID {video.id} deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete video ID {video.id}: {e}")
