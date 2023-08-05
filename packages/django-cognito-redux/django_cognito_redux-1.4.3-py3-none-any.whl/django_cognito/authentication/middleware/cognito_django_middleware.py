from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from django_cognito.authentication.middleware import helpers


# This is utilised from normal Django views. Currently used for anything that requires authentication but isn't
# already utilising rest framework
class AwsDjangoMiddleware(MiddlewareMixin):
    def __call__(self, request):
        # Get the user and a new token if required
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            return self.get_response(request)

        user, token, refresh_token = helpers.process_request(request)

        request.user = user

        response = self.get_response(request)

        if token:
            # TODO: Set the token in the response here as well? If the user hits here, they're still active
            http_only = settings.HTTP_ONLY_COOKIE
            secure = settings.SECURE_COOKIE

            response.set_cookie(key='AccessToken', value=token,
                                secure=secure, httponly=http_only)
            response.set_cookie(key="RefreshToken", value=refresh_token,
                                secure=secure, httponly=http_only)

        return response
