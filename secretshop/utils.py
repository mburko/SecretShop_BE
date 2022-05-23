from rest_framework.response import Response
from rest_framework import status
import jwt


class AuthenticationUtils:
    @staticmethod
    def authenticate(func):
        def auth_inner(*args, **kwargs):
            token = args[1].headers.get("Authorization")
            if not token:
                return Response({"message:": "Unauthenticated"},
                                status=status.HTTP_400_BAD_REQUEST)

            import os
            from dotenv import find_dotenv, load_dotenv

            load_dotenv(find_dotenv('./.env'))

            try:
                payload = jwt.decode(token, os.getenv("JWT_CODE"),
                                     algorithms=["HS256"])
            except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
                return Response({"message:": "Unauthenticated"},
                                status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return auth_inner
