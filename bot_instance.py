# bot_instance.py
import logging
import traceback
import time
import os
from ppadb.device import Device
from ppadb.client import Client as AdbClient
from utils.is_element_visible import is_element_visible
from utils.click_point import click_point

class Bot:
    def __init__(self, device: Device):
        self.device = device
        self.name = device.serial
        self.setup_logger()

    def setup_logger(self):
        os.makedirs("logs", exist_ok=True)
        log_filename = self.name.replace(":", "_") + ".log"
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.ERROR)
        handler = logging.FileHandler(f"logs/{log_filename}")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def reconnect_device(self):
        print(f"🔌 [{self.name}] Próba ponownego połączenia...")
        while True:
            try:
                client = AdbClient(host="127.0.0.1", port=5037)  # lub 5038 dla BlueStacks
                client.remote_connect(*self.name.split(":"))
                self.device = client.device(self.name)
                if self.device is not None:
                    print(f"✅ [{self.name}] Połączono ponownie.")
                    break
            except Exception as e:
                self.logger.error(f"[{self.name}] Błąd reconnect: {e}")
            time.sleep(60)

    def run(self):
        print(f"▶ Bot uruchomiony na {self.name}")
        REGION = (1244, 302, 36, 38)
        MODEL_PATH = "models/legions_menu.pt"

        while True:
            try:
                visible = is_element_visible(self.device, MODEL_PATH, REGION)
                if visible:
                    print(f"👁️ [{self.name}] Legions menu widoczne")
                else:
                    print(f"🚫 [{self.name}] Legions menu niewidoczne")

                time.sleep(5)

            except ConnectionError:
                print(f"⚠️ [{self.name}] Utracono połączenie – reconnect...")
                self.logger.error(f"[{self.name}] Utracono połączenie.")
                self.reconnect_device()

            except Exception:
                self.logger.error(
                    f"[{self.name}] Nieobsłużony błąd:\n{traceback.format_exc()}"
                )
                print(f"❌ [{self.name}] Błąd krytyczny – bot zatrzymany.")
                break
