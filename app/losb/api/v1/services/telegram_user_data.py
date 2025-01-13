import requests
from django.contrib.auth import get_user_model


def get_telegram_user_data(telegram_id: int, bot_token: str):
    """
    Get user data from Telegram Bot API.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getChat?chat_id={telegram_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            raise ValueError("Failed to get user data from Telegram.")

        user_data = data["result"]
        return {
            "id": telegram_id,
            "first_name": user_data.get("first_name", ""),
            "last_name": user_data.get("last_name", ""),
            "username": user_data.get("username", "")
        }
    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred while getting user data from Telegram: {e}")
        return {"first_name": "", "last_name": "", "username": ""}


def prepare_user_data(user_data):
    """
    Prepare data for user creation.
    """
    telegram_id = user_data["id"]
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    username = user_data.get("username", "")
    full_name = f"{last_name} {first_name}".strip()

    return {
        'telegram_id': telegram_id,
        'nickname': username,
        'full_name': full_name
    }


def get_or_create_user(user_data: dict):
    """
    Get or create user based on prepared data.
    """
    User = get_user_model()

    prepared_user_data = prepare_user_data(user_data)

    user, created = User.objects.get_or_create(telegram_id=prepared_user_data['telegram_id'],
                                                  defaults={'full_name': prepared_user_data['full_name'],
                                                            'nickname': prepared_user_data['nickname'],
                                                            })
    return user
