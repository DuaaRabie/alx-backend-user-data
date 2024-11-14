#!/usr/bin/env python3
""" Sessions in database """
from models.base import Base


class UserSession(Base):
    """ Sessions in database class """
    def __init__(self, *args: list, **kwargs: dict):
        """ the constructor method """
        super().__init__(*args, **kwargs)
        self.user_id = str(kwargs.get('user_id'))
        self.session_id = str(kwargs.get('session_id'))
