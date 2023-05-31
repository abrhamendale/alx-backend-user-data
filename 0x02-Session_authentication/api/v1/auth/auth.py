#!/usr/bin/env python3
"""
Authentication module.
"""


from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """
    Auth class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks entered path.
        """
        if path is None or excluded_paths is None:
            return True
        if excluded_paths is []:
            return True
        for i in excluded_paths:
            if re.search(i, path):
                return False
            if re.search(i, path + '/'):
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        handles authorization.
        """
        if request is None:
            return None
        if request.headers.get('Authorization'):
            return (request.headers.get('Authorization'))
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Checks current user.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.
        """
        if request is None:
            return None
        c_name = os.getenv('SESSION_NAME')
        if c_name:
            return request.cookies.get(c_name)
        else:
            return None
