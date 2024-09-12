import logging
import os
import shlex
import subprocess
import sys
from pathlib import Path

import vlc
from paths import Assets, Process
from settings import load_default_config
from utils.linux_utils import get_desktop_environment, get_wallpaper_commands, set_wallpaper_special_cases


def set_wallpaper(wallpaper: Path) -> None:
    desktop = get_desktop_environment()
    commands = get_wallpaper_commands(wallpaper, desktop)
    for command in commands:
        try:
            args = command % wallpaper
        except TypeError:
            args = command

        try:
            subprocess.Popen(args, shell=True)
        except Exception as e:
            logging.warning(f"Failed to run {args}. Reason: {e}")

    set_wallpaper_special_cases(wallpaper, desktop)


def set_vlc_window(player: vlc.MediaPlayer, window_id: int) -> None:
    player.set_xwindow(window_id)


def open_directory(url: str) -> None:
    subprocess.Popen(["xdg-open", url])


def make_shortcut(title: str, process: Path, icon: Path, location: Path | None = None) -> None:
    default_config = load_default_config()

    filename = f"{title}.desktop"
    file = (location if location else Path(os.path.expanduser("~/Desktop"))) / filename
    content = [
        "[Desktop Entry]",
        f"Version={default_config["versionplusplus"]}",
        f"Name={title}",
        f"Exec={shlex.join([str(sys.executable), str(process)])}",
        f"Icon={icon}",
        "Terminal=false",
        "Type=Application",
        "Categories=Application;",
    ]

    file.write_text("\n".join(content))
    if get_desktop_environment() == "gnome":
        subprocess.run(f'gio set "{str(file.absolute())}" metadata::trusted true', shell=True)


def toggle_run_at_startup(state: bool) -> None:
    autostart_path = Path(os.path.expanduser("~/.config/autostart"))
    if state:
        make_shortcut("Edgeware++", Process.MAIN, Assets.DEFAULT_ICON, autostart_path)
    else:
        (autostart_path / "Edgeware++.desktop").unlink(missing_ok=True)
