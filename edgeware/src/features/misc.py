import logging
import random
import time
import webbrowser
from collections.abc import Callable
from threading import Thread
from tkinter import Tk

import pystray
from pack import Pack
from panic import panic
from paths import PACK_PATH, Assets, Process
from PIL import Image
from playsound import playsound
from pypresence import Presence
from settings import Settings
from utils import utils
from utils.utils import State


def play_audio(settings: Settings, pack: Pack, state: State) -> None:
    # TODO: Race conditions?
    def play():
        state.audio_number += 1
        playsound(str(pack.random_audio()))
        state.audio_number -= 1

    if state.audio_number < settings.max_audio:
        Thread(target=play, daemon=True).start()


def open_web(pack: Pack) -> None:
    webbrowser.open(pack.random_web())


def make_tray_icon(root: Tk, settings: Settings, pack: Pack, state: State, hibernate_activity: Callable[[], None]) -> None:
    menu = [pystray.MenuItem("Panic", lambda: panic(root, settings, state))]
    if settings.hibernate_mode:

        def skip_hibernate() -> None:
            if state.hibernate_active:
                return

            try:
                root.after_cancel(state.hibernate_id)
            except Exception:
                pass
            hibernate_activity()

        menu.append(pystray.MenuItem("Skip to Hibernate", skip_hibernate))

    icon = pystray.Icon("Edgeware++", Image.open(pack.icon), "Edgeware++", menu)
    Thread(target=icon.run, daemon=True).start()


def make_desktop_icons(settings: Settings) -> None:
    if settings.desktop_icons:
        utils.make_shortcut("Edgeware++", Process.MAIN, Assets.DEFAULT_ICON)
        utils.make_shortcut("Edgeware++ Config", Process.CONFIG, Assets.CONFIG_ICON)
        utils.make_shortcut("Edgeware++ Panic", Process.PANIC, Assets.PANIC_ICON)


def handle_wallpaper(root: Tk, settings: Settings, pack: Pack, state: State) -> None:
    def rotate(previous: str = None) -> None:
        if settings.hibernate_fix_wallpaper and state.reset_wallpaper():
            return

        wallpapers = settings.wallpapers.copy()
        if previous:
            wallpapers.remove(previous)

        wallpaper = random.choice(wallpapers)
        utils.set_wallpaper(PACK_PATH / wallpaper)

        t = settings.wallpaper_timer
        v = settings.wallpaper_variance
        root.after(t + random.randint(-v, v), lambda: rotate(wallpaper))

    if settings.rotate_wallpaper and len(settings.wallpapers) > 1:
        rotate()
    else:
        utils.set_wallpaper(pack.wallpaper)


def handle_discord(root: Tk, settings: Settings, pack: Pack) -> None:
    if not settings.show_on_discord:
        return

    try:
        presence = Presence("820204081410736148")
        presence.connect()

        def update() -> None:
            presence.update(state=pack.discord_text, large_image=pack.discord_image, start=int(time.time()))
            root.after(15000, update)

        update()
    except Exception:
        logging.warning("Setting Discord presence failed")


def handle_timer_mode(root: Tk, settings: Settings, state: State) -> None:
    def timer_over() -> None:
        state.timer_active = False

    if settings.timer_mode:
        state.timer_active = True
        root.after(settings.timer_time, timer_over)


def handle_mitosis_mode(root: Tk, settings: Settings, pack: Pack, state: State) -> None:
    if settings.mitosis_mode:
        # Import done here to avoid circular imports
        from features.image_popup import ImagePopup

        ImagePopup(root, settings, pack, state)
