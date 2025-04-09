# yolo_dataset_builder/visible.py
import os
import cv2
import numpy as np
import time
from datetime import datetime
from ppadb.client import Client as AdbClient

TEMPLATE_PATH = "test.png"  # <- zmień na swój wzorzec
SAVE_DIR = "datasets/visible"              # <- katalog do zapisu
DEVICE_ID = "127.0.0.1:5555"
MARGIN = 20  # ile pikseli dodać w każdą stronę

def connect_device(device_id):
    client = AdbClient(host="127.0.0.1", port=5037)
    return client.device(device_id)

def capture_similar_to_template(device, template_path, margin=40):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print("❌ Nie można wczytać wzorca.")
        return

    screen_bytes = device.screencap()
    screen = cv2.imdecode(np.frombuffer(screen_bytes, np.uint8), cv2.IMREAD_COLOR)
    if screen is None:
        print("❌ Nie można pobrać zrzutu.")
        return

    base = template[:, :, :3] if template.shape[2] == 4 else template
    method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(screen, base, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    match_x, match_y = max_loc
    h, w = base.shape[:2]

    x1 = max(match_x - margin, 0)
    y1 = max(match_y - margin, 0)
    x2 = min(match_x + w + margin, screen.shape[1])
    y2 = min(match_y + h + margin, screen.shape[0])

    region = screen[y1:y2, x1:x2]
    os.makedirs(SAVE_DIR, exist_ok=True)
    filename = f"{SAVE_DIR}/found_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    cv2.imwrite(filename, region)
    print(f"✅ Zapisano: {filename} (score: {round(max_val, 3)})")

if __name__ == "__main__":
    device = connect_device(DEVICE_ID)
    capture_similar_to_template(device, TEMPLATE_PATH, MARGIN)
