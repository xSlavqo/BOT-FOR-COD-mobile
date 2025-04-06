# control_game/cod.py
def launch_cod(device):
    package = "com.farlightgames.samo.gp"
    activity = "com.harry.engine.MainActivity"
    device.shell(f"am start -n {package}/{activity}")
