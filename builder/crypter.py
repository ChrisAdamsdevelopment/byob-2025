from utils.encryption import aes_encrypt

def encrypt_payload(code):
    return aes_encrypt(code.encode('utf-8')).decode()
