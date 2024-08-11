import random
from tkinter import Label, Toplevel

from features.theme import get_theme
from screeninfo import get_monitors
from utils import utils
from utils.pack import Pack
from utils.settings import Settings


class CaptionPopup(Toplevel):
    def __init__(self, settings: Settings, pack: Pack):
        super().__init__()

        self.theme = get_theme(settings)

        self.wm_attributes("-topmost", True)
        self.wm_attributes("-type", "splash")
        self.attributes("-alpha", settings.opacity)
        if utils.is_windows():
            self.wm_attributes("-transparentcolor", self.theme.transparent_bg)

        monitor = random.choice(get_monitors())

        font = (self.theme.font, min(monitor.width, monitor.height) // 10)
        label = Label(
            self,
            text=pack.random_caption(),
            font=font,
            wraplength=monitor.width / 1.5,
            fg=self.theme.fg,
            bg=(self.theme.transparent_bg if utils.is_windows() else self.theme.bg),
        )
        label.pack()

        x = monitor.x + (monitor.width - label.winfo_reqwidth()) // 2
        y = monitor.y + (monitor.height - label.winfo_reqheight()) // 2

        self.geometry(f"+{x}+{y}")
        self.after(settings.caption_popup_timeout, self.destroy)
