# bot_runner.py
from control_emu.port_connector import connect_and_list_devices
from control_emu.bot_instance import Bot
import threading
import time

def run_all_bots():
    devices = connect_and_list_devices()
    print(f"🟢 Połączono z {len(devices)} emulatorami.")

    for device in devices:
        bot = Bot(device)
        threading.Thread(target=bot.run, daemon=True).start()
        time.sleep(60)

if __name__ == "__main__":
    run_all_bots()
    while True:
        time.sleep(1)
