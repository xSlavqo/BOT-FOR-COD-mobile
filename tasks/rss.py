# tasks/rss.py

import random
from tasks.legions_menu import legions_menu
from control_game.screen_navigation import map
from utils.click_point import click_point
from utils.locate_adb import locate

def rss(device):
    if legions_menu(device):
        return True

    if not map(device):
        return False

    click_options = [
        (432, 656),
        (638, 652)
    ]

    for _ in range(2):
        click_point(device, 54, 569)

        random_point = random.choice(click_options)
        click_point(device, *random_point)

        locate(device, "png/gather1.png", threshold=0.98, max_time=5, click_center=True)

        click_point(device, 639, 365)

        locate(device, "png/gather2.png", threshold=0.98, max_time=5, click_center=True)
        locate(device, "png/gather3.png", threshold=0.98, max_time=5, click_center=True)
        locate(device, "png/gather4.png", threshold=0.98, max_time=5, click_center=True)

        if not map(device):
            return False

    return True
