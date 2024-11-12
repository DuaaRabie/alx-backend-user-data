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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path in excluded_paths:
            return False

        for excluded in excluded_paths:
            if excluded.endswith('*'):
                if path.startswith(excluded[:-1]):
                    return False
            elif excluded.endswith('/'):
                if path.startswith(excluded):
                    return False
            elif path == excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header
        Return: None - request
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user
        Return: None - request"
        return "None - request"
        """
        return None
