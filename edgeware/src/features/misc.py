import logging
import random
import time
import webbrowser
from threading import Thread
from tkinter import Tk

from playsound import playsound
from pypresence import Presence
from utils import utils
from utils.pack import Pack
from utils.paths import PACK_PATH, Assets
from utils.settings import Settings


def panic(root: Tk, settings: Settings, key: str | None = None) -> None:
    if key and (settings.panic_disabled or key != settings.panic_key):
        return

    # TODO: https://github.com/araten10/EdgewarePlusPlus/issues/24
    utils.set_wallpaper(Assets.DEFAULT_PANIC_WALLPAPER)
    root.destroy()


def play_audio(settings: Settings, pack: Pack) -> None:
    global audio_number
    if "audio_number" not in globals():
        audio_number = 0

    # TODO: Race conditions?
    def play():
        audio_number += 1
        playsound(str(pack.random_audio()))
        audio_number -= 1

    if audio_number < settings.max_audio:
        Thread(target=play, daemon=True).start()


def open_web(pack: Pack) -> None:
    webbrowser.open(pack.random_web())


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
