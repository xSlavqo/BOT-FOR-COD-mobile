# utils/helpers/adb_locate_debug.py
import cv2
import numpy as np
import subprocess

def screencap(device_id):
    subprocess.run(["adb", "connect", device_id],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = subprocess.run([
        "adb", "-s", device_id,
        "exec-out", "screencap", "-p"
    ], capture_output=True)
    return cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)

def is_image_match(img, template):
    base = template[:, :, :3]
    mask = cv2.merge([template[:, :, 3]] * 3)
    result = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

def adb_locate_preview(device_id, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"❌ Nie znaleziono szablonu: {template_path}")
        return False

    screen = screencap(device_id)
    if screen is None:
        print(f"❌ Nie udało się pobrać screencapu z {device_id}")
        return False

    max_val, top_left = is_image_match(screen, template)
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])

    cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)
    print(f"🎯 Dopasowanie: {max_val * 100:.2f}%")
    print(f"📍 Pozycja: {top_left}")

    cv2.imshow("Najlepsze dopasowanie", screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    adb_locate_preview("127.0.0.1:5585", "pngs/city.png")
