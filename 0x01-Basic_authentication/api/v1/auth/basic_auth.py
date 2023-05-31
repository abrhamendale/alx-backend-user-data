#!/usr/bin/env python3
"""
Basic authentication module.
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns Base64 part of the authorization header.
        """
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str) is False:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decode Base64 value.
        """
        if base64_authorization_header is None:
            return None
        if isinstance(base64_authorization_header, str) is False:
            return None
        try:
            r = base64_authorization_header
            return base64.b64decode(r).decode('UTF-8')
        except ValueError:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns the email and password.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if isinstance(decoded_base64_authorization_header, str) is False:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        try:
            return (str(decoded_base64_authorization_header.split(":", 1)[0]),
                    str(decoded_base64_authorization_header.split(":", 1)[1]))
        except ValueError:
            return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        Returns a user instance based on the email and password.
        """
        if user_email is None or user_pwd is None:
            return None
        if isinstance(user_email, str) is False:
            return None
        if isinstance(user_pwd, str) is False:
            return None
        emails = User.search({'email': user_email})
        if emails:
            for i in emails:
                if i.is_valid_password(user_pwd):
                    return i
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Implements a basic authentication.
        """
        ad = self.authorization_header(self, request)
        print(ad)
        if ad:
            ad_64 = self.extract_base64_authorization_header(ad)
            print(ad_64)
        if ad_64:
            ad_64_str = decode_base64_authorization_header(ad_64)
            print(ad_64_str)
        if ad_64_str:
            user_cred = self.extract_user_credentials(ad_64_str)
            print(user_cred)
        if user_cred:
            user_inst = self.user_object_from_credentials(user_cred[0],
                                                          user_cred[1])
            print(user_inst)
            return user_inst
        return None
