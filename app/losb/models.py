from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import CASCADE, PROTECT, SET_NULL
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import timezone as dt_timezone
from losb.api.v1.services.telegram_user_data import get_telegram_user_data, prepare_user_data

from app import settings


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f'{self.name}'


class TGVerification(models.Model):
    request_id = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)


class SMSVerification(models.Model):
    otp = models.CharField(max_length=10)
    attempts = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id}, OTP: {self.otp}"


class Phone(models.Model):
    code = models.CharField(max_length=4)
    number = models.CharField(blank=True, max_length=15, default='') #TODO: should regex validation be added?

    def __str__(self):
        return f'+{self.code}{self.number if self.number else "-not-verified"}'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, telegram_id, password, **extra_fields):
        """
        Create and save a user with the given telegram_id and password.
        """
        if not telegram_id:
            raise ValueError(_("The telegram_id must be set"))

        bot_token = settings.TELEGRAM_BOT_TOKEN
        user_data = get_telegram_user_data(telegram_id, bot_token)
        prepared_user_data = prepare_user_data(user_data)

        phone = Phone.objects.create(code=7)
        user = self.model(
            telegram_id=telegram_id,
            phone=phone,
            full_name=prepared_user_data['full_name'],
            nickname=prepared_user_data['nickname'],
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, telegram_id, password, **extra_fields):
        """
        Create and save a SuperUser with the given telegram_id and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(telegram_id, password, **extra_fields)
    
    def get(self, *args, **kwargs):
        return super().select_related('phone', 'location').get(*args, **kwargs) #TODO: potentially add verification_code


class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.ForeignKey(Phone, on_delete=SET_NULL, related_name='user', blank=True, null=True)
    tg_verification = models.ForeignKey(TGVerification, null=True, blank=True, on_delete=SET_NULL, related_name='user')
    sms_verification = models.ForeignKey(SMSVerification, null=True, blank=True, on_delete=SET_NULL, related_name='user')
    avatar_url = models.ImageField(
        'Аватар',
        upload_to='user/avatar/',
        blank=True,
        null=True,
        max_length=512
    )
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    location = models.ForeignKey(City, on_delete=PROTECT, related_name='user', blank=True, null=True)

    username = models.CharField(max_length=255, blank=True, default='')
    password = models.CharField(max_length=255, blank=True, default='')
    last_login = None
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Makes birthday field insensitive to timezones
        if self.birthday and timezone.is_aware(self.birthday):
            self.birthday = timezone.make_naive(self.birthday, timezone=dt_timezone.utc)
        super().save(*args, **kwargs)


class MessageLog(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.chat_id} - {self.text} - {self.sent_at}'
