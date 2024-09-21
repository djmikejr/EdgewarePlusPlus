import random
from tkinter import Label, Toplevel

from features.theme import get_theme
from pack import Pack
from screeninfo import get_monitors
from settings import Settings
from utils import utils


class CaptionPopup(Toplevel):
    def __init__(self, settings: Settings, pack: Pack):
        if not self.should_init(settings, pack):
            return
        super().__init__()

        self.theme = get_theme(settings)

        self.attributes("-topmost", True)
        utils.set_borderless(self)
        self.attributes("-alpha", settings.opacity)
        if utils.is_windows():
            self.wm_attributes("-transparentcolor", self.theme.transparent_bg)

        monitor = random.choice(get_monitors())

        font = (self.theme.font, min(monitor.width, monitor.height) // 10)
        label = Label(
            self,
            text=pack.random_caption(settings),
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

    def should_init(self, settings: Settings, pack: Pack) -> bool:
        return pack.has_captions(settings)
