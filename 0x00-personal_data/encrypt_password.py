#!/usr/bin/env python3
"""Hashes passwords."""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes passwords."""
    return (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks hashed password."""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return (True)
    else:
        return (False)
