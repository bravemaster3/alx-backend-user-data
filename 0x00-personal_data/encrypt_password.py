#!/usr/bin/env python3
"""
Encryption function
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password with a salt."""
    # Generate a random salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
