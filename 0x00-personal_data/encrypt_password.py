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
