import codecs
import logging
import os
import re
import shutil
import subprocess
from configparser import ConfigParser
from pathlib import Path


def set_wallpaper_special_cases(wallpaper: Path, desktop: str) -> None:
    try:
        if desktop == "razor-qt":
            desktop_conf = ConfigParser()

            config_home = os.environ.get("XDG_CONFIG_HOME")
            if not config_home:
                config_home = os.environ.get("XDG_HOME_CONFIG", os.path.expanduser(".config"))
            config_dir = os.path.join(config_home, "razor")

            # Development version
            desktop_conf_file = os.path.join(config_dir, "desktop.conf")
            if os.path.isfile(desktop_conf_file):
                config_option = r"screens\1\desktops\1\wallpaper"
            else:
                desktop_conf_file = os.path.expanduser(".razor/desktop.conf")
                config_option = r"desktops\1\wallpaper"
            desktop_conf.read(os.path.join(desktop_conf_file))
            try:
                if desktop_conf.has_option("razor", config_option):  # only replacing a value
                    desktop_conf.set("razor", config_option, wallpaper)
                    with codecs.open(
                        desktop_conf_file,
                        "w",
                        encoding="utf-8",
                        errors="replace",
                    ) as f:
                        desktop_conf.write(f)
            except Exception:
                pass
    except Exception:
        logging.warning("Failed to set wallpaper")


# Modified from https://stackoverflow.com/a/21213358
def get_desktop_environment() -> str:
    desktop = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")
    if desktop:
        desktop = desktop.lower()

        special_cases = [
            ("xubuntu", "xfce4"),
            ("ubuntustudio", "kde"),
            ("ubuntu", "gnome"),
            ("lubuntu", "lxde"),
            ("kubuntu", "kde"),
            ("razor", "razor-qt"),  # e.g. razorkwin
            ("wmaker", "windowmaker"),  # e.g. wmaker-common
            ("pop", "gnome"),
        ]

        for special, actual in special_cases:
            if desktop.startswith(special):
                return actual
        if "xfce" in desktop:
            return "xfce4"
        return desktop
    if os.environ.get("KDE_FULL_SESSION") == "true":
        return "kde"
    if os.environ.get("GNOME_DESKTOP_SESSION_ID") and "deprecated" not in os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        return "gnome2"
    if is_running("xfce-mcs-manage"):
        return "xfce4"
    if is_running("ksmserver"):
        return "kde"

    return "unknown"


def get_wallpaper_commands(wallpaper: Path, desktop: str) -> list[str]:
    commands = {
        "mate": [
            f"gsettings set org.mate.background picture-filename {wallpaper}",  # MATE >= 1.6
            f"mateconftool-2 -t string --set /desktop/mate/background/picture_filename {wallpaper}",  # MATE < 1.6
        ],
        "xfce4": [
            f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s {wallpaper}",
            "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-style -s 3",
            "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-show -s true",
        ],
        "gnome2": [f"gconftool-2 -t string --set /desktop/gnome/background/picture_filename {wallpaper}"],
        "icewm": [f"icewmbg {wallpaper}"],
        "blackbox": [f"bsetbg -full {wallpaper}"],
        "lxde": [f"pcmanfm --set-wallpaper {wallpaper} --wallpaper-mode=scaled"],
        "windowmaker": [f"wmsetbg -s -u {wallpaper}"],
        "sway": [f'swaybg -o "*" -i {wallpaper} -m fill'],
        "hyprland": [f'hyprctl hyprpaper preload "{wallpaper}"', f'hyprctl hyprpaper wallpaper ",{wallpaper}"'],
        **dict.fromkeys(["gnome", "unity", "cinnamon"], [
            f"gsettings set org.gnome.desktop.background picture-uri file://{wallpaper}",
            f"gsettings set org.gnome.desktop.background picture-uri-dark file://{wallpaper}",
        ]),
        **dict.fromkeys(["kde3", "trinity"], [f'dcop kdesktop KBackgroundIface setWallpaper 0 "{wallpaper}" 6']),
        **dict.fromkeys(["fluxbox", "jwm", "openbox", "afterstep"], [f"fbsetbg {wallpaper}"]),
    }

    return commands.get(desktop) or (get_wm_wallpaper_commands() if desktop in ["i3", "awesome", "dwm", "xmonad", "bspwm"] else [])


def get_wm_wallpaper_commands(wallpaper: Path) -> list[str]:
    session = os.environ.get("XDG_SESSION_TYPE", "").lower()  # "x11" or "wayland"
    setters = {
        "x11": [
            ("nitrogen", []),
            ("feh", [f"feh --bg-scale {wallpaper}"]),
            ("habak", [f"habak -ms {wallpaper}"]),
            ("hsetroot", [f"hsetroot -fill {wallpaper}"]),
            ("chbg", [f"chbg -once -mode maximize {wallpaper}"]),
            ("qiv", [f"qiv --root_s {wallpaper}"]),
            ("xv", [f"xv -max -smooth -root -quit {wallpaper}"]),
            ("xsri", [f"xsri --center-x --center-y --scale-width=100 --scale-height=100 {wallpaper}"]),
            ("xli", [f"xli -fullscreen -onroot -quiet -border black {wallpaper}"]),
            ("xsetbg", [f"xsetbg -fullscreen -border black {wallpaper}"]),
            ("fvwm-root", [f"fvwm-root -r {wallpaper}"]),
            ("wmsetbg", [f"wmsetbg -s -S {wallpaper}"]),
            ("Esetroot", [f"Esetroot -scale {wallpaper}"])
            ("display", [f"display -sample `xwininfo -root 2> /dev/null|awk '/geom/{{print $2}}'` -window root {wallpaper}"]),
        ],
        "wayland": [],
    }

    for program, commands in setters.get(session, []):
        if shutil.which(program):
            if program == "nitrogen":
                # nitrogen can only set the wallpaper per-display, so get a list
                # of the display IDs and use multiple commands
                s = subprocess.Popen("xrandr --listmonitors | grep -Eo '[0-9]:' | tr -d ':'", shell=True, stdout=subprocess.PIPE)
                if not s.stdout:
                    logging.warning("Couldn't find any X11 displays")
                    return []
                return [f"nitrogen --head=%s --set-zoom-fill {wallpaper}" % (line.decode().strip(), "%s") for line in s.stdout.readlines()]
            return commands

    return []


def is_running(process: str) -> bool:
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    if s.stdout:
        return any(re.search(process, line.decode().strip()) for line in s.stdout)
    return False
