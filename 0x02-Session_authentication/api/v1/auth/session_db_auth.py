#!/usr/bin/env python3
"""
DB based session authentication module.
"""


from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth
import json
from datetime import datetime


def serialize_dict(idct):
    """
    Serializes a dictionary including datetime.
    """
    for i in idct:
        dat = idct[i]['created_at']
        idct[i]['created_at'] = dat.strftime('%y-%m-%d %H:%M:%S.%f')
    return idct


def deserialize_dict(idct):
    """
    Deserializes a dictionary including datetime.
    """
    for i in idct.keys():
        d = idct[i]['created_at']
        dat = datetime.strptime(d, '%y-%m-%d %H:%M:%S.%f')
        idct[i]['created_at'] = dat
    return idct


class SessionDBAuth(SessionExpAuth):
    """
    A class for DB based authentication.
    """

    def __init__(self):
        """
        Initializes new sessionDBauth instances.
        """
        super().__init__()

    """
    @classmethod
    def serialize_dict(idct):
        
        Serializes a dictionary including datetime.
        
        for i in idct:
            dat = idct[i]['created_at']
            idct[i]['created_at'] = dat.strftime('%y-%m-%d %H:%M:%S.%f')
        return idct

    @classmethod
    def deserialize_dict(idct):
        
        Deserializes a dictionary including datetime.
        
        for i in idict.keys():
            d = idict[i]['created_at']
            dat = datetime.strptime(d, '%y-%m-%d %H:%M:%S.%f')
            idict[i]['created_at'] = dat
        return idict
    """

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
                dat = self.user_id_by_session_id
                self.user_id_by_session_id = serialize_dict(dat)
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
            d = self.user_id_by_session_id
            self.user_id_by_session_id = deserialize_dict(d)
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
                dat = self.user_id_by_session_id
                self.user_id_by_session_id = serialize_dict(dat)
                json.dump(self.user_id_by_session_id, fw)
        else:
            with open("session_db", "rw") as frw:
                self.user_id_by_session_id = json.load(frw)
                d = self.user_id_by_session_id
                self.user_id_by_session_id = deserialize_dict(d)
                if self.user_id_for_session_id(s_id):
                    del self.user_id_by_session_id[s_id]
                    dat = self.user_id_by_session_id
                    self.user_id_by_session_id = serialize_dict(dat)
                    json.dump(self.user_id_by_session_id, frw)
