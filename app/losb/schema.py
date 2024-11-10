from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension

from losb.api.v1.services.auth import CustomAuthentication


class TelegramIdJWTSchema(OpenApiAuthenticationExtension):
    target_class = CustomAuthentication
    name = 'CustomAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': _(
                'Token-based authentication with required prefix "%s"'
            ) % "Token"
        }
