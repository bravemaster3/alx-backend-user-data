#!/usr/bin/env python3
"""
This module defines authentication class
"""
from api.v1.auth.auth import Auth
import re
import base64
from typing import Tuple


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
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """extracting user credentials"""
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if not ':' in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))
