from __future__ import annotations

from django.contrib import admin
from losb.models import User, Phone, City, SMSVerification, MessageLog, TGVerification, PhoneVerificationSettings


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


@admin.register(TGVerification)
class TGVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "request_id", 'created_at')


@admin.register(PhoneVerificationSettings)
class PhoneVerificationSettingsAdmin(admin.ModelAdmin):
    list_display = ("selected_option", "tg_verification_token", "sms_verification_token")
    fieldsets = (
        (None, {
            "fields": ("selected_option",)
        }),
        ("Верификация через Telegram", {
            "fields": ("tg_verification_token",)
        }),
        ("Верификация через SMS", {
            "fields": ("sms_verification_token",)
        }),
    )

    def has_add_permission(self, request):
        return not PhoneVerificationSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
