import ctypes
from pathlib import Path

import vlc  # TODO: May fail


def set_wallpaper(wallpaper: Path) -> None:
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(wallpaper), 0)


def set_vlc_window(player: vlc.MediaPlayer, window_id: int) -> None:
    player.set_hwnd(window_id)
