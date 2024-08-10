import time
from collections.abc import Callable
from threading import Thread
from tkinter import Toplevel

from PIL import Image
from screeninfo import get_monitors
from utils.pack import Pack
from widgets.image_label import ImageLabel


class StartupSplash(Toplevel):
    def __init__(self, pack: Pack, callback: Callable[[], None]):
        super().__init__()

        self.callback = callback

        self.wm_attributes("-topmost", True)
        self.wm_attributes("-type", "splash")

        monitor = next(m for m in get_monitors() if m.is_primary)

        image = Image.open(pack.startup_splash)

        # TODO: Better scaling
        scale = 0.6
        width = int(image.width * scale)
        height = int(image.height * scale)
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + (monitor.height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        ImageLabel(self, image, (width, height)).pack()
        Thread(target=self.animate, daemon=True).start()

    def animate(self) -> None:
        opacity = 0
        while opacity < 1:
            opacity += 0.01
            self.attributes("-alpha", opacity)
            time.sleep(0.01)

        time.sleep(2)
        while opacity > 0:
            opacity -= 2 * 0.01
            self.attributes("-alpha", opacity)
            time.sleep(0.01 / 4)

        self.destroy()
        self.callback()
