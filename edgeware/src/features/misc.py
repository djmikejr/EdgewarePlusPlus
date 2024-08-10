import random
import webbrowser
from threading import Thread
from tkinter import Tk

from playsound import playsound
from utils import utils
from utils.pack import Pack
from utils.paths import PACK_PATH
from utils.settings import Settings


def panic(root: Tk, settings: Settings, key: str | None = None) -> None:
    if key and (settings.panic_disabled or key != settings.panic_key):
        return

    # TODO: Set panic wallpaper
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
