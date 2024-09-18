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


def get_wm_wallpaper_commands() -> list[str]:
    # Check if the session is X11 or Wayland so we can pick which wallpaper
    # setters to use. Otherwise may run into issues trying to use X11 wallpaper
    # utilities on Wayland and vice-versa
    session = os.environ.get("XDG_SESSION_TYPE")  # "x11" or "wayland"
    if session == "x11":
        wallpaper_setters = [
            "nitrogen",
            "feh",
            "habak",  # not tested
            "hsetroot",  # not tested
            "chbg",  # not tested
            "qiv",  # not tested
            "xv",  # not tested
            "xsri",  # not tested
            "xli",  # not tested
            "xsetbg",  # not tested
            "fvwm-root",  # not tested
            "wmsetbg",  # not tested
            "Esetroot",  # not tested
            "display",  # not tested
        ]
    elif session == "wayland":
        wallpaper_setters = []
    else:
        logging.warning(f"Unknown session: {session}")

    for setter in wallpaper_setters:
        # fmt: off
        if not shutil.which(setter): continue
        if setter == "feh": return ["feh --bg-scale %s"]
        if setter == "habak": return ["habak -ms %s"]
        if setter == "hsetroot": return ["hsetroot -fill %s"]
        if setter == "chbg": return ["chbg -once -mode maximize %s"]
        if setter == "qiv": return ["qiv --root_s %s"]
        if setter == "xv": return ["xv -max -smooth -root -quit %s"]
        if setter == "xsri": return ["xsri --center-x --center-y --scale-width=100 --scale-height=100 %s"]
        if setter == "xli": return ["xli -fullscreen -onroot -quiet -border black %s"]
        if setter == "xsetbg": return ["xsetbg -fullscreen -border black %s"]
        if setter == "fvwm-root": return ["fvwm-root -r %s"]
        if setter == "wmsetbg": return ["wmsetbg -s -S %s"]
        if setter == "display": return ["display -sample `xwininfo -root 2> /dev/null|awk '/geom/{print $2}'` -window root"]
        # fmt: on

        if setter == "nitrogen":
            # nitrogen can only set the wallpaper per-display, so get a list
            # of the display IDs and use multiple commands
            s = subprocess.Popen("xrandr --listmonitors | grep -Eo '[0-9]:' | tr -d ':'", shell=True, stdout=subprocess.PIPE)
            if not s.stdout:
                logging.warning("Couldn't find any X11 displays")
                return []
            format = "nitrogen --head=%s --set-zoom-fill %s"
            return [format % (line.decode().strip(), "%s") for line in s.stdout.readlines()]

        if setter == "Esetroot":
            # Esetroot needs libImlib
            s = subprocess.Popen(["ldd", "Esetroot"], stdout=subprocess.PIPE)
            if not s.stdout:
                logging.warning("There was a problem running ldd on Esetroot.")
                return []
            for line in s.stdout:
                if not re.search("libImlib", line):
                    logging.warning("No wallpaper support for Esetroot: missing libImlib.")
                    return []
                return ["Esetroot -scale %s"]


def is_running(process: str) -> bool:
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    if s.stdout:
        return any(re.search(process, line.decode().strip()) for line in s.stdout)
    return False
