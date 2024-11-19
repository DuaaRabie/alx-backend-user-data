#!/usr/bin/env python3
"""
hashing passwords
"""
import bcrypt
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
        except Exception:
            hashed_password = _hash_password(password)
            hp_str = hashed_password.decode('utf-8')
            new_user = self._db.add_user(email, hp_str)
            return new_user
