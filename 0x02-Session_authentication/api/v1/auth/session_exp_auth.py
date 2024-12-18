#!/usr/bin/env python3
""" Expiration date to session ID """
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Expiration date class """
    def __init__(self):
        """ the constructor method """
        super().__init__()
        try:
            self.session_duration =\
                int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create new session - overload """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ return user id for the session id """
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None
        if self.session_duration <= 0:
            return session_data.get("user_id")
        created_at = session_data.get("created_at")
        if created_at is None:
            return None
        if created_at + timedelta(seconds=self.session_duration)\
                < datetime.now():
            return None

        return session_data.get("user_id")
