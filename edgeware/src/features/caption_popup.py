import random
from tkinter import Label, Toplevel

from screeninfo import get_monitors
from utils.pack import Pack
from utils.settings import Settings


# TODO: Transparent background for Windows
class CaptionPopup(Toplevel):
    def __init__(self, settings: Settings, pack: Pack):
        super().__init__()

        self.wm_attributes("-topmost", True)
        self.wm_attributes("-type", "splash")
        self.attributes("-alpha", settings.opacity)

        monitor = random.choice(get_monitors())

        font = ("Segoe UI", min(monitor.width, monitor.height) // 10)
        label = Label(self, text=pack.random_caption(), font=font, wraplength=monitor.width / 1.5)
        label.pack()

        x = monitor.x + (monitor.width - label.winfo_reqwidth()) // 2
        y = monitor.y + (monitor.height - label.winfo_reqheight()) // 2

        self.geometry(f"+{x}+{y}")
        self.after(settings.caption_popup_timeout, self.destroy)
