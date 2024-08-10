import random
import time
from threading import Thread
from tkinter import Button, Label, Tk, Toplevel

from features.misc import open_web, panic
from screeninfo import get_monitors
from utils import utils
from utils.pack import Pack
from utils.settings import Settings


class Popup(Toplevel):
    def __init__(self, root: Tk, settings: Settings, pack: Pack):
        super().__init__()

        self.settings = settings
        self.pack = pack

        self.bind("<KeyPress>", lambda event: panic(root, settings, event.keysym))
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-type", "splash")
        # TODO: May be needed for opacity on some Linux setups
        # self.update_idletasks()
        # self.overrideredirect(True)
        # self.wait_visibility(self)

        self.opacity = self.settings.opacity
        self.attributes("-alpha", self.opacity)

    def init_finish(self) -> None:
        self.try_caption()
        self.try_button()
        self.try_move()
        self.try_timeout()

    def set_size_and_position(self, source_width: int, source_height: int) -> None:
        self.monitor = random.choice(get_monitors())

        source_size = max(source_width, source_height) / min(self.monitor.width, self.monitor.height)
        target_size = random.randint(30, 70) / 100
        scale = target_size / source_size

        self.width = int(source_width * scale)
        self.height = int(source_height * scale)
        self.x = random.randint(self.monitor.x, self.monitor.x + self.monitor.width - self.width)
        self.y = random.randint(self.monitor.y, self.monitor.y + self.monitor.height - self.height)

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

    def try_caption(self) -> None:
        if self.settings.captions_in_popups:
            label = Label(self, text=self.pack.random_caption(), wraplength=self.width)
            label.place(x=5, y=5)

    def try_button(self) -> None:
        if self.settings.buttonless:
            self.bind("<ButtonRelease-1>", lambda event: self.close())
        else:
            button = Button(self, text=self.pack.close_text, command=self.close)
            button.place(x=-10, y=-10, relx=1, rely=1, anchor="se")

    def try_move(self) -> None:
        def move() -> None:
            speed_x = 0 if self.settings.moving_chance else self.settings.moving_speed
            speed_y = 0 if self.settings.moving_chance else self.settings.moving_speed
            while speed_x == 0 and speed_y == 0:
                speed_x = random.randint(-self.settings.moving_speed, self.settings.moving_speed)
                speed_y = random.randint(-self.settings.moving_speed, self.settings.moving_speed)

            try:
                while True:
                    self.x += speed_x
                    self.y += speed_y

                    left = self.x <= self.monitor.x
                    right = self.x + self.width >= self.monitor.x + self.monitor.width
                    if left or right:
                        speed_x = -speed_x

                    top = self.y <= self.monitor.y
                    bottom = self.y + self.height >= self.monitor.y + self.monitor.height
                    if top or bottom:
                        speed_y = -speed_y

                    self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
                    time.sleep(0.01)
            except Exception:
                pass  # Exception thrown when closing

        if utils.roll(self.settings.moving_chance):
            Thread(target=move, daemon=True).start()

    def try_timeout(self) -> None:
        def fade_out() -> None:
            try:
                while self.opacity > 0:
                    self.opacity -= 0.01
                    self.attributes("-alpha", self.opacity)
                    time.sleep(0.015)
                self.close()
            except Exception:
                pass  # Exception thrown when manually closed during fade out

        if self.settings.timeout_enabled:
            self.after(self.settings.timeout, Thread(target=fade_out, daemon=True).start)

    def try_web_open(self) -> None:
        if self.settings.web_on_popup_close and utils.roll((100 - self.settings.web_chance) / 2):
            open_web(self.pack)

    def close(self) -> None:
        self.try_web_open()
        self.destroy()
