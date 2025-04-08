# utils/yolo_detector.py
import cv2
import numpy as np
from ultralytics import YOLO


def screencap(device):
    result = device.screencap()
    return result


def detect_with_yolo(device, model_path, region, conf=0.5) -> bool:
    screen = screencap(device)
    img = cv2.imdecode(np.frombuffer(screen, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return False

    x, y, w, h = region
    img = img[y:y+h, x:x+w]
    if img.size == 0:
        return False

    model = YOLO(model_path)
    results = model.predict(source=img, imgsz=64, conf=conf, verbose=False)
    for r in results:
        if len(r.boxes) > 0:
            return True
    return False


if __name__ == "__main__":
    class DummyDevice:
        def screencap(self):
            import subprocess
            return subprocess.run(
                ["adb", "-s", "127.0.0.1:5555", "exec-out", "screencap", "-p"],
                capture_output=True
            ).stdout

    REGION = (1244, 302, 36, 38)
    MODEL_PATH = "models/legions_menu.pt"
    device = DummyDevice()
    if detect_with_yolo(device, MODEL_PATH, REGION):
        print("✅ Obiekt widoczny")
    else:
        print("❌ Obiekt niewidoczny")
