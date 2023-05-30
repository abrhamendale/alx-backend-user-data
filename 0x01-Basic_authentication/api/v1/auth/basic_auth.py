#!/usr/bin/env python3
"""
Basic authentication module.
"""


from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode Base64 value.
        """
        if base64_authorization_header is None:
            return None
        if isinstance(base64_authorization_header, str) is False:
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('UTF-8')
        except ValueError:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
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
            return (str(decoded_base64_authorization_header.split(":")[0]),
                    str(decoded_base64_authorization_header.split(":")[1]))
        except ValueError:
            return (None, None)
