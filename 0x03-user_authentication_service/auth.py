#!/usr/bin/env python3
"""
Auth module.
"""


import bcrypt
from db import DB
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(p_w: str):
    """
    Returns a hashed password.
    """
    password = p_w
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    has = bcrypt.hashpw(byte, salt)
    return has


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes new Auth instances.
        """
        self._db = DB()

    def register_user(self, em, pas):
        """
        Registers a new user.
        """
        try: 
            self._db.find_user_by(email = em)
            raise ValueError("User %em already exists")
        except NoResultFound:
            return self._db.add_user(em, _hash_password(pas))

    def valid_login(self, em, p_w):
        """
        validates a user.
        """
        try:
            usr = self._db.find_user_by(email = em)
            if usr:
                if bcrypt.checkpw(p_w.encode('utf-8'), usr.hashed_password):
                    return True
                else:
                    return False
            else:
                return False
        except NoResultFound:
            return False

    def _generate_uuid(self):
        """
        generates a uuid.
        """
        return uuid.uuid4()

    def create_session(self, em: str):
        """
        Creates a session ID.
        """
        try:
            usr = self._db.find_user_by(email = em)
            s_id = self._generate_uuid()
            usr.session_id = str(s_id)
            self._db._session.commit()
            return s_id
        except NoResultFound:
            return None

    def get_user_from_session_id(s_id: str):
        """
        Retrieves a user.
        Find_user_by
        """
        ret_value = AUTH._db._session.query(User).filter_by(session_id = s_id).first()
        return ret_value

    def destroy_session(u_id: str):
        """
        Deletes a user.
        """
        usr = self._db.find_user_by(user_id = u_id)
        usr.session_id = None
        self._db._session.commit()
        return None

    def get_reset_password_token(em: str):
        """
        Resets a password.
        """
        try:
            usr = self._db.find_user_by(email = em)
            usr.reset_token = self._generate_uuid()
            return usr.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(r_t: str, p_w str):
        """
        Updates a password for a user.
        """
        try:
            usr = self._db.find_user_by(reset_token = r_t))
            usr.hashed_password = _hash_password(p_w)
            usr.reset_token = None
            self._db._session.commit()
        except NoResultFound:
            raise ValueError