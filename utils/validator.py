import os
import sys

MAX_ATTEMPTS = 3
failed_attempts = 0

def validate_file_for_encryption(path):
    if not os.path.isfile(path):
        return False
    if path.endswith(".enc"):
        return False
    return True

def validate_file_for_decryption(path):
    if not os.path.isfile(path):
        return False
    if not path.endswith(".enc"):
        return False
    return True

def validate_password(password):
    if not password.strip():
        return False
    return True

def check_attempts():
    global failed_attempts
    failed_attempts += 1
    remaining = MAX_ATTEMPTS - failed_attempts
    if failed_attempts >= MAX_ATTEMPTS:
        print("\n  [X] Too many wrong attempts. Exiting for security.")
        sys.exit(1)
    else:
        print(f"  [!] {remaining} attempt(s) remaining before lockout.")

def reset_attempts():
    global failed_attempts
    failed_attempts = 0