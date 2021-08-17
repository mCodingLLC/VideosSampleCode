import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Callable

import pytest


class AuthenticationError(Exception):
    pass


"""Plaintext"""


def update_password_plaintext(db, user, password: str) -> None:
    user.password = password
    db.store(user)


def verify_password_plaintext(user, password: str) -> None:
    pw = user.password
    if not hmac.compare_digest(pw, password):
        raise AuthenticationError


"""Hashed"""


def hash_name(hash_fn: Callable[[bytes], bytes]) -> str:
    if hash_fn.name == "blake2b":
        return "blake2b"
    raise ValueError


def hash_from_name(name: str) -> Callable[[bytes], bytes]:
    if name == "blake2b":
        def hash_fn(b: bytes) -> bytes:
            return hashlib.blake2b(b).digest()

        hash_fn.name = "blake2b"
        return hash_fn
    raise ValueError


def hash_str_and_b64_encode(hash_fn: Callable[[bytes], bytes], password: str) -> str:
    pw_bytes = password.encode("utf-8")
    hash_bytes = hash_fn(pw_bytes)
    hash_bytes = base64.b64encode(hash_bytes)
    hashed_password = hash_bytes.decode("ascii")
    return hashed_password


def update_password_hashed(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    hashed_password = hash_str_and_b64_encode(hash_fn, password)
    name = hash_name(hash_fn)
    user.password = f"{name}${hashed_password}"
    db.store(user)


def verify_password_hashed(user, password: str) -> None:
    hash_fn_name, hashed_password = user.password.split("$")
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


"""Hashed and salted"""


def gen_salt() -> str:
    return secrets.token_urlsafe(20)


def update_password_hashed_salted(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    salt = gen_salt()
    hashed_password = hash_str_and_b64_encode(hash_fn, salt + password)
    name = hash_name(hash_fn)
    user.password = f"{name}${salt}${hashed_password}"
    db.store(user)


def verify_password_hashed_salted(user, password: str) -> None:
    hash_fn_name, salt, hashed_password = user.password.split("$")
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, salt + password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


"""Hashed, salted, and peppered"""


def get_global_pepper() -> str:
    """
    Get the global secret pepper from secure memory.
    The important thing is that it is NOT stored in the database.
    """
    return "subscribe to mcoding YSkkYFGRzdqNLCy68z0uT0kjZQgxh6-vzTH_dw7NirYPqDhcU3ykSlG0O-AAx65ivIbx1FPrukM3K4rNSFbcpg"


def update_password_hashed_salted_peppered(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    salt = gen_salt()
    pepper = get_global_pepper()
    hashed_password = hash_str_and_b64_encode(hash_fn, pepper + salt + password)
    name = hash_name(hash_fn)
    user.password = f"{name}${salt}${hashed_password}"
    db.store(user)


def verify_password_hashed_salted_peppered(user, password: str) -> None:
    hash_fn_name, salt, hashed_password = user.password.split("$")
    pepper = get_global_pepper()
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, pepper + salt + password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


def real_life():
    """
    Do not use any of this code in real life.
    Do not write your own hash function.
    Don't even write your own authentication code if you don't have to (use a well-proven library).

    According to the Open Web Application Security Project (OWASP) you should:
    Use Argon2id if you can.
    Else use bcrypt if you can.
    Else use scrypt if you can (for legacy systems).
    Else use PBKDF2 with HMAC-SHA-256 (for FIPS-140 compliance).
    """


def main():
    class LolDB:
        def __init__(self):
            self.user = None

        def store(self, user):
            self.user = user
            print("storing user:")
            print(f"{user.email=}")
            print(f"{user.password=}")
            print()

    @dataclass
    class User:
        email: str
        password: str

    user = User(email="user@example.com", password="")
    db = LolDB()
    hash_fn = hash_from_name("blake2b")

    print("plaintext")
    update_password_plaintext(db, user, "v3ry s3cur3")
    verify_password_plaintext(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_plaintext(user, "incorrect pass")

    print("hashed")
    update_password_hashed(db, user, hash_fn, "v3ry s3cur3")
    verify_password_hashed(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_hashed(user, "incorrect pass")

    print("hashed+salted")
    update_password_hashed_salted(db, user, hash_fn, "v3ry s3cur3")
    verify_password_hashed_salted(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_hashed_salted(user, "incorrect pass")

    print("hashed+salted+peppered")
    update_password_hashed_salted_peppered(db, user, hash_fn, "v3ry s3cur3")
    verify_password_hashed_salted_peppered(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_hashed_salted_peppered(user, "incorrect pass")


if __name__ == '__main__':
    main()
