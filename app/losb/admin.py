from __future__ import annotations

from django.contrib import admin
from losb.models import User, Phone, City, SMSVerification, MessageLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", 'username', 'full_name', 'phone', 'birthday', 'location')
    list_display_links = ("telegram_id",)


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("id", "code", 'number')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(SMSVerification)
class SMSVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "otp", 'created_at')


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_id", "text", "sent_at")
