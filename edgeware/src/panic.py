from multiprocessing.connection import Client, Listener
from threading import Thread
from tkinter import Tk, simpledialog

from paths import Assets
from settings import Settings
from utils import utils
from utils.utils import State

ADDRESS = ("localhost", 6000)
AUTHKEY = b"Edgeware++"
PANIC_MESSAGE = "panic"


def panic(root: Tk, settings: Settings, state: State, key: str | None = None) -> None:
    if settings.panic_disabled or (key and key != settings.panic_key):
        return

    if settings.timer_mode and state.timer_active:
        password = simpledialog.askstring("Panic", "Enter Panic Password")
        if password != settings.timer_password:
            return

    # TODO: https://github.com/araten10/EdgewarePlusPlus/issues/24
    utils.set_wallpaper(Assets.DEFAULT_PANIC_WALLPAPER)
    root.destroy()


def start_panic_listener(root: Tk, settings: Settings, state: State) -> None:
    def listen() -> None:
        with Listener(address=ADDRESS, authkey=AUTHKEY) as listener:
            with listener.accept() as connection:
                message = connection.recv()
                if message == PANIC_MESSAGE:
                    panic(root, settings, state)

    Thread(target=listen, daemon=True).start()


def send_panic() -> None:
    with Client(address=ADDRESS, authkey=AUTHKEY) as connection:
        connection.send(PANIC_MESSAGE)


if __name__ == "__main__":
    send_panic()
