#!/usr/bin/env python3
""" Session Auth class """

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Authentication class """
    user_id_by_session_id = {}

    def __init__(self):
        """ the constructor method """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ create a session method """
        if user_id is None or\
                not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns user ID based on session ID """
        if session_id is None or\
                not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

