# 💀 OBLIVION
**Full-Spectrum Post-Exploitation & Payload Orchestration Framework**

---

OBLIVION is a modular, stealth-focused offensive security suite designed for red team operations, adversary emulation, and payload delivery automation. Built for maximum flexibility and evasion, it offers polymorphic stagers, encrypted payloads, in-memory loaders, and a real-time WebSocket C2 infrastructure.



## ⚔️ Capabilities

### 🛠️ Payload Forge Engine
- Obfuscates & mutates Python/C2 stubs at build time
- Embeds AES-encrypted payloads inside decoy installers
- Supports EXE, DLL, shellcode, HTA, and PowerShell formats

### 🎭 Fake Installer Dropper Generator
- Builds decoy installers (Chrome, VPN, VLC, Windows Update)
- PyQt5-based GUI triggers in-memory execution of encoded shellcode
- Installer generation is automated and polymorphic

### 📡 Command & Control Infrastructure
- FastAPI WebSocket C2 with full-duplex encrypted control
- Live shell terminal (WebSocket-powered)
- Task queuing and plugin deployment interface
- Domain fronting reverse proxy with configurable SNI spoofing

### 🧩 Offensive Plugins
- `keylogger.py` — keystroke capture with dynamic flushing  
- `screen_capture.py` — base64 PNG snapshots  
- `clipboard_hijacker.py` — crypto wallet swapper  
- `ransomware.py` — AES+RSA hybrid file locker  
- `browser_cred_stealer.py` — Chrome credential DB dumper  

### 🧬 Persistence Modules
- **Windows**: Registry keys, AppData copy, scheduled tasks  
- **Linux**: `~/.bashrc` hooks, systemd autostart  

### 👻 Evasion Techniques
- In-memory loaders via `ctypes`, `CreateThread`, and `VirtualAlloc`
- AMSI & ETW bypasses with syscall patching
- Randomized identifier mutation + junk logic injection
- Fileless HTA/Powershell delivery vectors (`mshta.exe` support)

## 🗂️ Project Structure



OBLIVION/
├── builder/           
### Payload forge, obfuscator, mutator

├── c2/                
### FastAPI C2 server, WebSocket manager

├── client/            
### Stager stubs, plugin code

├── stager/            
### PyQt5 decoy installers, HTA generator

├── forge_panel/       
### Web-based payload builder UI

├── utils/             
### AES, evasion, and memory execution helpers

├── build/             
### Auto-generated payloads

└── README.md



## 🚀 Quick Start

### 🔧 Set Up the Environment



```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

```bash
python3 builder/campaign_builder.py

```

```bash
python3 c2/server.py

```

```bash
cd forge_panel
python3 app.py

```

Then open your browser and go to:
http://localhost:8081/

🧠 Usage Highlights
Generate encrypted shellcode and wrap it in fake installers

Execute payloads in-memory using PyQt5 or HTA dropper

View live bot telemetry and run commands via WebSocket shell

Automate campaigns with branding, persistence, and task injection

Front traffic through CDN (e.g. Cloudflare, GCP, Azure) for stealth ops

⚠️ Legal Disclaimer
This project is intended for authorized red teaming, penetration testing, and educational research purposes only.
Unauthorized access to systems you do not own or have explicit written permission to test is illegal.

You are solely responsible for your actions. Use responsibly.

🧬 Author Statement
OBLIVION is a product of offensive R&D. It exists to train, test, and protect against the evolving threat landscape.

If your blue team can stop this, your infrastructure is hardened.
If your red team can wield this, your simulation is real.

“Welcome to the black mirror of modern cyber warfare. Welcome to OBLIVION.”
