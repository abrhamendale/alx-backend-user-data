#!/usr/bin/env python3
"""
Auth module.
"""


import bcrypt
from db import DB
from user import Base, User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import TypeVar, Any, Union
uuid4 = TypeVar("uuid4")
User = TypeVar("User")


def _hash_password(p_w: str) -> Any:
    """
    Returns a hashed password.
    """
    if not p_w:
        return None
    if not isinstance(p_w, str):
        return None
    password = p_w
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    has = bcrypt.hashpw(byte, salt)
    return has


def _generate_uuid() -> str:
    """
    generates a uuid.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """
        Initializes new Auth instances.
        """
        self._db = DB()

    def register_user(self, em: str, pas: str) -> User:
        """
        Registers a new user.
        """
        if not em or not pas:
            return None
        try:
            self._db.find_user_by(email=em)
            raise ValueError("User {} already exists".format(em))
        except NoResultFound:
            usr = self._db.add_user(em, _hash_password(pas))
            self._db._session.commit()
            return usr

    def valid_login(self, em: str, p_w: str) -> bool:
        """
        validates a user.
        """
        if not isinstance(em, str) or not isinstance(p_w, str):
            return False
        try:
            usr: User = self._db.find_user_by(email=em)
            if bcrypt.checkpw(p_w.encode('utf-8'), usr.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, em: str) -> str:
        """
        Creates a session ID.
        """
        try:
            usr = self._db.find_user_by(email=em)
            s_id = _generate_uuid()
            usr.session_id = s_id
            self._db._session.commit()
            return s_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, s_id: str) -> User:
        """
        Retrieves a user.
        Find_user_by
        """
        if not s_id:
            return None
        try:
            usr: User = self._db.find_user_by(session_id=s_id)
            return usr
        except NoResultFound:
            return None

    def destroy_session(self, u_id: int) -> None:
        """
        Deletes a user.
        """
        try:
            usr: User = self._db.find_user_by(id=u_id)
            usr.session_id = None
            self._db._session.commit()
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, em: str) -> str:
        """
        Resets a password.
        """
        try:
            usr = self._db.find_user_by(email=em)
            usr.reset_token = _generate_uuid()
            return usr.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, r_t: str, p_w: str) -> None:
        """
        Updates a password for a user.
        """
        try:
            usr = self._db.find_user_by(reset_token=r_t)
            usr.hashed_password = _hash_password(p_w)
            usr.reset_token = None
            self._db._session.commit()
        except NoResultFound:
            raise ValueError
