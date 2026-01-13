import os
import hashlib
import hmac
import base64

# Configuration
HASH_NAME = "sha256"
ITERATIONS = 200_000
SALT_SIZE = 16  # bytes


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC.
    Returns a string you can safely store in DB.
    """
    salt = os.urandom(SALT_SIZE)

    pwd_hash = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    # store: iterations$salt$hash (base64 encoded)
    return f"{ITERATIONS}$" \
           f"{base64.b64encode(salt).decode()}$" \
           f"{base64.b64encode(pwd_hash).decode()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against stored hash.
    """
    iterations, salt_b64, hash_b64 = stored_hash.split("$")

    salt = base64.b64decode(salt_b64)
    stored_pwd_hash = base64.b64decode(hash_b64)

    pwd_hash = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        int(iterations)
    )

    # constant-time comparison (prevents timing attacks)
    return hmac.compare_digest(pwd_hash, stored_pwd_hash)
