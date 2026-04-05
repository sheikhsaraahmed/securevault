# encryptor.py
import os
import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from core.key_manager import generate_salt, derive_key

IV_SIZE = 16

def encrypt_file(input_path, output_path, password):
    try:
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        salt = generate_salt()
        iv = os.urandom(IV_SIZE)
        key = derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        hmac_value = hmac.new(key, salt + iv + ciphertext, hashlib.sha256).digest()
        with open(output_path, 'wb') as f:
            f.write(hmac_value)
            f.write(salt)
            f.write(iv)
            f.write(ciphertext)
        return True
    except Exception as e:
        print(f"Encryption error: {e}")
        return False