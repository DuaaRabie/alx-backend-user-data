#!/usr/bin/env python3
"""
hashing passwords
"""
import bcrypt
import uuid
from db import DB
from db import User


def _hash_password(password: str) -> bytes:
    """
    To salted hah the input password
    Args:
        password: Password to hash.
    Returns:
        bytes: the salted hash of the password.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    returns a string representation of new uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user.
        Args:
            email: user email to register
            password: user password to register
        Returns:
            new_user: registered user
        Raises:
            ValueError: User <user's email> already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except ValueError:
            raise
        except Exception:
            hashed_password = _hash_password(password)
            hp_str = hashed_password.decode('utf-8')
            new_user = self._db.add_user(email, hp_str)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Determine the valid login
        Args:
            email: user's email want to login
            password: user's password
        Returns:
            Boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password.encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """return session ID"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ returns user from session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int):
        """ Destroy session
        """
        user = self._db.find_user_by(user_id=user_id)
        user.session_id = None
