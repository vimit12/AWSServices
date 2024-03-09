import json

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from ...init_service.models import AWSUser


class AWSUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the request headers
        token = request.headers.get("Authorization")
        # print("TOKEN =========> ", token)
        if not token:
            return None

        # Validate the token
        try:
            aws_user_obj = AWSUser.objects.get(
                access_token__token__contains=token.split(" ")[-1]
            )
        except AWSUser.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        # If the token is valid, return the user and token
        return aws_user_obj.user, aws_user_obj

    def authenticate_header(self, request):
        return "Token"
