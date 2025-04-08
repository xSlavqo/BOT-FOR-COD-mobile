#tasks/legions_menu

from control_game.screen_navigation import city, map, main_screen
from utils.yolo_detector import detect_with_yolo

def legions_menu(device):
    if not main_screen(device):
        return False
    
    model_path = "models/legions_menu.pt"
    region = (1239, 272, 39, 96)
    return detect_with_yolo(device, model_path, region)
