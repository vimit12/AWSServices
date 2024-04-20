from django.utils import timezone
from oauthlib.common import generate_token


class TokenGeneration:
    def __init__(self):
        ...

    @classmethod
    def generate_access_token(cls) -> dict:
        # Generate a random token using oauthlib
        token = generate_token(length=256)

        # Set the token expiry time (in seconds)
        expires_in = 300

        # Set the token expiry time (as a datetime object)
        expires = timezone.now() + timezone.timedelta(seconds=expires_in)

        # Return a dictionary containing the token and its expiry time
        return {
            "token": token,
            "expires_in": expires_in,
            "expires": int(expires.timestamp()),
        }

    @classmethod
    def generate_refresh_token(cls) -> dict:
        # Generate a random token using oauthlib
        token = generate_token(length=512)

        # Set the token expiry time (in seconds)
        expires_in = 3600

        # Set the token expiry time (as a datetime object)
        expires = timezone.now() + timezone.timedelta(seconds=expires_in)

        # Return a dictionary containing the token and its expiry time
        return {
            "token": token,
            "expires_in": expires_in,
            "expires": int(expires.timestamp()),
        }
