#!/usr/bin/env python3
"""
This module defines authentication class
"""
from flask import request
from typing import List, TypeVar
import re


class Auth():
    """class definition here"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication method"""
        if path:
            n_path = path.rstrip('/')
        if excluded_paths:
            n_excluded_paths = [p.rstrip('/') for p in excluded_paths]
        # if not excluded_paths or not path or n_path not in n_excluded_paths:
        if not excluded_paths or not path:
            return True
        matched = False
        for p in n_excluded_paths:
            matched += re.match(p, path)
        if not matched:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Authentication header"""
        if not request or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
