from __future__ import annotations

from django.contrib import admin
from ambassador.models import Video


@admin.register(Video)
class UserAdmin(admin.ModelAdmin):
    pass
