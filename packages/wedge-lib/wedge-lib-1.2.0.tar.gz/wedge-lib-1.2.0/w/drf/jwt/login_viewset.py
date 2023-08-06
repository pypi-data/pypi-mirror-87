from dj_rest_auth.views import LoginView
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from w.drf.serializers.serpy_serializers import UserSerializer
from w.services.technical.date_service import DateService


class LoginViewset(LoginView):
    permission_classes = [HasAPIKey]

    def get_response(self):

        if not getattr(settings, "REST_USE_JWT", False):
            raise RuntimeError("This viewset need REST_USE_JWT=True")

        from datetime import datetime
        from rest_framework_simplejwt.settings import api_settings as jwt_settings

        jwt_expiration = datetime.utcnow() + jwt_settings.ACCESS_TOKEN_LIFETIME
        data = {
            "user": UserSerializer(self.user).data,
            "access_token": str(self.access_token),
            "expires": DateService.to_mysql_datetime(jwt_expiration),
        }
        response = Response(data, status=status.HTTP_200_OK)
        cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
        cookie_secure = getattr(settings, "JWT_AUTH_SECURE", False)
        cookie_httponly = getattr(settings, "JWT_AUTH_HTTPONLY", True)
        cookie_samesite = getattr(settings, "JWT_AUTH_SAMESITE", "Lax")

        if cookie_name:
            response.set_cookie(
                cookie_name,
                self.refresh_token,
                expires=jwt_expiration,
                secure=cookie_secure,
                httponly=cookie_httponly,
                samesite=cookie_samesite,
            )
        return response
