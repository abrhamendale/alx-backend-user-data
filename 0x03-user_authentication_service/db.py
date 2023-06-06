#!/usr/bin/env python3
"""DB module
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from typing import TypeVar


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, em: str, h_p: str) -> User:
        """
        A function to add a user.
        """
        if not em or not h_p:
            return None
        user_1 = User(email=em, hashed_password=h_p)
        self._session.add(user_1)
        self._session.commit()
        return user_1
    """
    def find_user_by(self, **kwargs) -> TypeVar(User):

        Finds a user by input string em.

        ret_value = self._session.query(User).filter_by(**kwargs).first()
        if ret_value:
            return ret_value
        else:
            raise NoResultFound

    def update_user(self, u_id: int, **kwargs) -> None:

        Updates a user.

        u = self.find_user_by(id=u_id)
        for key, value in kwargs.items():
            if hasattr(u, key):
                setattr(u, key, value)
            else:
                raise ValueError()
        self._session.commit()
        return None
        """
