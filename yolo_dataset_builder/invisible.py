# yolo_dataset_builder/invisible.py

import os
import cv2
import numpy as np
import random
import time
from datetime import datetime
from ppadb.client import Client as AdbClient

TEMPLATE_PATH = "test.png"
SAVE_DIR = "datasets/invisible"
DEVICE_ID = "127.0.0.1:5555"
MARGIN = 20
SAMPLES = 30

def connect_device(device_id):
    client = AdbClient(host="127.0.0.1", port=5037)
    return client.device(device_id)

def get_template_and_match_area(screen, template_path, margin):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print("❌ Nie można wczytać wzorca.")
        return None, None

    base = template[:, :, :3] if template.shape[2] == 4 else template
    method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(screen, base, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    match_x, match_y = max_loc
    h, w = base.shape[:2]

    crop_w = w + margin * 2
    crop_h = h + margin * 2

    avoid_area = (
        max(match_x - margin, 0),
        max(match_y - margin, 0),
        min(match_x + w + margin, screen.shape[1]),
        min(match_y + h + margin, screen.shape[0])
    )

    return (crop_w, crop_h), avoid_area

def does_overlap(x, y, crop_w, crop_h, avoid_area):
    ax1, ay1, ax2, ay2 = avoid_area
    bx1, by1 = x, y
    bx2, by2 = x + crop_w, y + crop_h

    return not (bx2 < ax1 or bx1 > ax2 or by2 < ay1 or by1 > ay2)

def generate_invisible_samples(device, template_path, margin=20, samples=30):
    screen_bytes = device.screencap()
    screen = cv2.imdecode(np.frombuffer(screen_bytes, np.uint8), cv2.IMREAD_COLOR)
    if screen is None:
        print("❌ Nie można pobrać zrzutu.")
        return

    (crop_w, crop_h), avoid_area = get_template_and_match_area(screen, template_path, margin)
    if crop_w is None:
        return

    screen_h, screen_w = screen.shape[:2]
    os.makedirs(SAVE_DIR, exist_ok=True)

    count = 0
    attempts = 0
    max_attempts = samples * 10  # żeby nie zaciąć się w pętli

    while count < samples and attempts < max_attempts:
        x = random.randint(0, screen_w - crop_w)
        y = random.randint(0, screen_h - crop_h)

        if does_overlap(x, y, crop_w, crop_h, avoid_area):
            attempts += 1
            continue

        crop = screen[y:y+crop_h, x:x+crop_w]
        filename = f"{SAVE_DIR}/inv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        cv2.imwrite(filename, crop)
        print(f"✅ Zapisano: {filename}")
        count += 1
        attempts += 1

if __name__ == "__main__":
    device = connect_device(DEVICE_ID)
    generate_invisible_samples(device, TEMPLATE_PATH, MARGIN, SAMPLES)
