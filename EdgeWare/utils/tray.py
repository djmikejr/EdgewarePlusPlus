import hashlib
import logging
import os
import subprocess
import sys
import tkinter as tk
from tkinter import simpledialog

import pystray
from PIL import Image
from utils import utils
from utils.paths import Data, Defaults, Process, Resource
from utils.settings import Settings

settings = Settings()


# class to handle window for tray icon
class TrayHandler:
    def __init__(self, hiber_wait):
        self.root = tk.Tk()
        self.root.title("Edgeware")
        self.hiber_wait = hiber_wait

        self.option_list = [pystray.MenuItem("Edgeware Menu", print), pystray.MenuItem("Panic", self.try_panic)]
        if settings["toggleHibSkip"]:
            self.option_list.append(pystray.MenuItem("Skip to Hibernate", self.hib_skip))

        if os.path.isfile(Resource.ICON):
            self.tray_icon = pystray.Icon("Edgeware", Image.open(Resource.ICON), "Edgeware", self.option_list)
        else:
            self.tray_icon = pystray.Icon("Edgeware", Image.open(Defaults.ICON), "Edgeware", self.option_list)

        self.root.withdraw()

        self.password_setup()

    def hib_skip(self):
        if settings.HIBERNATE_MODE:
            try:
                self.hiber_wait.set()
            except Exception as e:
                logging.critical(f"failed to skip to hibernate start. {e}")

    def password_setup(self):
        if settings.TIMER_MODE:
            try:
                utils.show_file(Data.PASS_HASH)
                with open(Data.PASS_HASH, "r") as file:
                    self.hashedPass = file.readline()
                utils.hide_file(Data.PASS_HASH)
            except Exception:
                # no hash found
                self.hashedPass = None

    def try_panic(self):
        logging.info("attempting tray panic")
        if not settings.PANIC_DISABLED:
            if settings.TIMER_MODE:
                pass_ = simpledialog.askstring("Panic", "Enter Panic Password")
                t_hash = None if pass_ is None or pass_ == "" else hashlib.sha256(pass_.encode(encoding="ascii", errors="ignore")).hexdigest()
                if t_hash == self.hashedPass:
                    # revealing hidden files
                    try:
                        utils.show_file(Data.PASS_HASH)
                        utils.show_file(Data.HID_TIME)
                        os.remove(Data.PASS_HASH)
                        os.remove(Data.HID_TIME)
                        subprocess.Popen([sys.executable, Process.PANIC])
                    except Exception:
                        logging.critical("panic initiated due to failed pass/timer check")
                        self.tray_icon.stop()
                        subprocess.Popen([sys.executable, Process.PANIC])
            else:
                logging.warning("panic initiated from tray command")
                self.tray_icon.stop()
                subprocess.Popen([sys.executable, Process.PANIC])

    def move_to_tray(self):
        self.tray_icon.run(tray_setup)
        logging.info("tray handler thread running")


def tray_setup(icon):
    icon.visible = True
