# utils/locate_adb.py
import cv2
import numpy as np
import time
import random

def screencap(device):
    img_bytes = device.screencap()
    return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

def is_image_match(img, template, threshold):
    if template.shape[2] == 4:
        base = template[:, :, :3]
        alpha_mask = cv2.merge([template[:, :, 3]] * 3)
        correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    else:
        correlation = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)

    max_val = correlation.max()
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches, max_val

def locate(device, template_path, threshold=0.99, max_time=5, click_center=False):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"❌ Nie znaleziono szablonu: {template_path}")
        return False

    start = time.time()

    while time.time() - start < max_time:
        img = screencap(device)
        if img is None:
            continue

        matches, _ = is_image_match(img, template, threshold)
        if matches:
            if click_center:
                match_x, match_y = matches[0]
                w, h = template.shape[1], template.shape[0]

                center_x = match_x + w // 2
                center_y = match_y + h // 2

                offset_x = int(random.uniform(-0.25, 0.25) * w)
                offset_y = int(random.uniform(-0.25, 0.25) * h)

                final_x = center_x + offset_x
                final_y = center_y + offset_y

                time.sleep(random.uniform(0.4, 2.2))
                device.shell(f"input tap {final_x} {final_y}")
                time.sleep(random.uniform(0.6, 2))
            return True

    return False
