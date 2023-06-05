#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, em: str, h_p:str):
        """
        A function to add a user.
        """
        user_1 = User(email = em, hashed_password = h_p)
        self._session.add(user_1)
        self._session.commit()
        return user_1

    def find_user_by(self, em: str):
        """
        Finds a user by input string em.
        """
        for row in self._session.query(User).\filter_by(email=em):
            return row
