from __future__ import annotations

from django.contrib import admin
from losb.models import User, Phone, City, SMSVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", 'username', 'full_name', 'phone', 'birthday', 'location')


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("id", "code", 'number')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(SMSVerification)
class SMSVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "otp", 'created_at')
