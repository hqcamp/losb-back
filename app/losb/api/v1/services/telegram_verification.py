import requests
from django.conf import settings
from losb.api.v1 import exceptions

from losb.models import Phone, PhoneVerificationSettings


class TelegramVerificationService:
    BASE_URL = settings.TELEGRAM_GATEWAY_BASE_URL

    def __init__(self, user):
        verification_settings = PhoneVerificationSettings.objects.first()
        self.user = user
        self.token = verification_settings.tg_verification_token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def send_verification_code(self, code, number, ttl=60):
        endpoint = "sendVerificationMessage"
        url = f"{self.BASE_URL}{endpoint}"
        phone_number = f"{code}{number}"
        json_body = {
            "phone_number": phone_number,
            "code_length": settings.SMS_VERIFICATION_CODE_DIGITS,
            "ttl": ttl
        }

        if not self.user.phone:
            self.user.phone = Phone.objects.create(code=7)
            self.user.save()

        if self.user.phone.code == code[1:] and self.user.phone.number == number:
            raise exceptions.PhoneAlreadyVerified()

        response = requests.post(url, headers=self.headers, json=json_body)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("ok"):
                result = response_json.get("result", {})
                return result.get("request_id")
            else:
                raise exceptions.SmsDeliveryError(response_json.get("error", "Unknown error"))
        else:
            raise exceptions.SmsDeliveryError(f"HTTP {response.status_code}: Failed to send verification code")

    def verify_code(self, request_id, user_code):
        endpoint = "checkVerificationStatus"
        url = f"{self.BASE_URL}{endpoint}"
        json_body = {
            "request_id": request_id,
            "code": user_code
        }

        response = requests.post(url, headers=self.headers, json=json_body)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("ok"):
                result = response_json.get("result", {})
                verification_status = result.get("verification_status", {}).get("status")
                if verification_status == "code_valid":
                    return True
                elif verification_status == "code_invalid":
                    raise exceptions.SmsVerificationFailed("Invalid code")
                elif verification_status == "expired":
                    raise exceptions.SmsVerificationExpired("Code expired")
                else:
                    raise exceptions.SmsVerificationFailed("Verification failed")
            else:
                raise exceptions.SmsVerificationFailed(response_json.get("error", "Unknown error"))
        else:
            raise exceptions.SmsVerificationFailed(f"HTTP {response.status_code}: Verification failed")
