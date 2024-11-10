from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = "Set up Telegram webhook"

    def handle(self, *args, **kwargs):
        TECHSUPPORT_BOT_TOKEN = settings.TECHSUPPORT_BOT_TOKEN
        WEBHOOK_URL = f"{settings.DOMAIN_NAME}api/v1/losb/webhook"

        response = requests.get(
            f"https://api.telegram.org/bot{TECHSUPPORT_BOT_TOKEN}/setWebhook",
            params={"url": WEBHOOK_URL}
        )

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("Telegram webhook set successfully."))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to set Telegram webhook: {response.status_code}, "
                                               f"{response.text}"))
