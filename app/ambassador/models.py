from django.contrib.auth import get_user_model
from django.core.files import File
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from ambassador.api.v1.validators import validate_location, validate_file_size
from ambassador.api.v1.services.video_processing import VideoProcessingService
from ambassador.api.v1.services.unique_naming import unique_upload_to
import os
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    location = models.JSONField(default=dict)
    duration = models.DurationField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    file_url = models.FileField(upload_to=unique_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True, max_length=100)

    _prev_file_url = None

    def __str__(self):
        return f"Video by {self.user.nickname} at {self.created_at}"

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.full_clean()
        is_file_url_updated = self.file_url != self._prev_file_url
        super().save(*args, **kwargs)

        if is_file_url_updated:
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f'{self.pk}_thumbnail.jpg')
            service = VideoProcessingService(self.file_url.url, thumbnail_path)
            self.duration = service.process_video()

            with open(thumbnail_path, 'rb') as thumb_file:
                self.thumbnail.save(os.path.basename(thumbnail_path), File(thumb_file), save=False)

            super().save(update_fields=["duration", "thumbnail"])

        self._prev_file_url = self.file_url

    def clean(self):
        super().clean()

        if self.location is not None:
            try:
                validate_location(self.location)
            except ValidationError as e:
                raise ValidationError({"location": e.messages})

        if self.file_url:
            validate_file_size(self.file_url)
