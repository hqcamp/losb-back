import os
import uuid


def unique_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    unique_name = f"{base}_{uuid.uuid4().hex}{ext}"
    return f"user/avatar/{unique_name}"
