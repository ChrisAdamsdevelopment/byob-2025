import os, time

def anti_vm_check():
    processes = ['vbox', 'vmware', 'xen']
    for proc in processes:
        if proc in os.popen("ps aux").read().lower():
            return False
    time.sleep(3)
    return True
