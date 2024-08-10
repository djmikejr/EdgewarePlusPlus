import subprocess
from pathlib import Path

import vlc  # TODO: May fail
from utils.linux_utils import get_desktop_environment, get_wallpaper_commands, set_wallpaper_special_cases


def set_wallpaper(wallpaper: Path) -> None:
    global first_run
    if "first_run" not in globals():
        first_run = True

    desktop = get_desktop_environment()
    commands = get_wallpaper_commands(wallpaper, desktop)
    for command in commands:
        try:
            args = command % wallpaper
        except Exception:
            args = command

        try:
            subprocess.Popen(args, shell=True)
        except Exception:
            print(f"Failed to run {args}")

    set_wallpaper_special_cases(wallpaper, desktop)
    first_run = False


def set_vlc_window(player: vlc.MediaPlayer, window_id: int) -> None:
    player.set_xwindow(window_id)
