#!/usr/bin/env python3
"""
This module defines authentication class
"""
from api.v1.auth.auth import Auth
import re


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
