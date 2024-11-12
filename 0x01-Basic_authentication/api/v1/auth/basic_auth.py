#!/usr/bin/env python3
""" inherit from Auth class """


import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ returns the Base64 part of the Authorization header """
        if not isinstance(authorization_header, str):
            return None
        if authorization_header is None:
            return None

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0] != 'Basic':
            return None

        return parts[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ eturns the user email and password """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)
