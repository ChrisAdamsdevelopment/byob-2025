from Crypto.Cipher import AES
import base64, os

KEY = b'32_byte_key_placeholder_123456789012'
IV = os.urandom(16)

def aes_encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    return base64.b64encode(IV + cipher.encrypt(data))

def aes_decrypt(data):
    raw = base64.b64decode(data)
    cipher = AES.new(KEY, AES.MODE_CFB, raw[:16])
    return cipher.decrypt(raw[16:])
