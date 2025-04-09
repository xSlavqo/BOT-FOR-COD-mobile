# port_connector.py
import subprocess
from ppadb.client import Client as AdbClient

PORTS = [5555, 5585, 6666]  # <-- uzupełniasz jak chcesz

def connect_and_list_devices():
    connected = []

    for port in PORTS:
        device_id = f"127.0.0.1:{port}"
        subprocess.run(["adb", "connect", device_id],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # teraz pobierz listę aktywnych
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    for device in devices:
        if device.serial.startswith("127.0.0.1:") and int(device.serial.split(":")[1]) in PORTS:
            connected.append(device)

    return connected
