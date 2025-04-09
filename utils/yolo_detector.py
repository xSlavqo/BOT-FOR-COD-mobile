# utils/yolo_detector.py
import cv2
import numpy as np
from ultralytics import YOLO

def screencap(device):
    return device.screencap()

def detect_with_yolo(device, model_path, region=None, conf=0.5):
    screen = screencap(device)
    img = cv2.imdecode(np.frombuffer(screen, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return False, 0.0

    if region:
        x, y, w, h = region
        img = img[y:y+h, x:x+w]
        if img.size == 0:
            return False, 0.0

    model = YOLO(model_path)
    results = model.predict(source=img, imgsz=736, conf=conf, verbose=False)

    for r in results:
        if len(r.boxes) > 0:
            best_conf = float(r.boxes.conf.max())  # największy score z wykrytych boxów
            return True, best_conf
    return False, 0.0


# Przykład testowy:
if __name__ == "__main__":
    class DummyDevice:
        def screencap(self):
            import subprocess
            return subprocess.run(
                ["adb", "-s", "127.0.0.1:5555", "exec-out", "screencap", "-p"],
                capture_output=True
            ).stdout

    MODEL_PATH = "runs/detect/train2/weights/best.pt"
    REGION = (1239, 272, 39, 96)

    device = DummyDevice()
    is_visible, confidence = detect_with_yolo(device, MODEL_PATH)

    if is_visible:
        print(f"✅ Obiekt widoczny (confidence: {round(confidence, 3)})")
    else:
        print("❌ Obiekt niewidoczny")
