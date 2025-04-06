# utils/helpers/adb_screencap.py
import subprocess
import numpy as np
import cv2
from datetime import datetime

def adb_screencap(device_id):
    # 🔄 Spróbuj się połączyć, jeśli nie jesteś połączony
    subprocess.run(["adb", "connect", device_id],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = subprocess.run([
        "adb", "-s", device_id,
        "exec-out", "screencap", "-p"
    ], capture_output=True)

    img = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)

    if img is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{device_id.replace(':', '_')}_{timestamp}.png"
        cv2.imwrite(filename, img)
        print(f"📸 Zapisano zrzut: {filename}")
        return filename
    else:
        print(f"❌ Nie udało się pobrać zrzutu z {device_id}.")
        return None

if __name__ == "__main__":
    adb_screencap("127.0.0.1:5555")
