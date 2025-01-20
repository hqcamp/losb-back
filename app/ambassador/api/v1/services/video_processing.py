import os
import requests
import imageio_ffmpeg as ffmpeg
import subprocess
import re
from datetime import timedelta
from django.conf import settings
from tempfile import NamedTemporaryFile
import logging

logger = logging.getLogger(__name__)


class VideoProcessingService:
    def __init__(self, video_url: str, thumbnail_path: str, time: int = 1, thumbnail_exists: bool = False):
        self.video_url = video_url
        self.thumbnail_path = thumbnail_path
        self.time = time
        self.local_video_path = None
        self.thumbnail_exists = thumbnail_exists

    def download_file(self):
        file_name = os.path.basename(self.video_url)

        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        file_path = os.path.join(temp_dir, file_name)

        response = requests.get(self.video_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.local_video_path = file_path
            logger.info(f"Video uploaded: {file_path}")
        else:
            logger.error(f"Video upload error: {response.status_code}")
            raise RuntimeError(f"Video upload error: {response.status_code}")

    def extract_duration(self):
        if not self.local_video_path:
            raise ValueError("Video local path is not set.")

        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()

        try:
            cmd = [
                ffmpeg_exe,
                "-nostdin",
                "-i", self.local_video_path,
                "-f", "null", "-"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            stderr = result.stderr
            match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", stderr)
            if match:
                hours, minutes, seconds = map(float, match.groups())
                duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                logger.info(f"Video duration: {duration}")
                return duration
            else:
                logger.error("Failed to extract video duration.")
                raise ValueError("Failed to extract video duration.")
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg probe failed: {e.stderr}")
            raise RuntimeError(f"FFmpeg probe failed: {e.stderr}")

    def generate_thumbnail(self):
        if not self.local_video_path:
            raise ValueError("Video local path is not set.")

        if self.thumbnail_exists:
            return

        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
        local_thumbnail = NamedTemporaryFile(suffix=".jpg", delete=False)

        try:
            os.makedirs(os.path.dirname(self.thumbnail_path), exist_ok=True)

            cmd = [
                ffmpeg_exe, "-y",
                "-i", self.local_video_path, "-ss", str(self.time),
                "-vframes", "1", local_thumbnail.name
            ]
            subprocess.run(cmd, check=True)

            with open(local_thumbnail.name, 'rb') as thumb_file:
                with open(self.thumbnail_path, 'wb') as thumb_output:
                    thumb_output.write(thumb_file.read())

            logger.info(f"Thumbnail created: {self.thumbnail_path}")
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
            raise RuntimeError(f"FFmpeg thumbnail generation failed: {e}")
        finally:
            try:
                os.remove(local_thumbnail.name)
            except PermissionError as e:
                logger.warning(f"Failed to delete temporary file: {local_thumbnail.name}. {e}")

    def process_video(self):
        self.download_file()
        try:
            duration = self.extract_duration()
            self.generate_thumbnail()
            return duration
        finally:
            if self.local_video_path and os.path.exists(self.local_video_path):
                os.remove(self.local_video_path)
                logger.info(f"Temporary video file deleted: {self.local_video_path}")
