#!/usr/bin/env python3
"""
Session module.
"""


from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Session authentication class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session_id for a user_id.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        """print("session id.py", session_id)"""
        uid = self.user_id_for_session_id(session_id)
        """print(uid)"""
        return User.get(uid)

    def destroy_session(self, request=None):
        """
        Deletes a user if it is found.
        """
        if request is None:
            return False
        s_id = self.session_cookie(request)
        if not s_id:
            return False
        if not self.user_id_for_session_id(s_id):
            return False
        del self.user_id_by_session_id[s_id]
        return True
