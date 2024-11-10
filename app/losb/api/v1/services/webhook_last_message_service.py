from losb.models import MessageLog
from django.conf import settings


class WebhookLastMessageService:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.relative_avatar_url = 'images/default_avi.png'

    def get_last_message(self):
        try:
            last_message = MessageLog.objects.filter(chat_id=self.telegram_id).first()
            if last_message:
                return {
                    "message": last_message.text,
                    "time": last_message.sent_at
                }, None
            return None, "No messages found for this user."
        except MessageLog.DoesNotExist:
            return None, "No messages found for this user."

    def get_avatar_url(self):
        return f"{settings.MEDIA_URL}{self.relative_avatar_url}"
