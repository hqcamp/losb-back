from losb.models import TGVerification
from losb.api.v1 import exceptions

from losb.api.v1.services.sms_verification import SmsVerificationService
from losb.api.v1.services.telegram_verification import TelegramVerificationService


class MainVerificationService:
    def __init__(self, user):
        self.user = user

    def send_otp_telegram(self, code: str, number: str):
        service = TelegramVerificationService(self.user)

        try:
            request_id = service.send_verification_code(code=code, number=number)
        except exceptions.SmsDeliveryError as e:
            raise exceptions.SmsDeliveryError(detail=f"Failed to send verification code: {e}")

        if not self.user.tg_verification:
            self.user.tg_verification = TGVerification.objects.create(request_id=request_id)
        else:
            self.user.tg_verification.request_id = request_id
            self.user.tg_verification.save()

        self.user.save()

    def send_otp_sms(self, code: str, number: str):
        service = SmsVerificationService(self.user)

        try:
            service.request_verification(code=code, number=number)
        except exceptions.SmsDeliveryError as e:
            raise exceptions.SmsDeliveryError(detail=f"Failed to send SMS: {e}")

    def verify_telegram_code(self, otp: str, code: str, number: str):
        service = TelegramVerificationService(self.user)

        try:
            service.verify_code(request_id=self.user.tg_verification.request_id, user_code=otp)
        except exceptions.SmsVerificationFailed as e:
            raise exceptions.SmsVerificationFailed(detail=str(e))

        self.user.phone.code = code
        self.user.phone.number = number
        self.user.phone.save()
        self.user.tg_verification.delete()

    def verify_sms_code(self, otp: str, code: str, number: str):
        service = SmsVerificationService(self.user)
        service.verify_code(otp=otp, code=code, number=number)
