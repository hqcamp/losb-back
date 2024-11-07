from urllib.parse import quote

import requests
from django.conf import settings

from losb.api.v1 import exceptions


class SmsRuService:
    BASE_URL = "https://sms.ru/sms/send"

    def __init__(self):
        self.api_key = settings.SMS_RU_API_KEY
        self.default_params = {
            'api_id': self.api_key,
            'json': 1
        }

    def send_sms(self, phone: str, message: str) -> dict[str, str]:
        """
        Send SMS using sms.ru API

        Args:
            phone: Phone number (ex. 74993221627)
            message: Text message to send

        Returns:
            dict: API response

        Raises:
            SmsDeliveryError: If SMS couldn't be sent
        """
        try:
            encoded_message = quote(message)

            params = {
                **self.default_params,
                'to': phone,
                'msg': encoded_message
            }

            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()

            result = response.json()

            if result.get('status') == 'OK':
                for phone, info in result.get('sms', {}).items():
                    if info.get('status') != 'OK':
                        raise exceptions.SmsDeliveryError(
                            f"Error sending to {phone}: {info.get('status_text', 'Unknown error')}")
            else:
                raise exceptions.SmsDeliveryError(
                    f"SMS service unavailable: {result.get('status_text', 'Unknown error')}")

            return result

        except requests.RequestException as e:
            raise exceptions.SmsDeliveryError(f"SMS service unavailable: {str(e)}")

        except Exception as e:
            raise exceptions.SmsDeliveryError(f"{str(e)}")
