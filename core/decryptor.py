import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from core.key_manager import derive_key

HMAC_SIZE = 32
SALT_SIZE = 16
IV_SIZE = 16

def decrypt_file(input_path, output_path, password):
    try:
        with open(input_path, 'rb') as f:
            file_data = f.read()
        hmac_stored = file_data[:HMAC_SIZE]
        salt = file_data[HMAC_SIZE:HMAC_SIZE+SALT_SIZE]
        iv = file_data[HMAC_SIZE+SALT_SIZE:HMAC_SIZE+SALT_SIZE+IV_SIZE]
        ciphertext = file_data[HMAC_SIZE+SALT_SIZE+IV_SIZE:]
        key = derive_key(password, salt)
        hmac_calc = hmac.new(key, salt+iv+ciphertext, hashlib.sha256).digest()
        if not hmac.compare_digest(hmac_stored, hmac_calc):
            return False
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        return True
    except ValueError:
        return False
    except Exception as e:
        print(f"  [!] Decryption error: {e}")
        return False