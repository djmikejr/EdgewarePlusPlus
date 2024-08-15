import logging
import random
import time
import webbrowser
from threading import Thread
from tkinter import Tk, simpledialog

import pystray
from PIL import Image
from playsound import playsound
from pypresence import Presence
from utils import utils
from utils.pack import Pack
from utils.paths import PACK_PATH, Assets
from utils.settings import Settings
from utils.utils import State


def panic(root: Tk, settings: Settings, state: State, key: str | None = None) -> None:
    if settings.panic_disabled or key != settings.panic_key:
        return

    if settings.timer_mode and state.timer_active:
        password = simpledialog.askstring("Panic", "Enter Panic Password")
        if password != "password":  # TODO: Actual password
            return

    # TODO: https://github.com/araten10/EdgewarePlusPlus/issues/24
    utils.set_wallpaper(Assets.DEFAULT_PANIC_WALLPAPER)
    root.destroy()


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


def make_tray_icon(root: Tk, settings: Settings, pack: Pack) -> None:
    menu = [pystray.MenuItem("Panic", lambda: panic(root, settings))]
    icon = pystray.Icon("Edgeware++", Image.open(pack.icon), "Edgeware++", menu)
    Thread(target=icon.run, daemon=True).start()


def handle_wallpaper(root: Tk, settings: Settings, pack: Pack) -> None:
    def rotate(previous: str = None) -> None:
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
