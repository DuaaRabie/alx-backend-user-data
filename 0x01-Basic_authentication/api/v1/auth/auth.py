#!/usr/bin/env python3
""" task3: Auth class to manage the API auth """


from flask import request
from typing import List, TypeVar


class Auth:
    """ a class to manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth
        Return:
            False - path and excluded_paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization header
        Return: None - request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user
        Return: None - request"
        return "None - request"
        """
        return None
