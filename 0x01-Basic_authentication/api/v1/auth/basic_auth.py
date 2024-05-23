#!/usr/bin/env python3
"""
This module defines authentication class
"""
from api.v1.auth.auth import Auth
import re
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """class definition here"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extracts the hashed auth string"""
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not re.match('^Basic ', authorization_header):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the encoded string"""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extracting user credentials"""
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Recreates user object from credentials"""
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        if not User.all():
            return None
        user_x = None
        try:
            user_x = User.search({"email": user_email})
        except Exception:
            return None
        if not user_x or len(user_x) > 1:
            return None
        if not user_x[0].is_valid_password(user_pwd):
            return None
        return user_x[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        auth_header = self.authorization_header(request)
        auth_header64 = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(auth_header64)
        decod_str = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(decod_str[0], decod_str[1])
