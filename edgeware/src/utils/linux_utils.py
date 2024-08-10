import codecs
import os
import re
import shutil
import subprocess
from configparser import ConfigParser
from pathlib import Path

# ruff: noqa: E701


def set_wallpaper_special_cases(wallpaper: Path, desktop: str) -> None:
    global first_run

    try:
        if desktop == "razor-qt":
            if first_run:
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
            else:
                pass  # TODO: Reload desktop when possible
    except Exception:
        print("Failed to set wallpaper")


# Source (Martin Hansen, Serge Stroobandt): https://stackoverflow.com/a/21213358
def get_desktop_environment() -> str:
    def is_running(process: str) -> bool:
        # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
        process = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
        if process.stdout:
            for line in process.stdout.readlines():
                if re.search(process, line.decode().strip()):
                    return True
        return False

    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    desktop = os.environ.get("XDG_CURRENT_DESKTOP")
    if not desktop:
        desktop = os.environ.get("DESKTOP_SESSION")

    # fmt: off
    if desktop:
        desktop = desktop.lower()

        ## Special cases ##
        # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
        # There is no guarantee that they will not do the same with the other
        # desktop environments.
        if "xfce" in desktop or desktop.startswith("xubuntu"): return "xfce4"
        if desktop.startswith("ubuntustudio"): return "kde"
        if desktop.startswith("ubuntu"): return "gnome"
        if desktop.startswith("lubuntu"): return "lxde"
        if desktop.startswith("kubuntu"): return "kde"
        if desktop.startswith("razor"): return "razor-qt"  # e.g. razorkwin
        if desktop.startswith("wmaker"): return "windowmaker"  # e.g. wmaker-common
        if desktop.startswith("pop"): return "gnome"
        return desktop
    if os.environ.get("KDE_FULL_SESSION") == "true": return "kde"
    if os.environ.get("GNOME_DESKTOP_SESSION_ID") and "deprecated" not in os.environ.get("GNOME_DESKTOP_SESSION_ID"): return "gnome2"
    if is_running("xfce-mcs-manage"): return "xfce4"
    if is_running("ksmserver"): return "kde"
    # fmt: on

    return "unknown"


def get_wallpaper_commands(wallpaper: Path, desktop: str) -> list[str]:
    global first_run

    # fmt: off
    if desktop in ["gnome", "unity", "cinnamon"]:
        return [
            "gsettings set org.gnome.desktop.background picture-uri file://%s",
            "gsettings set org.gnome.desktop.background picture-uri-dark file://%s",
        ]
    if desktop == "mate":
        return [
            "gsettings set org.mate.background picture-filename %s",  # MATE >= 1.6
            "mateconftool-2 -t string --set /desktop/mate/background/picture_filename %s",  # MATE < 1.6
        ]
    if desktop == "xfce4":
        return [
            "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s %s",
            "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-style -s 3",
            "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-show -s true",
        ] if first_run else ["xfdesktop --reload"]
    if desktop == "gnome2": return ["gconftool-2 -t string --set /desktop/gnome/background/picture_filename %s"]
    if desktop in ["kde3", "trinity"]: return ['dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6']
    if desktop in ["fluxbox", "jwm", "openbox", "afterstep"]: return ["fbsetbg %s"]
    if desktop == "icewm": return ["icewmbg %s"]
    if desktop == "blackbox": return ["bsetbg -full %s"]
    if desktop == "lxde": return ["pcmanfm --set-wallpaper %s --wallpaper-mode=scaled"]
    if desktop == "windowmaker": return ["wmsetbg -s -u %s"]
    if desktop == "sway": return ['swaybg -o "*" -i %s -m fill']
    if desktop in ["i3", "awesome", "dwm", "xmonad", "bspwm"]: return get_wm_wallpaper_commands()
    # fmt: on

    if desktop == "hyprland":
        if not shutil.which("hyprctl"):
            first_run_print("hyprpaper requires hyprctl.")
            return []
        preloaded = False
        process = subprocess.Popen("hyprctl hyprpaper listloaded", shell=True, stdout=subprocess.PIPE)
        if process.stdout:
            for line in process.stdout.readlines():
                if re.search(wallpaper, line.decode().strip()):
                    preloaded = True
                    break
        preload = [] if preloaded else ['hyprctl hyprpaper preload "%s"']
        return preload + ['hyprctl hyprpaper wallpaper ",%s"']

    return []


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
        first_run_print(f"Unknown session: {session}")

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
        # fmt: on

        if setter == "nitrogen":
            # nitrogen can only set the wallpaper per-display, so get a list
            # of the display IDs and use multiple commands
            process = subprocess.Popen("xrandr --listmonitors | grep -Eo '[0-9]:' | tr -d ':'", shell=True, stdout=subprocess.PIPE)
            if not process.stdout:
                first_run_print("Couldn't find any X11 displays")
                return []
            format = "nitrogen --head=%s --set-zoom-fill %s"
            return [format % (line.decode().strip(), "%s") for line in process.stdout.readlines()]

        if setter == "Esetroot":
            # Esetroot needs libImlib
            process = subprocess.Popen(["ldd", "Esetroot"], stdout=subprocess.PIPE)
            if not process.stdout:
                first_run_print("There was a problem running ldd on Esetroot.")
                return []
            for line in process.stdout:
                if not re.search("libImlib", line):
                    first_run_print("No wallpaper support for Esetroot: missing libImlib.")
                    return []
                return ["Esetroot -scale %s"]

        if setter == "display":
            if not shutil.which("xwininfo"):
                first_run_print("display needs xwininfo to query the size of the root window.")
                return []
            return ["display -sample `xwininfo -root 2> /dev/null|awk '/geom/{print $2}'` -window root"]


def first_run_print(text: str) -> None:
    global first_run
    if first_run:
        print(text)
