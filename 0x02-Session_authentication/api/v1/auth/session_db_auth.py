#!/usr/bin/env python3
"""
DB based session authentication module.
"""


from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth
import json
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """
    A class for DB based authentication.
    """

    def __init__(self):
        """
        Initializes new sessionDBauth instances.
        """
        super().__init__()

    def create_session(self, user_id=None):
        """
        Creates and stores new instance of
        UserSession and returns the Session ID
        """
        if not user_id:
            return None
        se_id = super().create_session(user_id)
        if se_id:
            with open("session_db", "w") as fw:
                for i in self.user_id_by_session_id.keys():
                    dat = self.user_id_by_session_id[i]['created_at']
                    self.user_id_by_session_id[i]['created_at'] = dat.strftime('%y-%m-%d %H:%M:%S.%f')
                json.dump(self.user_id_by_session_id, fw)
        return se_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting 
        UserSession in the database based on session_id
        """
        if not session_id:
            return None
        with open("session_db", "r") as fr:
            self.user_id_by_session_id = json.load(fr)
            for i in self.user_id_by_session_id.keys():
                d = self.user_id_by_session_id[i]['created_at']
                dat = datetime.strptime(d, '%y-%m-%d %H:%M:%S.%f')
                self.user_id_by_session_id[i]['created_at'] = dat
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the
        Session ID from the request cookie.
        """
        if request is None:
            return False
        s_id = self.session_cookie(request)
        if not s_id:
            return False
        if self.user_id_for_session_id(s_id):
            del self.user_id_by_session_id[s_id]
            with open("session_db", "w") as fw:
                for i in self.user_id_by_session_id.keys():
                    dat = self.user_id_by_session_id[i]['created_at']
                    self.user_id_by_session_id[i]['created_at'] = dat.strftime('%y-%m-%d %H:%M:%S.%f')
                json.dump(self.user_id_by_session_id, fw)
        else:
            with open("session_db", "rw") as frw:
                self.user_id_by_session_id = json.load(frw)
                for i in self.user_id_by_session_id.keys():
                    d = self.user_id_by_session_id[i]['created_at']
                    dat = datetime.strptime(d, '%y-%m-%d %H:%M:%S.%f')
                    self.user_id_by_session_id[i]['created_at'] = dat
                if self.user_id_for_session_id(s_id):
                    del self.user_id_by_session_id[s_id]
                    for i in self.user_id_by_session_id.keys():
                        dat = self.user_id_by_session_id[i]['created_at']
                        self.user_id_by_session_id[i]['created_at'] = dat.strftime('%y-%m-%d %H:%M:%S.%f')
                    json.dump(self.user_id_by_session_id, frw)
