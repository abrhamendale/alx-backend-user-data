#!/usr/bin/env python3
"""
Authentication module.
"""


from flask import request


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
        if path in excluded_paths or path + "/" in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """
        handles authorization.
        """
        if reauest is None:
            return None
        if "Authorization" in request.keys():
            return (request["Authorization"]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Checks current user.
        """
        return None
