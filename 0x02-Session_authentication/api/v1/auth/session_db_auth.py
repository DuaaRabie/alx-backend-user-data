#!/usr/bin/env python3
""" UserSession model
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class """
    def __init__(self):
        """ constructor method """
        super().__init__()

    def create_session(self, user_id=None):
        """ overload create_session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(
                user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session id """
        if not session_id:
            return None

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if created_at + timedelta(seconds=self.session_duration) <\
                datetime.nou():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroy session """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        user_session.remove()
        return True
