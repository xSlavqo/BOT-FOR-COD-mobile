# yolo_dataset_builder/device_capture.py
import os
import cv2
import numpy as np
import time
from datetime import datetime
from ppadb.client import Client as AdbClient

REGION = (1244, 302, 36, 38)  # (x, y, w, h)
SAVE_DIR = "datasets/invisible"  # lub zmień na "datasets/invisible"
DEVICE_ID = "127.0.0.1:5555"

def connect_device(device_id):
    client = AdbClient(host="127.0.0.1", port=5037)
    return client.device(device_id)

def capture_region(device):
    img_bytes = device.screencap()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return None
    x, y, w, h = REGION
    return img[y:y+h, x:x+w]

def run_capture_loop(device):
    os.makedirs(SAVE_DIR, exist_ok=True)
    count = 0
    while True:
        region_img = capture_region(device)
        if region_img is not None:
            filename = f"{SAVE_DIR}/region_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(filename, region_img)
            print(f"✅ Zapisano: {filename}")
            count += 1
        time.sleep(1)

if __name__ == "__main__":
    device = connect_device(DEVICE_ID)
    run_capture_loop(device)
