# helpers/is_legion_menu_visible.py
import cv2
import numpy as np

def is_legion_menu_visible(device):
    img_bytes = device.screencap()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return False

    # Przytnij tylko fragment gdzie pojawia się przycisk (dostosuj jeśli trzeba)
    x, y, w, h = 1167, 238, 111, 183
    roi = img[y:y+h, x:x+w]

    # Konwersja do odcieni szarości + rozmycie
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detekcja krawędzi
    edges = cv2.Canny(blurred, 50, 150)

    # Znajdź kontury
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtruj kontury: szukamy poziomych kresek
    horizontal_lines = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if aspect_ratio > 5 and 5 < w < 120 and 3 < h < 15:
            horizontal_lines += 1

    return horizontal_lines >= 3

if __name__ == "__main__":
    from ppadb.client import Client as AdbClient
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("127.0.0.1:5555")
    print("Widoczne:", is_legion_menu_visible(device))
