# utils/click_point.py

import random
import time

def click_point(device, x, y, offset=10):
    dx = random.randint(-offset, offset)
    dy = random.randint(-offset, offset)
    time.sleep(random.uniform(0.3, 0.7))
    device.shell(f"input tap {x + dx} {y + dy}")
    time.sleep(random.uniform(0.2, 0.5))
