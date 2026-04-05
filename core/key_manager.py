# key_manager.py
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100000

def generate_salt():
    return os.urandom(SALT_SIZE)

def derive_key(password, salt):
    key = PBKDF2(
        password,
        salt,
        dkLen=KEY_SIZE,
        count=ITERATIONS,
        hmac_hash_module=SHA256
    )
    return key