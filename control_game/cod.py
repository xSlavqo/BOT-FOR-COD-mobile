# control_game/cod.py

import time

def launch_cod(device):
    package = "com.farlightgames.samo.gp"
    activity = "com.harry.engine.MainActivity"
    device.shell(f"am start -n {package}/{activity}")

def close_cod(device):
    package = "com.farlightgames.samo.gp"
    device.shell(f"am force-stop {package}")

def restart_cod(device, wait_time=3):
    close_cod(device)
    time.sleep(wait_time)
    launch_cod(device)

def is_cod_running(device):
    package = "com.farlightgames.samo.gp"
    output = device.shell("dumpsys window windows | grep mCurrentFocus")
    return package in output