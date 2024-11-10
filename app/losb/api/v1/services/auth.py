import json
import jwt
import urllib.parse
from app.settings import SECRET_KEY, TELEGRAM_BOT_TOKEN
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from typing import Optional
from losb.api.v1.services.telegram_user_data import get_or_create_user, get_telegram_user_data


class TokenError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class InvalidInitDataError(Exception):
    pass


class CustomAuthentication(authentication.BaseAuthentication):
    def get_raw_token(self, header: bytes) -> Optional[bytes]:
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None
        AUTH_HEADER_TYPES = ['Bearer']
        if parts[0] not in AUTH_HEADER_TYPES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _("Authorization header must contain two space-delimited values"),
                code="bad_authorization_header",
            )

        return parts[1]

    def get_init_data(self, header: bytes) -> Optional[bytes]:
        """
        Extracts Telegram initData from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None
        AUTH_HEADER_TYPES = ['Bearer']
        if parts[0] not in AUTH_HEADER_TYPES:
            # Assume the header does not contain initData
            return None

        if len(parts) != 3:
            raise AuthenticationFailed(
                _("Authorization header must contain three space-delimited values"),
                code="bad_authorization_header",
            )

        return parts[2]

    def parse_authorization_header(self, query_string):
        parsed_query = urllib.parse.parse_qs(query_string)
    
        for key, value in parsed_query.items():
            if len(value) == 1:
                parsed_query[key] = value[0]
    
        return parsed_query

    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None

        # initData based authentication
        if header.startswith("Bearer tma "):
            raw_init_data = self.get_init_data(header)
            if raw_init_data is None:
                return None

            try:
                parsed_init_data = self.parse_authorization_header(raw_init_data)
            except InvalidInitDataError as ex:
                raise TokenError(_("Invalid initData")) from ex

            try:
                User = get_user_model()
                user_data = json.loads(parsed_init_data['user'])
                user = get_or_create_user(user_data)
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

        # token based authentication
        else:
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            try:
                decoded_token = jwt.decode(
                    raw_token,
                    SECRET_KEY,
                    algorithms=['HS256'],
                )
            except InvalidTokenError as ex:
                raise TokenError(_("Token is invalid or expired")) from ex

            try:
                User = get_user_model()
                telegram_id = decoded_token.get('telegram_id')
                user_data = get_telegram_user_data(telegram_id, TELEGRAM_BOT_TOKEN)
                user = get_or_create_user(user_data)
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

        return user, None
