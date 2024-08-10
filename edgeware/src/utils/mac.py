from pathlib import Path

import vlc  # TODO: May fail


def set_wallpaper(wallpaper: Path) -> None:
    pass


def set_vlc_window(player: vlc.MediaPlayer, window_id: int) -> None:
    player.set_nsobject(window_id)
