# helpers/adn_get_coords.py
import subprocess
import numpy as np
import cv2

def adb_screencap_and_click(device_id):
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

    coords = []

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coords.append((x, y))
            cv2.destroyAllWindows()

    cv2.imshow("Kliknij punkt na ekranie", img)
    cv2.setMouseCallback("Kliknij punkt na ekranie", on_mouse)
    cv2.waitKey(0)

    if coords:
        print(f"✅ Koordynaty kliknięcia: {coords[0]}")
        return coords[0]
    else:
        print("❌ Nie wybrano punktu.")
        return None

# Przykład użycia
if __name__ == "__main__":
    adb_screencap_and_click("127.0.0.1:5555")
