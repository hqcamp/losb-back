from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def validate_image_file(file):
    if isinstance(file, InMemoryUploadedFile):
        allowed_mime_types = [
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/bmp',
            'image/tiff',
            'image/webp'
        ]

        if file.content_type not in allowed_mime_types:
            raise ValidationError(_("Unsupported file type."))

        try:
            img = Image.open(file)
            img.verify()
        except Exception:
            raise ValidationError(_("Uploaded file is not a valid image."))

    else:
        raise ValidationError(_("Uploaded file is not a valid type."))
