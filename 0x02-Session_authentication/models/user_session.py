#!/usr/bin/env python3
"""
A user session class.
"""


from models.base import Base


class UserSession(Base):
    """
    User session class.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes new UserSession instances.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        user_id = kwargs.get('user_id')
        session_id = kwargs.get('session_id')
