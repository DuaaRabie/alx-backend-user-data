#!/usr/bin/env python3
""" inherit from Auth class """


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """
    def extract_base64_authorization_header(self, authorization_header: str)\
        -> str:
        """ returns the Base64 part of the Authorization header """
        if not isinstance(authorization_header, str):
            return None
        if authorization_header is None:
            return None

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0] != 'Basic':
            return None

        return parts[1]
