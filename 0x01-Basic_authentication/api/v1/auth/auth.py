#!/usr/bin/env python3
"""
This module defines authentication class
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """class definition here"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication method"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authentication header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
