#!/usr/bin/env python3
"""
Session expiration module.
"""


import os
from datetime import timedelta, datetime
from api.v1.auth.session_auth import SessionAuth
from models.user import User


class SessionExpAuth(SessionAuth):
    """
    class for session expiration control.
    """

    def __init__(self):
        """
        Initializes new sessionexpauth instances.
        """
        if not os.getenv('SESSION_DURATION'):
            self.session_duration = 0
        else:
            try:
                s = int(os.getenv('SESSION_DURATION'))
            except ValueError:
                s = 0
            if s:
                self.session_duration = s
            else:
                self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a new session.
        """
        if not user_id:
            return None
        se_id = super().create_session(user_id)
        if not se_id:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[se_id] = session_dictionary
        return se_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user id associated with a session id.
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        s_dct = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return s_dct['user_id']
        if 'created_at' not in s_dct.keys():
            return None
        dur = self.session_duration * timedelta(seconds=1)
        if (s_dct['created_at'] + dur) < datetime.now():
            return None
        else:
            return s_dct['user_id']

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        uid = self.user_id_for_session_id(session_id)
        return User.get(uid)
