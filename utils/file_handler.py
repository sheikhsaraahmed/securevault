import os

ENCRYPTED_FOLDER = "encrypted_files"

def get_output_encrypt_path(input_path):
    filename = os.path.basename(input_path)
    return os.path.join(ENCRYPTED_FOLDER, filename + ".enc")

def get_output_decrypt_path(input_path):
    filename = os.path.basename(input_path)
    if filename.endswith(".enc"):
        original_name = filename[:-4]
    else:
        original_name = filename
    name, ext = os.path.splitext(original_name)
    safe_name = name + "_decrypted" + ext
    return os.path.join(ENCRYPTED_FOLDER, safe_name)

def file_exists(path):
    return os.path.isfile(path)