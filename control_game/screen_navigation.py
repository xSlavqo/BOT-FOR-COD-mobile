# control_game/screen_navigation.py

import time
from utils.locate_adb import locate

def press_key(device, key):
    mapping = {
        "esc": "KEYCODE_ESCAPE",
        "space": "KEYCODE_SPACE",
        "o": "KEYCODE_O"
    }
    if key in mapping:
        device.shell(f"input keyevent {mapping[key]}")
        time.sleep(0.8)

def check_and_navigate(device, target_image, alt_image, attempts=0):
    max_attempts = 5

    if locate(device, target_image, 0.99, 3):
        return True
    elif locate(device, alt_image, 0.99, 3, click_center=True):
        time.sleep(2)
        return locate(device, target_image, 0.99, 5)
    else:
        if attempts < max_attempts:
            press_key(device, "esc")
            return check_and_navigate(device, target_image, alt_image, attempts + 1)
        else:
            print(f"[{device.serial}] Nie można odnaleźć widoku {target_image}")
            return False


def city(device):
    return check_and_navigate(device, "png/city.png", "png/map.png")

def map(device):
    return check_and_navigate(device, "png/map.png", "png/city.png")

def main_screen(device):
    escape_attempts = 0
    max_esc_presses = 10
    while not (locate(device, "png/map.png", 0.99, 3) or locate(device, "png/city.png", 0.99, 3)):
        if escape_attempts >= max_esc_presses:
            print(f"[{device.serial}] Nie można odnaleźć main_screen")
            return False
        press_key(device, "esc")
        escape_attempts += 1
    return True

def ally_menu(device):
    if locate(device, "png/ally_menu.png", 0.99, 3):
        return True
    else:
        main_screen(device)
        press_key(device, "o")
        return locate(device, "png/ally_menu.png", 0.99, 3)
