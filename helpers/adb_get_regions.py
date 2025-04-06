# helpers/adn_get_region.py
import subprocess
import numpy as np
import cv2

def adb_screencap_and_select_region(device_id):
    subprocess.run(["adb", "connect", device_id],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = subprocess.run([
        "adb", "-s", device_id,
        "exec-out", "screencap", "-p"
    ], capture_output=True)

    img = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        print(f"❌ Nie udało się pobrać zrzutu z {device_id}.")
        return None

    region = []
    drawing = False
    start_point = (0, 0)

    def on_mouse(event, x, y, flags, param):
        nonlocal drawing, start_point, region
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            temp_img = img.copy()
            cv2.rectangle(temp_img, start_point, (x, y), (0, 255, 0), 2)
            cv2.imshow("Zaznacz region", temp_img)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x1, y1 = start_point
            x2, y2 = x, y
            x, y = min(x1, x2), min(y1, y2)
            w, h = abs(x1 - x2), abs(y1 - y2)
            region = [x, y, w, h]
            cv2.destroyAllWindows()

    cv2.imshow("Zaznacz region", img)
    cv2.setMouseCallback("Zaznacz region", on_mouse)
    cv2.waitKey(0)

    if region:
        print(f"✅ Wybrany region: {tuple(region)}")
        return tuple(region)
    else:
        print("❌ Nie wybrano regionu.")
        return None

# Przykład użycia
if __name__ == "__main__":
    adb_screencap_and_select_region("127.0.0.1:5555")
